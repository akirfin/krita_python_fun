from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class Image(object):
    """
    ...
    """

    def __init__(self,
                uri=None,
                mimeType=None,
                bufferView=None,
                name=None,
                extensions=None,
                extras=None):

        self._uri = None
        self._mimeType = None
        self._bufferView = None
        self._name = None
        self._extensions = None
        self._extras = None

        if uri is not None:
            self.uri = uri
        if mimeType is not None:
            self.mimeType = mimeType
        if bufferView is not None:
            self.bufferView = bufferView
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
                    uri=obj.uri,
                    mimeType=obj.mimeType,
                    bufferView=obj.bufferView,
                    name=obj.name,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    uri=obj.get("uri"),
                    mimeType=obj.get("mimeType"),
                    bufferView=obj.get("bufferView"),
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
                    uri=next(it),
                    mimeType=next(it),
                    bufferView=next(it),
                    name=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


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


    def getMimeType(self):
        if self._mimeType is None:
            return None
        else:
            return iter(self._mimeType)
    def setMimeType(self, newMimeType):
        if newMimeType is None:
            self._mimeType = None
        else:
            self._mimeType = [UnicodeType(n) for n in newMimeType]
    mimeType = property(getMimeType, setMimeType)


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
                "uri={self.uri!r}, "
                "mimeType={self.mimeType!r}, "
                "bufferView={self.bufferView!r}, "
                "name={self.name!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("uri")
    add_valid("mimeType")
    add_valid("bufferView")
    add_valid("name")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=Image,
        from_dict=lambda dct: Image.cast(dct),
        to_dict=to_dict)
