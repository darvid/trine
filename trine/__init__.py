#!/usr/bin/env python
"""Generate DB structures for WoW emulators with YAML."""
import abc
import argparse
import logging
import sys

import schema
import yaml

from sqlalchemy import create_engine, select, exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import and_, or_
from sqlalchemy.sql.expression import desc, _BinaryExpression

from sweet.io.fs import file_local_path, path
from sweet.structures.dict import AttrDict
from sweet.structures.list import flatten

from trine.models import initialize_world_db_connection, world, WorldDBSession
from trine.util import _col_constants_mapping, get_cmp, get_flags, get_table, printquery
from trine import yamlobjects


default_wd = path("~/.trine")
log = logging.getLogger("trine")


class SpecFile(object):

    def __init__(self, documents, from_file=None):
        if not isinstance(documents, list):
            documents = [documents]
        self.documents = documents
        self.from_file = path(from_file)

        self.models = []
        for document in self.documents:
            for name, documents in document.items():
                if not name.startswith("_"):
                    for data in documents:
                        model = Model(name, data)
                        model.validate()
                        self.models.append(model)

        for model in self.models:
            model.validate()

    @classmethod
    def load_from(cls, file_):
        file_ = path(file_)
        if not file_.exists:
            log.error("file does not exist: {0}".format(file_.absolute))
            return
        return cls(list(yaml.load_all(file_.open("r"))), file_)

    def build_all_queries(self):
        for model in self.models:
            for query in model.build_queries():
                yield model.table.bind, query

    def __repr__(self):
        return "<{0}(models=[{2}], from_file='{1}')>".format(
            self.__class__.__name__,
            self.from_file,
            ", ".join([repr(model) for model in self.models])
        )


class Model(object):

    def __init__(self, name, data):
        self.name = name
        self.table = get_table(name)
        self.method = data.pop("method", "create").lower()
        self.data = data
        self.process()

    def _execute(self, *args, **kwargs):
        return self.table.bind.execute(*args, **kwargs)

    def process(self):
        def _process_where(data, table):
            if not "where" in data:
                return
            for where_col_name, values in data["where"].items():
                if not isinstance(values, list):
                    values = [values]
                data["where"][where_col_name] = []
                for value in values:
                    if isinstance(value, yamlobjects.SelectQueryBuilder):
                        rows = flatten(self._execute(value.build()).fetchall())
                        for field in rows:
                            data["where"][where_col_name].append(
                                get_cmp(table, where_col_name, field)
                            )
                    else:
                        data["where"][where_col_name].append(
                            get_cmp(table, where_col_name, value)
                        )
        for col_name, values in self.data.items():
            flags = get_flags(col_name, values)

            # DBC flags
            if flags is not None:
                self.data[col_name] = flags

            # vendor items
            elif col_name == "items" and values is not None:
                items = []
                item_table = get_table("ItemTemplate")
                if not isinstance(values, list):
                    values = [values]
                for item in values:
                    query_append = None
                    if isinstance(item, basestring):
                        if item.endswith("^"):
                            item = item[:-1]
                            query_append = lambda q: q.order_by(desc(item_table.c.ItemLevel))
                        query = select([item_table.c.entry])\
                            .where(get_cmp(item_table, "name", item))
                        if query_append:
                            query = query_append(query)
                        items.append(self._execute(query).fetchone())
                        if items[-1] is None:
                            log.error("could not find entry for '{0}'".format(item))
                    elif isinstance(item, int):
                        items.append(item)
                    elif isinstance(item, yamlobjects.SelectQueryBuilder):
                        items += item_table.bind.execute(item.build()).fetchall()
                self.data["items"] = flatten(items)

            elif col_name == "extended_costs":
                costs = self.data["extended_costs"]
                costs = [costs] if not isinstance(costs, list) else costs
                for cost_spec in costs:
                    _process_where(cost_spec, get_table("ItemTemplate"))

        _process_where(self.data, self.table)

    def build_queries(self):
        queries = []
        where = []
        if self.method == "update":
            values = {}
            for column in self.table.columns:
                if column.name in self.data:
                    values[column] = self.data[column.name]
            query = self.table.update().values(values)
            where = []
            for name, exprs in self.data["where"].items():
                if len(exprs) > 1:
                    where.append(or_(*exprs))
                else:
                    where.append(exprs[0])
            if len(where) > 1:
                queries.append(query.where(and_(*where)))
            else:
                queries.append(query.where(*where))

        elif self.method == "merge" and "merge-from" in self.data:
            merge_from = self.data["merge-from"]

            if isinstance(merge_from, dict):
                for col_name, value in merge_from.items():
                    merge_from[col_name] = get_cmp(self.table, col_name, value)
                query = self.table.select().where(*merge_from.values())
            else:
                query = self.table.select().where({"entry": merge_from})
            templ = dict(self.table.bind.execute(query).fetchone())
            for col_name, value in self.data.items():
                if col_name in templ:
                    templ[col_name] = value

            if (self._execute(select([exists().where(
                self.table.c.entry == templ["entry"])])).scalar()):
                queries.append(self.table.update()\
                    .where(self.table.c.entry == templ["entry"])\
                    .values(**templ))
            else:
                queries.append(self.table.insert().values(**templ))

        elif self.method == "create":
            data = dict([(k, v) for k, v in self.data.items() if k not in
                ("method", "merge-from", "items", "extended_costs")])
            pk = None
            for col_name, value in data.items():
                if getattr(getattr(self.table.c, col_name), "primary_key"):
                    pk = col_name
            assert pk, "Could not find a primary key for model `{0}`, use "\
                "the MERGE or UPDATE methods instead.".format(self.name)
            pk_col = getattr(self.table.c, pk)
            if (self._execute(select([exists().where(pk_col == data[pk])])).scalar()):
                queries.append(self.table.update()\
                    .where(pk_col == data[pk])\
                    .values(**data))
            else:
                queries.append(self.table.insert().values(**data))

        vendor = get_table("NpcVendor")
        entry = self.data["entry"] if "entry" in self.data else None

        if "items" in self.data:
            if entry is None and "where" in self.data:
                query = select([self.table.columns.entry])
                where = []
                for name, exprs in self.data["where"].items():
                    if len(exprs) > 1:
                        where.append(or_(*exprs))
                    else:
                        where.append(exprs[0])
                if len(where) > 1:
                    query = query.where(and_(*where))
                else:
                    query = query.where(*where)
                entry = self._execute(query).fetchone()["entry"]
            assert entry is not None, "missing creature_template entry"
            slot = 0
            queries.append(vendor.delete().where(vendor.columns.entry == entry))
            for item in self.data["items"]:
                queries.append(vendor.insert().values(
                    entry=entry,
                    slot=slot,
                    item=item,
                    maxcount=0,
                    incrtime=0,
                    # extended costs are handled separately as it is more likely
                    # one will want to apply extended costs in bulk rather than
                    # item by item.
                    ExtendedCost=0
                ))
                slot += 1

        if "extended_costs" in self.data:
            for cost_spec in self.data["extended_costs"]:
                item_table = get_table("ItemTemplate")
                query = select([item_table.c.entry])
                where = []
                if "where" in cost_spec:
                    for name, exprs in cost_spec["where"].items():
                        if len(exprs) > 1:
                            where.append(or_(*exprs))
                        else:
                            where.append(exprs[0])
                where.append(item_table.c.entry.in_(self.data["items"]))
                query = query.where(and_(*where) if len(where) > 1 else where[0])
                item_ids = self._execute(query)
                for row in item_ids:
                    queries.append(vendor.update().values(ExtendedCost=cost_spec["cost"])\
                        .where(and_(vendor.c.entry == entry, vendor.c.item == row[0])))
        return queries


    def validate(self):
        if self.method == "update" and "where" not in self.data:
            raise schema.SchemaError("Update method requires where dict")
        def _build_all_cols(data, table, use_expr=False):
            all_cols = {}
            for column in table.columns:
                # schema breaks on values expected to be strings which are None
                if (column.name in data and column.type.python_type == str and
                    data[column.name] is None):
                    data[column.name] = ""
                all_cols[schema.Optional(column.name)] = (column.type.python_type
                    if not use_expr else lambda o: isinstance(o, (list, _BinaryExpression)))
            return all_cols
        all_cols = _build_all_cols(self.data, self.table)
        if self.method == "update":
            where = all_cols["where"] = {}
            for col_name, value in all_cols.items():
                if col_name == "where": continue
                if isinstance(col_name, schema.Optional):
                    col_name = col_name._schema
                value = lambda o: isinstance(o, (list, _BinaryExpression))
                where[schema.Optional(col_name)] = value
            schema.Schema(all_cols["where"]).validate(self.data["where"])
        all_cols[schema.Optional("items")] = list
        all_cols[schema.Optional("merge-from")] = schema.Or(dict, int)
        all_cols[schema.Optional("extended_costs")] = [{
            schema.Optional("where"): _build_all_cols(
                self.data.get("extended_costs", {}),
                get_table("ItemTemplate"), True),
            "cost": int
        }]
        schema.Schema(all_cols).validate(self.data)

    def __repr__(self):
        return "<{0}(name='{1}')>".format(self.__class__.__name__, self.name)


def setup_logging(logger=log):
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    console.setFormatter(logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s"))
    log.addHandler(console)


def setup_db_sessions(config):
    db_uri = "{0}://{1}:{2}@{3}/{4}"

    world_engine = create_engine(db_uri.format(
        config.db.type,
        config.db.username,
        config.db.password,
        config.db.host,
        config.db.world_db
    ))

    initialize_world_db_connection(world_engine)
    world_session = WorldDBSession
    return AttrDict({
        "world": WorldDBSession,
    })


def main():
    setup_logging()

    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--working-directory", dest="path",
        default=path("."), nargs="?", help="specify path to YAML documents")
    parser.add_argument("spec", help="name of spec or 'all'")
    parser.add_argument("operation", help="[execute|dml]", nargs="?",
        default="dml")
    args = parser.parse_args()

    op = args.operation.lower()
    if op not in ("execute", "dml"):
        log.error("invalid operation")
        sys.exit(1)

    wd = path(args.path)
    search_path = [wd]
    if not wd.exists:
        log.error("directory '{0}' does not exist".format(wd))
        if not default_wd.exists:
            log.critical("default working directory ({0}) does not exist".format(default_wd))
            sys.exit(1)
        search_path += default_wd
    config_file = None
    search_path = [wd]
    if default_wd.exists:
        search_path.append(default_wd)
    for documents in [p.glob("*.yml") for p in search_path]:
        if not documents:
            log.error("no YAML documents found in {0}".format(wd.absolute))
        else:
            for document in documents:
                if document.name == "config.yml":
                    config_file = document
                    break
        if config_file: break
    config = AttrDict(yaml.load(config_file.open("r")))
    setup_db_sessions(config)

    specs = []
    for documents in [p.glob("*.yml") for p in search_path]:
        for spec in documents:
            if spec.name == "config.yml": continue
            if args.spec == "all" or spec.name.startswith(args.spec):
                specs.append(spec)
                if args.spec == spec.name:
                    break
    if not specs:
        log.error("invalid spec name")
        sys.exit(1)

    yamlobjects.install()

    for spec in specs:
        spec = SpecFile.load_from(spec)

        queries = spec.build_all_queries()

        for bind, query in queries:
            if op == "dml":
                printquery(query, bind)
            elif op == "execute":
                bind.execute(query)