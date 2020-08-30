from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class Buffer(object):
    """
    ...
    """

    def __init__(self,
                byteLength=None,
                uri=None,
                name=None,
                extensions=None,
                extras=None):

        self._byteLength = 0
        self._uri = None
        self._name = None
        self._extensions = None
        self._extras = None

        if byteLength is not None:
            self.byteLength = byteLength
        if uri is not None:
            self.uri = uri
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
                    byteLength=obj.byteLength,
                    uri=obj.uri,
                    name=obj.name,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    byteLength=obj.get("byteLength"),
                    uri=obj.get("uri"),
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
                    byteLength=next(it),
                    uri=next(it),
                    name=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


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


    def getUri(self):
        if self._uri is None:
            return None
        else:
            return iter(self._uri)
    def setUri(self, newUri):
        if newUri is None:
            self._uri = None
        else:
            self._uri = [UnicodeType(n) for n in newUri]
    uri = property(getUri, setUri)


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
                "byteLength={self.byteLength!r}, "
                "uri={self.uri!r}, "
                "name={self.name!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("byteLength")
    add_valid("uri")
    add_valid("name")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=Buffer,
        from_dict=lambda dct: Buffer.cast(dct),
        to_dict=to_dict)
