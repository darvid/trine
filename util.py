from sqlalchemy import desc
from models.world import ItemTemplate


_custom_ids = {}


def get_items(session, items, filters=[], order_by=desc(ItemTemplate.ItemLevel)):
    """Retrieve one or more items from the `item_template` table.

    By default, only the first matching item result is returned.

    If **items** ends with a `%`, a LIKE clause is used to filter item names.

    If **items** ends with a `^`, only the one result with the highest iLevel is
    returned.

    If **items** ends with a `*`, all items matching the given name are
    returned.
    """
    result = []
    query = session.query(ItemTemplate)
    for item_name in items:
        if callable(item_name): item_name = item_name()
        if "%" in item_name:
            subresult = query.filter(ItemTemplate.name.like(item_name)).all()
        elif item_name.endswith("^"):
            subresult = [
                query.filter_by(name=item_name[:-1]).\
                    order_by(order_by).\
                    first()
            ]
        elif item_name.endswith("*"):
            subresult = query.filter_by(name=item_name[:-1]).all()
        else:
            subresult = [query.filter(ItemTemplate.name == item_name).first()]
        if filters:
            for item in subresult:
                for item_filter in filters:
                    if not item_filter(item):
                        subresult.remove(item)
        result += subresult
    return result


def init_custom_id(name, num):
    _custom_ids[name] = num - 1


def incr_custom_id(name):
    _custom_ids[name] += 1
    return _custom_ids[name]

def get_custom_id(name):
    return _custom_ids[name]

def get_last_custom_id(name):
    return get_custom_id(name) - 1