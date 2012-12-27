"""
    trine.tags
    ~~~~~~~~~~

    Provides convenient YAML tags for use within **Trine** schemata.

    :copyright: Copyright 2012 by David Gidwani
    :license: BSD, see LICENSE for details.
"""
from collections import defaultdict
import logging
import re
import yaml
import tarjan

from sqlalchemy.sql import and_, or_, not_, select
from sweet.io.fs import path

from trine.util import get_cmp, get_flags, get_table, printquery


log = logging.getLogger("trine")
_include_edges = defaultdict(list)


def _query(model, what, where):
    """
    Internal. Retrieves the appropriate table from a **model** name, and selects
    a single column (**what**) restricted by a dictionary representing the
    **WHERE** clause.
    """
    table = get_table(model)
    if table is None:
        log.error("invalid model name: {0}".format(model))
        raise
    _where = []
    for col_name, value in where.items():
        _where.append(get_cmp(table, col_name, value)[0])
    query = select([getattr(table.c, what)], and_(*_where))
    return query


class SelectQueryBuilder(yaml.YAMLObject):
    """
    Provides a YAML tag that selects at most one column of results from a given
    table.
    """
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
    """
    Selects item entries (or IDs) based on a **where** mapping.
    """
    yaml_tag = u"!getitems"

    def __init__(self, **where):
        pass

    def build(self):
        return _query("ItemTemplate", "entry", self.__dict__)

    def __repr__(self):
        return "<{0}(where={1})>".format(self.__class__.__name__, self.__dict__)


def include_tag(loader, node):
    """
    Provides simplistic include support for YAML.
    """
    current_file = path(loader.stream.name)
    include_file = current_file.parent.join(node.value)
    if not include_file.exists:
        raise yaml.YAMLError("'%s' does not exist" % include_file)
    _include_edges[current_file.absolute].append(include_file.absolute)
    for edges in tarjan.tarjan(_include_edges):
        if len(edges) > 1:
            raise yaml.YAMLError("circular dependency detected between %r" %
                edges)
    return yaml.load(include_file.open())


def install_yaml_tags():
    # manually add constructors or representers here
    yaml.add_constructor("!include", include_tag)