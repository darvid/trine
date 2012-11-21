from sqlalchemy import desc
from sqlalchemy.ext import compiler
from sqlalchemy.sql.expression import Executable, ClauseElement

from trine import constants
from trine.models import world

from sweet.structures.list import flatten


_col_constants_mapping = {
    'AllowableClass': constants.ChrClasses,
    'npcflag': constants.NpcFlag,
    'race': constants.ChrRaces
}
_custom_ids = {}


class InsertFromSelect(Executable, ClauseElement):
    def __init__(self, table, select):
        self.table = table
        self.select = select

@compiler.compiles(InsertFromSelect)
def visit_insert_from_select(element, compiler, **kw):
    return "INSERT INTO %s (%s)" % (
        compiler.process(element.table, asfrom=True),
        compiler.process(element.select)
    )


def get_cmp(table, col_name, value):
    col = getattr(table.c, col_name)

    neg = False
    cmp_in = False

    if isinstance(value, basestring) and value.startswith("!"):
        value = value[1:]
        neg = True

    if isinstance(value, basestring) and value.startswith("in "):
        value = value[3:]
        cmp_in = True

    flags = get_flags(col_name, value)
    if flags is not None:
        value = col.in_(flags) if cmp_in else (col == flags)

    if isinstance(value, basestring) and "%" in value:
        value = col.like(value)
        if neg:
            value = not_(value)
    elif neg:
        value = not_(value)
    elif flags is None:
        value = col == value

    return value


def get_flags(col_name, values):
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
    """Retrieve one or more items from the `item_template` table.

    By default, only the first matching item result is returned.

    If **items** ends with a `%`, a LIKE clause is used to filter item names.

    If **items** ends with a `^`, only the one result with the highest iLevel is
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
    for db in [world]:
        obj = getattr(db, model_name, None)
        if obj is None:
            continue
        return obj.__table__
    log.error("could not find corresponding table for {0} in any db".format(model_name))


def init_custom_id(name, num):
    _custom_ids[name] = num - 1


def incr_custom_id(name):
    _custom_ids[name] += 1
    return _custom_ids[name]


def get_custom_id(name):
    return _custom_ids[name]


def get_last_custom_id(name):
    return get_custom_id(name) - 1


def printquery(statement, bind=None):
    """
    print a query, with values filled in
    for debugging purposes *only*
    for security, you should always separate queries from their values
    please also note that this function is quite slow
    """
    import sqlalchemy.orm
    if isinstance(statement, sqlalchemy.orm.Query):
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