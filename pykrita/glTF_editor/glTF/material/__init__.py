from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class Material(object):
    """
    ...
    """

    def __init__(self,
                emissiveFactor=None,
                alphaMode=None,
                alphaCutoff=None,
                doubleSided=None,
                pbrMetallicRoughness=None,
                normalTexture=None,
                occlusionTexture=None,
                emissiveTexture=None,
                name=None,
                extensions=None,
                extras=None):

        self._emissiveFactor = Color(0.0, 0.0, 0.0)
        self._alphaMode = AlphaMode.OPAQUE
        self._alphaCutoff = 0.5
        self._doubleSided = False
        self._pbrMetallicRoughness = None
        self._normalTexture = None
        self._occlusionTexture = None
        self._emissiveTexture = None
        self._name = None
        self._extensions = None
        self._extras = None

        if emissiveFactor is not None:
            self.emissiveFactor = emissiveFactor
        if alphaMode is not None:
            self.alphaMode = alphaMode
        if alphaCutoff is not None:
            self.alphaCutoff = alphaCutoff
        if doubleSided is not None:
            self.doubleSided = doubleSided
        if pbrMetallicRoughness is not None:
            self.pbrMetallicRoughness = pbrMetallicRoughness
        if normalTexture is not None:
            self.normalTexture = normalTexture
        if occlusionTexture is not None:
            self.occlusionTexture = occlusionTexture
        if emissiveTexture is not None:
            self.emissiveTexture = emissiveTexture
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
                    emissiveFactor=obj.emissiveFactor,
                    alphaMode=obj.alphaMode,
                    alphaCutoff=obj.alphaCutoff,
                    doubleSided=obj.doubleSided,
                    pbrMetallicRoughness=obj.pbrMetallicRoughness,
                    normalTexture=obj.normalTexture,
                    occlusionTexture=obj.occlusionTexture,
                    emissiveTexture=obj.emissiveTexture,
                    name=obj.name,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    emissiveFactor=obj.get("emissiveFactor"),
                    alphaMode=obj.get("alphaMode"),
                    alphaCutoff=obj.get("alphaCutoff"),
                    doubleSided=obj.get("doubleSided"),
                    pbrMetallicRoughness=obj.get("pbrMetallicRoughness"),
                    normalTexture=obj.get("normalTexture"),
                    occlusionTexture=obj.get("occlusionTexture"),
                    emissiveTexture=obj.get("emissiveTexture"),
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
                    emissiveFactor=next(it),
                    alphaMode=next(it),
                    alphaCutoff=next(it),
                    doubleSided=next(it),
                    pbrMetallicRoughness=next(it),
                    normalTexture=next(it),
                    occlusionTexture=next(it),
                    emissiveTexture=next(it),
                    name=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def getEmissiveFactor(self):
        if self._emissiveFactor is None:
            return None
        else:
            return iter(self._emissiveFactor)
    def setEmissiveFactor(self, newEmissiveFactor):
        if newEmissiveFactor is None:
            self._emissiveFactor = None
        else:
            self._emissiveFactor = [UnicodeType(n) for n in newEmissiveFactor]
    emissiveFactor = property(getEmissiveFactor, setEmissiveFactor)


    def getAlphaMode(self):
        if self._alphaMode is None:
            return None
        else:
            return iter(self._alphaMode)
    def setAlphaMode(self, newAlphaMode):
        if newAlphaMode is None:
            self._alphaMode = None
        else:
            self._alphaMode = [UnicodeType(n) for n in newAlphaMode]
    alphaMode = property(getAlphaMode, setAlphaMode)


    def getAlphaCutoff(self):
        if self._alphaCutoff is None:
            return None
        else:
            return iter(self._alphaCutoff)
    def setAlphaCutoff(self, newAlphaCutoff):
        if newAlphaCutoff is None:
            self._alphaCutoff = None
        else:
            self._alphaCutoff = [UnicodeType(n) for n in newAlphaCutoff]
    alphaCutoff = property(getAlphaCutoff, setAlphaCutoff)


    def getDoubleSided(self):
        if self._doubleSided is None:
            return None
        else:
            return iter(self._doubleSided)
    def setDoubleSided(self, newDoubleSided):
        if newDoubleSided is None:
            self._doubleSided = None
        else:
            self._doubleSided = [UnicodeType(n) for n in newDoubleSided]
    doubleSided = property(getDoubleSided, setDoubleSided)


    def getPbrMetallicRoughness(self):
        if self._pbrMetallicRoughness is None:
            return None
        else:
            return iter(self._pbrMetallicRoughness)
    def setPbrMetallicRoughness(self, newPbrMetallicRoughness):
        if newPbrMetallicRoughness is None:
            self._pbrMetallicRoughness = None
        else:
            self._pbrMetallicRoughness = [UnicodeType(n) for n in newPbrMetallicRoughness]
    pbrMetallicRoughness = property(getPbrMetallicRoughness, setPbrMetallicRoughness)


    def getNormalTexture(self):
        if self._normalTexture is None:
            return None
        else:
            return iter(self._normalTexture)
    def setNormalTexture(self, newNormalTexture):
        if newNormalTexture is None:
            self._normalTexture = None
        else:
            self._normalTexture = [UnicodeType(n) for n in newNormalTexture]
    normalTexture = property(getNormalTexture, setNormalTexture)


    def getOcclusionTexture(self):
        if self._occlusionTexture is None:
            return None
        else:
            return iter(self._occlusionTexture)
    def setOcclusionTexture(self, newOcclusionTexture):
        if newOcclusionTexture is None:
            self._occlusionTexture = None
        else:
            self._occlusionTexture = [UnicodeType(n) for n in newOcclusionTexture]
    occlusionTexture = property(getOcclusionTexture, setOcclusionTexture)


    def getEmissiveTexture(self):
        if self._emissiveTexture is None:
            return None
        else:
            return iter(self._emissiveTexture)
    def setEmissiveTexture(self, newEmissiveTexture):
        if newEmissiveTexture is None:
            self._emissiveTexture = None
        else:
            self._emissiveTexture = [UnicodeType(n) for n in newEmissiveTexture]
    emissiveTexture = property(getEmissiveTexture, setEmissiveTexture)


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
                "emissiveFactor={self.emissiveFactor!r}, "
                "alphaMode={self.alphaMode!r}, "
                "alphaCutoff={self.alphaCutoff!r}, "
                "doubleSided={self.doubleSided!r}, "
                "pbrMetallicRoughness={self.pbrMetallicRoughness!r}, "
                "normalTexture={self.normalTexture!r}, "
                "occlusionTexture={self.occlusionTexture!r}, "
                "emissiveTexture={self.emissiveTexture!r}, "
                "name={self.name!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("emissiveFactor")
    add_valid("alphaMode")
    add_valid("alphaCutoff")
    add_valid("doubleSided")
    add_valid("pbrMetallicRoughness")
    add_valid("normalTexture")
    add_valid("occlusionTexture")
    add_valid("emissiveTexture")
    add_valid("name")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=Material,
        from_dict=lambda dct: Material.cast(dct),
        to_dict=to_dict)
