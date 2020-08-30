from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class PbrMetallicRoughness(object):
    """
    ...
    """

    def __init__(self,
                baseColorFactor=None,
                metallicFactor=None,
                roughnessFactor=None,
                baseColorTexture=None,
                metallicRoughnessTexture=None,
                extensions=None,
                extras=None):

        self._baseColorFactor = Color(1.0, 1.0, 1.0)
        self._metallicFactor = 1.0
        self._roughnessFactor = 1.0
        self._baseColorTexture = None
        self._metallicRoughnessTexture = None
        self._extensions = None
        self._extras = None

        if baseColorFactor is not None:
            self.baseColorFactor = baseColorFactor
        if metallicFactor is not None:
            self.metallicFactor = metallicFactor
        if roughnessFactor is not None:
            self.roughnessFactor = roughnessFactor
        if baseColorTexture is not None:
            self.baseColorTexture = baseColorTexture
        if metallicRoughnessTexture is not None:
            self.metallicRoughnessTexture = metallicRoughnessTexture
        if extensions is not None:
            self.extensions = extensions
        if extras is not None:
            self.extras = extras


    @classmethod
    def cast(cls, obj):
        if isinstance(obj, cls):
            return cls(
                    baseColorFactor=obj.baseColorFactor,
                    metallicFactor=obj.metallicFactor,
                    roughnessFactor=obj.roughnessFactor,
                    baseColorTexture=obj.baseColorTexture,
                    metallicRoughnessTexture=obj.metallicRoughnessTexture,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    baseColorFactor=obj.get("baseColorFactor"),
                    metallicFactor=obj.get("metallicFactor"),
                    roughnessFactor=obj.get("roughnessFactor"),
                    baseColorTexture=obj.get("baseColorTexture"),
                    metallicRoughnessTexture=obj.get("metallicRoughnessTexture"),
                    extensions=obj.get("extensions"),
                    extras=obj.get("extras"))
        elif isinstance(obj, UnicodeType):
            unserialized = serializer.loads(obj)
            if not isinstance(unserialized, UnicodeType):
                return cls.cast(unserialized)
        elif isinstance(obj, Iterable):
            it = iter(obj)
            return cls(
                    baseColorFactor=next(it),
                    metallicFactor=next(it),
                    roughnessFactor=next(it),
                    baseColorTexture=next(it),
                    metallicRoughnessTexture=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def getBaseColorFactor(self):
        if self._baseColorFactor is None:
            return None
        else:
            return iter(self._baseColorFactor)
    def setBaseColorFactor(self, newBaseColorFactor):
        if newBaseColorFactor is None:
            self._baseColorFactor = None
        else:
            self._baseColorFactor = [UnicodeType(n) for n in newBaseColorFactor]
    baseColorFactor = property(getBaseColorFactor, setBaseColorFactor)


    def getMetallicFactor(self):
        if self._metallicFactor is None:
            return None
        else:
            return iter(self._metallicFactor)
    def setMetallicFactor(self, newMetallicFactor):
        if newMetallicFactor is None:
            self._metallicFactor = None
        else:
            self._metallicFactor = [UnicodeType(n) for n in newMetallicFactor]
    metallicFactor = property(getMetallicFactor, setMetallicFactor)


    def getRoughnessFactor(self):
        if self._roughnessFactor is None:
            return None
        else:
            return iter(self._roughnessFactor)
    def setRoughnessFactor(self, newRoughnessFactor):
        if newRoughnessFactor is None:
            self._roughnessFactor = None
        else:
            self._roughnessFactor = [UnicodeType(n) for n in newRoughnessFactor]
    roughnessFactor = property(getRoughnessFactor, setRoughnessFactor)


    def getBaseColorTexture(self):
        if self._baseColorTexture is None:
            return None
        else:
            return iter(self._baseColorTexture)
    def setBaseColorTexture(self, newBaseColorTexture):
        if newBaseColorTexture is None:
            self._baseColorTexture = None
        else:
            self._baseColorTexture = [UnicodeType(n) for n in newBaseColorTexture]
    baseColorTexture = property(getBaseColorTexture, setBaseColorTexture)


    def getMetallicRoughnessTexture(self):
        if self._metallicRoughnessTexture is None:
            return None
        else:
            return iter(self._metallicRoughnessTexture)
    def setMetallicRoughnessTexture(self, newMetallicRoughnessTexture):
        if newMetallicRoughnessTexture is None:
            self._metallicRoughnessTexture = None
        else:
            self._metallicRoughnessTexture = [UnicodeType(n) for n in newMetallicRoughnessTexture]
    metallicRoughnessTexture = property(getMetallicRoughnessTexture, setMetallicRoughnessTexture)


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
                "baseColorFactor={self.baseColorFactor!r}, "
                "metallicFactor={self.metallicFactor!r}, "
                "roughnessFactor={self.roughnessFactor!r}, "
                "baseColorTexture={self.baseColorTexture!r}, "
                "metallicRoughnessTexture={self.metallicRoughnessTexture!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("baseColorFactor")
    add_valid("metallicFactor")
    add_valid("roughnessFactor")
    add_valid("baseColorTexture")
    add_valid("metallicRoughnessTexture")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=PbrMetallicRoughness,
        from_dict=lambda dct: PbrMetallicRoughness.cast(dct),
        to_dict=to_dict)
