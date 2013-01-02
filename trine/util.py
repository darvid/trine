"""
    trine.util
    ~~~~~~~~~~

    Provides utility methods which are used internally but can also be used in
    an interactive interpreter when interfacing with an emulator's database.

    :copyright: Copyright 2012 by David Gidwani
    :license: BSD, see LICENSE for details.
"""
import logging

from clint.textui import colored, puts

from sqlalchemy import desc, func, select
from sqlalchemy.ext import compiler
from sqlalchemy.orm import Query
from sqlalchemy.sql import and_
from sqlalchemy.sql.expression import Executable, ClauseElement

from trine import constants
from trine.models import world

from sweet.structures.list import flatten


log = logging.getLogger("trine")


# maps known flag columns to their respective class equivalents from
# trine.constants
_col_constants_mapping = {
    'AllowableClass': constants.ChrClasses,
    'AllowableRace': constants.ChrRaces,
    'npcflag': constants.NpcFlag,
    'race': constants.ChrRaces,
    'faction_H': constants.FactionTemplate,
    'faction_A': constants.FactionTemplate,
    'InventoryType': constants.InventoryType,
}

# XXX: unused
# holds global identifiers for accessing and incrementing row IDs for custom
# creatures/items/spells
_custom_ids = {}

# provides user-friendly aliases for frequently used model names
_table_aliases = {
    "CreatureTemplate": ["npc"],
    "ItemTemplate": ["item"],
}


# XXX: unused
class InsertFromSelect(Executable, ClauseElement):
    def __init__(self, table, select):
        self.table = table
        self.select = select


# XXX: unused
@compiler.compiles(InsertFromSelect)
def visit_insert_from_select(element, compiler, **kw):
    return "INSERT INTO %s (%s)" % (
        compiler.process(element.table, asfrom=True),
        compiler.process(element.select)
    )


def get_cmp(table, col_name, value):
    """
    Build a SQL expression for a given column from a representational
    dictionary.
    """
    col = getattr(table.c, col_name)
    original_value = value

    neg = False
    cmp_in = False
    regex = False
    max_ilvl = False

    is_string = isinstance(value, basestring)

    if is_string and value.startswith("!"):
        value = value[1:]
        neg = True

    if is_string and value.endswith("^"):
        value = value[:-1]
        assert str(table) == "item_template"
        # TODO: support other tables where a use case exists for restricting
        # results to the MAX/MIN of a specific column
        max_ilvl = True

    if is_string and value.startswith("/") and value.endswith("/"):
        value = value[1:-1]
        regex = True

    elif is_string and value.startswith("in "):
        value = value[3:]
        cmp_in = True

    flags = get_flags(col_name, value)
    if flags is not None:
        value = col.in_(flags) if cmp_in else (col == flags)
    elif regex:
        value = col.op("rlike")(value)
    elif is_string and "%" in value:
        value = col.like(value)
        if neg:
            value = not_(value)
    elif neg:
        value = not_(value)
    elif flags is None:
        value = col == value

    # TODO: actually handle this monkeypatch in the Model object, and stop using
    # the AWFUL subquery hack below.
    value._max = None
    if max_ilvl:
        value._max = func.max(table.c.ItemLevel)
        subquery = select(["*"]).select_from(
            select([func.max(table.c.ItemLevel)]).where(value).alias("tmp")
        )
        value = and_(value, table.c.ItemLevel == subquery)

    return (value, original_value)


def get_flags(col_name, values):
    """
    Convert flag names to their respective numerical values.
    """
    if col_name not in _col_constants_mapping:
        return
    if not isinstance(values, (list, tuple)):
        values = [values]
    const_group = _col_constants_mapping[col_name]
    flags = []
    for value in values:
        if isinstance(value, int):
            flags.append(value)
            continue
        const_name = value.upper().replace(" ", "_")
        const = getattr(const_group, const_name)
        if isinstance(const, (constants.Race, constants.Class)):
            const = const.binary
        flags.append(const)
    if not tuple in map(type, flags):
        return sum(flags)
    else:
        def convert(flags_):
            if isinstance(flags_, (list, tuple)):
                flags_ = list(flags_)
                for index, flag in enumerate(flags_):
                    try:
                        flags_[index] = flag.id
                    except AttributeError:
                        pass
            return flags_
        return flatten(map(convert, flags))


def get_items(session, items, filters=[], order_by=desc(world.ItemTemplate.ItemLevel)):
    """
    Retrieve one or more items from the `item_template` table. By default, only
    the first matching item result is returned.

    If **items** ends with a `%`, a LIKE clause is used to filter item names.

    If **items** ends with a `^`, the item with the highest ItemLevel is
    returned.

    If **items** ends with a `*`, all items matching the given name are
    returned.
    """
    result = []
    query = session.query(world.ItemTemplate)
    for item_name in items:
        if callable(item_name): item_name = item_name()
        if "%" in item_name:
            subresult = query.filter(world.ItemTemplate.name.like(item_name)).all()
        elif item_name.endswith("^"):
            subresult = [
                query.filter_by(name=item_name[:-1]).\
                    order_by(order_by).\
                    first()
            ]
        elif item_name.endswith("*"):
            subresult = query.filter_by(name=item_name[:-1]).all()
        else:
            subresult = [query.filter(world.ItemTemplate.name == item_name).first()]
        if filters:
            for item in subresult:
                for item_filter in filters:
                    if not item_filter(item):
                        subresult.remove(item)
        result += subresult
    return result


def get_table(model_name):
    """
    Returns a SQLAlchemy **Table** object for a given model name.
    """
    for real_model_name, aliases in _table_aliases.items():
        if model_name.lower() in aliases:
            model_name = real_model_name
    for db in [world]:
        obj = getattr(db, model_name, None)
        if obj is None:
            continue
        return obj.__table__
    log.error("could not find corresponding table for %s in any db" % model_name)


# From http://stackoverflow.com/a/5698357
def printquery(statement, bind=None):
    """
    print a query, with values filled in
    for debugging purposes *only*
    for security, you should always separate queries from their values
    please also note that this function is quite slow
    """
    if isinstance(statement, Query):
        if bind is None:
            bind = statement.session.get_bind(
                    statement._mapper_zero_or_none()
            )
        statement = statement.statement
    elif bind is None:
        bind = statement.bind

    dialect = bind.dialect
    compiler = statement._compiler(dialect)

    class LiteralCompiler(compiler.__class__):
        def visit_bindparam(
                self, bindparam, within_columns_clause=False,
                literal_binds=False, **kwargs
        ):
            return super(LiteralCompiler, self).render_literal_bindparam(
                    bindparam, within_columns_clause=within_columns_clause,
                    literal_binds=literal_binds, **kwargs
            )

    compiler = LiteralCompiler(dialect, statement)
    print(compiler.process(statement) + ";")


def truncate(str_or_list, char_length=80, list_length=None, split_words=True,
             join_str=" "):
    """
    Truncates a string or list for printing.
    """
    if isinstance(str_or_list, basestring):
        if len(str_or_list) <= char_length:
            return str_or_list
        if not split_words:
            return str_or_list[:char_length - 4] + " ..."
        else:
            char_count = 0
            words = str_or_list.split(join_str)
            trunc_words = []
            for index, word in enumerate(words):
                char_count += len(word)
                if index != len(words) - len(join_str):
                    char_count += len(join_str)
                if char_count >= char_length - 4:
                    return join_str.join(trunc_words) + " ..."
                trunc_words.append(word)
    elif isinstance(str_or_list, (list, tuple)):
        str_or_list = list(str_or_list)
        if list_length is None:
            return "[%s]" % truncate(str(str_or_list), char_length - 2)
        else:
            return (str(str_or_list[:list_length])[:-1] + ", ...]"
                    if len(str_or_list) > list_length else str(str_or_list))


def setup_logging(logger=log):
    """
    Initialize logging handlers.
    """
    class ColoredLevelFormatter(logging.Formatter, object):
        def format(self, record):
            if record.levelno in (logging.WARNING, logging.CRITICAL,
                logging.ERROR):
                record.msg = colored.red("[!] ") + colored.clean(record.msg)
            else:
                record.msg = colored.green("(i) ") + colored.clean(record.msg)
            return super(ColoredLevelFormatter, self).format(record)

    logger.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setFormatter(ColoredLevelFormatter("%(message)s"))
    logger.addHandler(console)


# XXX: Deprecated functions included for possible future use
def init_custom_id(name, num):
    _custom_ids[name] = num - 1


def incr_custom_id(name):
    _custom_ids[name] += 1
    return _custom_ids[name]


def get_custom_id(name):
    return _custom_ids[name]


def get_last_custom_id(name):
    return get_custom_id(name) - 1