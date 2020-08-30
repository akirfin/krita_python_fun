from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class Light(object):
    """
    ...
    """

    def __init__(self,
                type=None,
                color=None,
                intensity=None,
                name=None,
                spot=None,
                range=None,
                extensions=None,
                extras=None):

        self._type = LightType.DIRECTIONAL
        self._color = Color(1.0, 1.0, 1.0)
        self._intensity = 1.0
        self._name = None
        self._spot = None
        self._range = None
        self._extensions = None
        self._extras = None

        if type is not None:
            self.type = type
        if color is not None:
            self.color = color
        if intensity is not None:
            self.intensity = intensity
        if name is not None:
            self.name = name
        if spot is not None:
            self.spot = spot
        if range is not None:
            self.range = range
        if extensions is not None:
            self.extensions = extensions
        if extras is not None:
            self.extras = extras


    @classmethod
    def cast(cls, obj):
        if isinstance(obj, cls):
            return cls(
                    type=obj.type,
                    color=obj.color,
                    intensity=obj.intensity,
                    name=obj.name,
                    spot=obj.spot,
                    range=obj.range,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    type=obj.get("type"),
                    color=obj.get("color"),
                    intensity=obj.get("intensity"),
                    name=obj.get("name"),
                    spot=obj.get("spot"),
                    range=obj.get("range"),
                    extensions=obj.get("extensions"),
                    extras=obj.get("extras"))
        elif isinstance(obj, UnicodeType):
            unserialized = serializer.loads(obj)
            if not isinstance(unserialized, UnicodeType):
                return cls.cast(unserialized)
        elif isinstance(obj, Iterable):
            it = iter(obj)
            return cls(
                    type=next(it),
                    color=next(it),
                    intensity=next(it),
                    name=next(it),
                    spot=next(it),
                    range=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def getType(self):
        if self._type is None:
            return None
        else:
            return iter(self._type)
    def setType(self, newType):
        if newType is None:
            self._type = None
        else:
            self._type = [UnicodeType(n) for n in newType]
    type = property(getType, setType)


    def getColor(self):
        if self._color is None:
            return None
        else:
            return iter(self._color)
    def setColor(self, newColor):
        if newColor is None:
            self._color = None
        else:
            self._color = [UnicodeType(n) for n in newColor]
    color = property(getColor, setColor)


    def getIntensity(self):
        if self._intensity is None:
            return None
        else:
            return iter(self._intensity)
    def setIntensity(self, newIntensity):
        if newIntensity is None:
            self._intensity = None
        else:
            self._intensity = [UnicodeType(n) for n in newIntensity]
    intensity = property(getIntensity, setIntensity)


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


    def getSpot(self):
        if self._spot is None:
            return None
        else:
            return iter(self._spot)
    def setSpot(self, newSpot):
        if newSpot is None:
            self._spot = None
        else:
            self._spot = [UnicodeType(n) for n in newSpot]
    spot = property(getSpot, setSpot)


    def getRange(self):
        if self._range is None:
            return None
        else:
            return iter(self._range)
    def setRange(self, newRange):
        if newRange is None:
            self._range = None
        else:
            self._range = [UnicodeType(n) for n in newRange]
    range = property(getRange, setRange)


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
                "type={self.type!r}, "
                "color={self.color!r}, "
                "intensity={self.intensity!r}, "
                "name={self.name!r}, "
                "spot={self.spot!r}, "
                "range={self.range!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("type")
    add_valid("color")
    add_valid("intensity")
    add_valid("name")
    add_valid("spot")
    add_valid("range")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=Light,
        from_dict=lambda dct: Light.cast(dct),
        to_dict=to_dict)
