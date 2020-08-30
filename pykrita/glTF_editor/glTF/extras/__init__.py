from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class Extras(object):
    """
    ...
    """

    def __init__(self,
                items=None):

        self._items = oDict()

        if items is not None:
            self.items = items


    @classmethod
    def cast(cls, obj):
        if isinstance(obj, cls):
            return cls(
                    items=obj.items)
        elif isinstance(obj, Mapping):
            return cls(
                    items=obj.get("items"))
        elif isinstance(obj, UnicodeType):
            unserialized = serializer.loads(obj)
            if not isinstance(unserialized, UnicodeType):
                return cls.cast(unserialized)
        elif isinstance(obj, Iterable):
            it = iter(obj)
            return cls(
                    items=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def getItems(self):
        if self._items is None:
            return None
        else:
            return iter(self._items)
    def setItems(self, newItems):
        if newItems is None:
            self._items = None
        else:
            self._items = [UnicodeType(n) for n in newItems]
    items = property(getItems, setItems)


    def __str__(self):
        return serializer.dumps(self, type_hints=False)


    def __repr__(self):
        cls = type(self)
        return ("{cls.__name__}("
                "items={self.items!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("items")
    return result


serializer.register(
        data_cls=Extras,
        from_dict=lambda dct: Extras.cast(dct),
        to_dict=to_dict)
