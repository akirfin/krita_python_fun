from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class Mesh(object):
    """
    ...
    """

    def __init__(self,
                primitives=None,
                weights=None,
                name=None,
                extensions=None,
                extras=None):

        self._primitives = list()
        self._weights = None
        self._name = None
        self._extensions = None
        self._extras = None

        if primitives is not None:
            self.primitives = primitives
        if weights is not None:
            self.weights = weights
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
                    primitives=obj.primitives,
                    weights=obj.weights,
                    name=obj.name,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    primitives=obj.get("primitives"),
                    weights=obj.get("weights"),
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
                    primitives=next(it),
                    weights=next(it),
                    name=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def getPrimitives(self):
        if self._primitives is None:
            return None
        else:
            return iter(self._primitives)
    def setPrimitives(self, newPrimitives):
        if newPrimitives is None:
            self._primitives = None
        else:
            self._primitives = [UnicodeType(n) for n in newPrimitives]
    primitives = property(getPrimitives, setPrimitives)


    def getWeights(self):
        if self._weights is None:
            return None
        else:
            return iter(self._weights)
    def setWeights(self, newWeights):
        if newWeights is None:
            self._weights = None
        else:
            self._weights = [UnicodeType(n) for n in newWeights]
    weights = property(getWeights, setWeights)


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
                "primitives={self.primitives!r}, "
                "weights={self.weights!r}, "
                "name={self.name!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("primitives")
    add_valid("weights")
    add_valid("name")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=Mesh,
        from_dict=lambda dct: Mesh.cast(dct),
        to_dict=to_dict)
