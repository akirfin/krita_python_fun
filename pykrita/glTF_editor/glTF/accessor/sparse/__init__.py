from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class Sparse(object):
    """
    ...
    """

    def __init__(self,
                indices=None,
                values=None,
                count=None,
                extensions=None,
                extras=None):

        self._indices = Indices()
        self._values = Values()
        self._count = 0
        self._extensions = None
        self._extras = None

        if indices is not None:
            self.indices = indices
        if values is not None:
            self.values = values
        if count is not None:
            self.count = count
        if extensions is not None:
            self.extensions = extensions
        if extras is not None:
            self.extras = extras


    @classmethod
    def cast(cls, obj):
        if isinstance(obj, cls):
            return cls(
                    indices=obj.indices,
                    values=obj.values,
                    count=obj.count,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    indices=obj.get("indices"),
                    values=obj.get("values"),
                    count=obj.get("count"),
                    extensions=obj.get("extensions"),
                    extras=obj.get("extras"))
        elif isinstance(obj, UnicodeType):
            unserialized = serializer.loads(obj)
            if not isinstance(unserialized, UnicodeType):
                return cls.cast(unserialized)
        elif isinstance(obj, Iterable):
            it = iter(obj)
            return cls(
                    indices=next(it),
                    values=next(it),
                    count=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def getIndices(self):
        if self._indices is None:
            return None
        else:
            return iter(self._indices)
    def setIndices(self, newIndices):
        if newIndices is None:
            self._indices = None
        else:
            self._indices = [UnicodeType(n) for n in newIndices]
    indices = property(getIndices, setIndices)


    def getValues(self):
        if self._values is None:
            return None
        else:
            return iter(self._values)
    def setValues(self, newValues):
        if newValues is None:
            self._values = None
        else:
            self._values = [UnicodeType(n) for n in newValues]
    values = property(getValues, setValues)


    def getCount(self):
        if self._count is None:
            return None
        else:
            return iter(self._count)
    def setCount(self, newCount):
        if newCount is None:
            self._count = None
        else:
            self._count = [UnicodeType(n) for n in newCount]
    count = property(getCount, setCount)


    def getExtensions(self):
        if self._extensions is None:
            return None
        else:
            return iter(self._extensions)
    def setExtensions(self, newExtensions):
        if newExtensions is None:
            self._extensions = None
        else:
            self._extensions = [UnicodeType(n) for n in newExtensions]
    extensions = property(getExtensions, setExtensions)


    def getExtras(self):
        if self._extras is None:
            return None
        else:
            return iter(self._extras)
    def setExtras(self, newExtras):
        if newExtras is None:
            self._extras = None
        else:
            self._extras = [UnicodeType(n) for n in newExtras]
    extras = property(getExtras, setExtras)


    def __str__(self):
        return serializer.dumps(self, type_hints=False)


    def __repr__(self):
        cls = type(self)
        return ("{cls.__name__}("
                "indices={self.indices!r}, "
                "values={self.values!r}, "
                "count={self.count!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("indices")
    add_valid("values")
    add_valid("count")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=Sparse,
        from_dict=lambda dct: Sparse.cast(dct),
        to_dict=to_dict)
