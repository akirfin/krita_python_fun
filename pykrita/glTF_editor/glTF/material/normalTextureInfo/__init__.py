from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class NormalTextureInfo(object):
    """
    ...
    """

    def __init__(self,
                index=None,
                texCoord=None,
                scale=None,
                extensions=None,
                extras=None):

        self._index = 0
        self._texCoord = 0
        self._scale = 1.0
        self._extensions = None
        self._extras = None

        if index is not None:
            self.index = index
        if texCoord is not None:
            self.texCoord = texCoord
        if scale is not None:
            self.scale = scale
        if extensions is not None:
            self.extensions = extensions
        if extras is not None:
            self.extras = extras


    @classmethod
    def cast(cls, obj):
        if isinstance(obj, cls):
            return cls(
                    index=obj.index,
                    texCoord=obj.texCoord,
                    scale=obj.scale,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    index=obj.get("index"),
                    texCoord=obj.get("texCoord"),
                    scale=obj.get("scale"),
                    extensions=obj.get("extensions"),
                    extras=obj.get("extras"))
        elif isinstance(obj, UnicodeType):
            unserialized = serializer.loads(obj)
            if not isinstance(unserialized, UnicodeType):
                return cls.cast(unserialized)
        elif isinstance(obj, Iterable):
            it = iter(obj)
            return cls(
                    index=next(it),
                    texCoord=next(it),
                    scale=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def getIndex(self):
        if self._index is None:
            return None
        else:
            return iter(self._index)
    def setIndex(self, newIndex):
        if newIndex is None:
            self._index = None
        else:
            self._index = [UnicodeType(n) for n in newIndex]
    index = property(getIndex, setIndex)


    def getTexCoord(self):
        if self._texCoord is None:
            return None
        else:
            return iter(self._texCoord)
    def setTexCoord(self, newTexCoord):
        if newTexCoord is None:
            self._texCoord = None
        else:
            self._texCoord = [UnicodeType(n) for n in newTexCoord]
    texCoord = property(getTexCoord, setTexCoord)


    def getScale(self):
        if self._scale is None:
            return None
        else:
            return iter(self._scale)
    def setScale(self, newScale):
        if newScale is None:
            self._scale = None
        else:
            self._scale = [UnicodeType(n) for n in newScale]
    scale = property(getScale, setScale)


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
                "index={self.index!r}, "
                "texCoord={self.texCoord!r}, "
                "scale={self.scale!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("index")
    add_valid("texCoord")
    add_valid("scale")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=NormalTextureInfo,
        from_dict=lambda dct: NormalTextureInfo.cast(dct),
        to_dict=to_dict)
