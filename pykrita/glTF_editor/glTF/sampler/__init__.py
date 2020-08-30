from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class Sampler(object):
    """
    ...
    """

    def __init__(self,
                wrapS=None,
                wrapT=None,
                magFilter=None,
                minFilter=None,
                name=None,
                extensions=None,
                extras=None):

        self._wrapS = WarpingMode.REPEAT
        self._wrapT = WarpingMode.REPEAT
        self._magFilter = MagnificationFilter.LINEAR
        self._minFilter = MinificationFilter.LINEAR
        self._name = None
        self._extensions = None
        self._extras = None

        if wrapS is not None:
            self.wrapS = wrapS
        if wrapT is not None:
            self.wrapT = wrapT
        if magFilter is not None:
            self.magFilter = magFilter
        if minFilter is not None:
            self.minFilter = minFilter
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
                    wrapS=obj.wrapS,
                    wrapT=obj.wrapT,
                    magFilter=obj.magFilter,
                    minFilter=obj.minFilter,
                    name=obj.name,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    wrapS=obj.get("wrapS"),
                    wrapT=obj.get("wrapT"),
                    magFilter=obj.get("magFilter"),
                    minFilter=obj.get("minFilter"),
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
                    wrapS=next(it),
                    wrapT=next(it),
                    magFilter=next(it),
                    minFilter=next(it),
                    name=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def getWrapS(self):
        if self._wrapS is None:
            return None
        else:
            return iter(self._wrapS)
    def setWrapS(self, newWrapS):
        if newWrapS is None:
            self._wrapS = None
        else:
            self._wrapS = [UnicodeType(n) for n in newWrapS]
    wrapS = property(getWrapS, setWrapS)


    def getWrapT(self):
        if self._wrapT is None:
            return None
        else:
            return iter(self._wrapT)
    def setWrapT(self, newWrapT):
        if newWrapT is None:
            self._wrapT = None
        else:
            self._wrapT = [UnicodeType(n) for n in newWrapT]
    wrapT = property(getWrapT, setWrapT)


    def getMagFilter(self):
        if self._magFilter is None:
            return None
        else:
            return iter(self._magFilter)
    def setMagFilter(self, newMagFilter):
        if newMagFilter is None:
            self._magFilter = None
        else:
            self._magFilter = [UnicodeType(n) for n in newMagFilter]
    magFilter = property(getMagFilter, setMagFilter)


    def getMinFilter(self):
        if self._minFilter is None:
            return None
        else:
            return iter(self._minFilter)
    def setMinFilter(self, newMinFilter):
        if newMinFilter is None:
            self._minFilter = None
        else:
            self._minFilter = [UnicodeType(n) for n in newMinFilter]
    minFilter = property(getMinFilter, setMinFilter)


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
                "wrapS={self.wrapS!r}, "
                "wrapT={self.wrapT!r}, "
                "magFilter={self.magFilter!r}, "
                "minFilter={self.minFilter!r}, "
                "name={self.name!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("wrapS")
    add_valid("wrapT")
    add_valid("magFilter")
    add_valid("minFilter")
    add_valid("name")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=Sampler,
        from_dict=lambda dct: Sampler.cast(dct),
        to_dict=to_dict)
