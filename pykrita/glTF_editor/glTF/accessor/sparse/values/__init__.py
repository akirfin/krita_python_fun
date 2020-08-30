from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class Values(object):
    """
    ...
    """

    def __init__(self,
                bufferView=None,
                byteOffset=None,
                extensions=None,
                extras=None):

        self._bufferView = 0
        self._byteOffset = 0
        self._extensions = None
        self._extras = None

        if bufferView is not None:
            self.bufferView = bufferView
        if byteOffset is not None:
            self.byteOffset = byteOffset
        if extensions is not None:
            self.extensions = extensions
        if extras is not None:
            self.extras = extras


    @classmethod
    def cast(cls, obj):
        if isinstance(obj, cls):
            return cls(
                    bufferView=obj.bufferView,
                    byteOffset=obj.byteOffset,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    bufferView=obj.get("bufferView"),
                    byteOffset=obj.get("byteOffset"),
                    extensions=obj.get("extensions"),
                    extras=obj.get("extras"))
        elif isinstance(obj, UnicodeType):
            unserialized = serializer.loads(obj)
            if not isinstance(unserialized, UnicodeType):
                return cls.cast(unserialized)
        elif isinstance(obj, Iterable):
            it = iter(obj)
            return cls(
                    bufferView=next(it),
                    byteOffset=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def getBufferView(self):
        if self._bufferView is None:
            return None
        else:
            return iter(self._bufferView)
    def setBufferView(self, newBufferView):
        if newBufferView is None:
            self._bufferView = None
        else:
            self._bufferView = [UnicodeType(n) for n in newBufferView]
    bufferView = property(getBufferView, setBufferView)


    def getByteOffset(self):
        if self._byteOffset is None:
            return None
        else:
            return iter(self._byteOffset)
    def setByteOffset(self, newByteOffset):
        if newByteOffset is None:
            self._byteOffset = None
        else:
            self._byteOffset = [UnicodeType(n) for n in newByteOffset]
    byteOffset = property(getByteOffset, setByteOffset)


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
                "bufferView={self.bufferView!r}, "
                "byteOffset={self.byteOffset!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("bufferView")
    add_valid("byteOffset")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=Values,
        from_dict=lambda dct: Values.cast(dct),
        to_dict=to_dict)
