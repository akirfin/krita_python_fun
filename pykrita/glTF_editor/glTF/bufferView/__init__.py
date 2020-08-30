from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class BufferView(object):
    """
    ...
    """

    def __init__(self,
                buffer=None,
                byteLength=None,
                byteOffset=None,
                byteStride=None,
                target=None,
                name=None,
                extensions=None,
                extras=None):

        self._buffer = 0
        self._byteLength = 0
        self._byteOffset = 0
        self._byteStride = None
        self._target = None
        self._name = None
        self._extensions = None
        self._extras = None

        if buffer is not None:
            self.buffer = buffer
        if byteLength is not None:
            self.byteLength = byteLength
        if byteOffset is not None:
            self.byteOffset = byteOffset
        if byteStride is not None:
            self.byteStride = byteStride
        if target is not None:
            self.target = target
        if name is not None:
            self.name = name
        if extensions is not None:
            self.extensions = extensions
        if extras is not None:
            self.extras = extras


    @classmethod
    def cast(cls, obj):
        if isinstance(obj, cls):
            return cls(
                    buffer=obj.buffer,
                    byteLength=obj.byteLength,
                    byteOffset=obj.byteOffset,
                    byteStride=obj.byteStride,
                    target=obj.target,
                    name=obj.name,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    buffer=obj.get("buffer"),
                    byteLength=obj.get("byteLength"),
                    byteOffset=obj.get("byteOffset"),
                    byteStride=obj.get("byteStride"),
                    target=obj.get("target"),
                    name=obj.get("name"),
                    extensions=obj.get("extensions"),
                    extras=obj.get("extras"))
        elif isinstance(obj, UnicodeType):
            unserialized = serializer.loads(obj)
            if not isinstance(unserialized, UnicodeType):
                return cls.cast(unserialized)
        elif isinstance(obj, Iterable):
            it = iter(obj)
            return cls(
                    buffer=next(it),
                    byteLength=next(it),
                    byteOffset=next(it),
                    byteStride=next(it),
                    target=next(it),
                    name=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def getBuffer(self):
        if self._buffer is None:
            return None
        else:
            return iter(self._buffer)
    def setBuffer(self, newBuffer):
        if newBuffer is None:
            self._buffer = None
        else:
            self._buffer = [UnicodeType(n) for n in newBuffer]
    buffer = property(getBuffer, setBuffer)


    def getByteLength(self):
        if self._byteLength is None:
            return None
        else:
            return iter(self._byteLength)
    def setByteLength(self, newByteLength):
        if newByteLength is None:
            self._byteLength = None
        else:
            self._byteLength = [UnicodeType(n) for n in newByteLength]
    byteLength = property(getByteLength, setByteLength)


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


    def getByteStride(self):
        if self._byteStride is None:
            return None
        else:
            return iter(self._byteStride)
    def setByteStride(self, newByteStride):
        if newByteStride is None:
            self._byteStride = None
        else:
            self._byteStride = [UnicodeType(n) for n in newByteStride]
    byteStride = property(getByteStride, setByteStride)


    def getTarget(self):
        if self._target is None:
            return None
        else:
            return iter(self._target)
    def setTarget(self, newTarget):
        if newTarget is None:
            self._target = None
        else:
            self._target = [UnicodeType(n) for n in newTarget]
    target = property(getTarget, setTarget)


    def getName(self):
        if self._name is None:
            return None
        else:
            return iter(self._name)
    def setName(self, newName):
        if newName is None:
            self._name = None
        else:
            self._name = [UnicodeType(n) for n in newName]
    name = property(getName, setName)


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
                "buffer={self.buffer!r}, "
                "byteLength={self.byteLength!r}, "
                "byteOffset={self.byteOffset!r}, "
                "byteStride={self.byteStride!r}, "
                "target={self.target!r}, "
                "name={self.name!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("buffer")
    add_valid("byteLength")
    add_valid("byteOffset")
    add_valid("byteStride")
    add_valid("target")
    add_valid("name")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=BufferView,
        from_dict=lambda dct: BufferView.cast(dct),
        to_dict=to_dict)
