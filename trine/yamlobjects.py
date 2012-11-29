import logging
import re
import yaml

from sqlalchemy.sql import and_, or_, not_, select

from trine.util import get_cmp, get_flags, get_table, printquery


log = logging.getLogger("trine")


class SelectQueryBuilder(yaml.YAMLObject):
    yaml_tag = u"!query"

    def __init__(self, model, what, where):
        self.model = model
        self.what = what
        assert not isinstance(what, (list, tuple))
        self.where = where

    def build(self):
        table = get_table(self.model)
        if table is None:
            log.error("invalid model name: {0}".format(self.model))
            raise
        where = []
        for col_name, value in self.where.items():
            where.append(get_cmp(table, col_name, value))
        query = select([getattr(table.c, self.what)], and_(*where))
        return query

    @property
    def table(self):
        return get_table(self.model)

    def __repr__(self):
        return "<{0}(model='{1}', where={2})>".format(
            self.__class__.__name__,
            self.model,
            self.where
        )


def install():
    # manually add constructors or representers here
    pass