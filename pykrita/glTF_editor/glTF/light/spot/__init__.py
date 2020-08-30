from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class Spot(object):
    """
    ...
    """

    def __init__(self,
                innerConeAngle=None,
                outerConeAngle=None,
                extensions=None,
                extras=None):

        self._innerConeAngle = 0.0
        self._outerConeAngle = 0.25 * math.pi
        self._extensions = None
        self._extras = None

        if innerConeAngle is not None:
            self.innerConeAngle = innerConeAngle
        if outerConeAngle is not None:
            self.outerConeAngle = outerConeAngle
        if extensions is not None:
            self.extensions = extensions
        if extras is not None:
            self.extras = extras


    @classmethod
    def cast(cls, obj):
        if isinstance(obj, cls):
            return cls(
                    innerConeAngle=obj.innerConeAngle,
                    outerConeAngle=obj.outerConeAngle,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    innerConeAngle=obj.get("innerConeAngle"),
                    outerConeAngle=obj.get("outerConeAngle"),
                    extensions=obj.get("extensions"),
                    extras=obj.get("extras"))
        elif isinstance(obj, UnicodeType):
            unserialized = serializer.loads(obj)
            if not isinstance(unserialized, UnicodeType):
                return cls.cast(unserialized)
        elif isinstance(obj, Iterable):
            it = iter(obj)
            return cls(
                    innerConeAngle=next(it),
                    outerConeAngle=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def getInnerConeAngle(self):
        if self._innerConeAngle is None:
            return None
        else:
            return iter(self._innerConeAngle)
    def setInnerConeAngle(self, newInnerConeAngle):
        if newInnerConeAngle is None:
            self._innerConeAngle = None
        else:
            self._innerConeAngle = [UnicodeType(n) for n in newInnerConeAngle]
    innerConeAngle = property(getInnerConeAngle, setInnerConeAngle)


    def getOuterConeAngle(self):
        if self._outerConeAngle is None:
            return None
        else:
            return iter(self._outerConeAngle)
    def setOuterConeAngle(self, newOuterConeAngle):
        if newOuterConeAngle is None:
            self._outerConeAngle = None
        else:
            self._outerConeAngle = [UnicodeType(n) for n in newOuterConeAngle]
    outerConeAngle = property(getOuterConeAngle, setOuterConeAngle)


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
                "innerConeAngle={self.innerConeAngle!r}, "
                "outerConeAngle={self.outerConeAngle!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("innerConeAngle")
    add_valid("outerConeAngle")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=Spot,
        from_dict=lambda dct: Spot.cast(dct),
        to_dict=to_dict)
