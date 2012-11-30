import logging
import re
import yaml

from sqlalchemy.sql import and_, or_, not_, select

from trine.util import get_cmp, get_flags, get_table, printquery


log = logging.getLogger("trine")


def _query(model, what, where):
    table = get_table(model)
    if table is None:
        log.error("invalid model name: {0}".format(model))
        raise
    _where = []
    for col_name, value in where.items():
        _where.append(get_cmp(table, col_name, value))
    query = select([getattr(table.c, what)], and_(*_where))
    return query


class SelectQueryBuilder(yaml.YAMLObject):
    yaml_tag = u"!query"

    def __init__(self, model, what, where):
        self.model = model
        self.what = what
        assert not isinstance(what, (list, tuple))
        self.where = where

    def build(self):
        return _query(self.model, self.what, self.where)

    @property
    def table(self):
        return get_table(self.model)

    def __repr__(self):
        return "<{0}(model='{1}', where={2})>".format(
            self.__class__.__name__,
            self.model,
            self.where
        )


class SelectItemBuilder(SelectQueryBuilder):
    yaml_tag = u"!getitems"

    def __init__(self, **where):
        pass

    def build(self):
        return _query("ItemTemplate", "entry", self.__dict__)

    def __repr__(self):
        return "<{0}(where={1})>".format(self.__class__.__name__, self.__dict__)


def install():
    # manually add constructors or representers here
    pass