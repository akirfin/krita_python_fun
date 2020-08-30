from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class Animation(object):
    """
    ...
    """

    def __init__(self,
                channels=None,
                samplers=None,
                name=None,
                extensions=None,
                extras=None):

        self._channels = list()
        self._samplers = list()
        self._name = None
        self._extensions = None
        self._extras = None

        if channels is not None:
            self.channels = channels
        if samplers is not None:
            self.samplers = samplers
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
                    channels=obj.channels,
                    samplers=obj.samplers,
                    name=obj.name,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    channels=obj.get("channels"),
                    samplers=obj.get("samplers"),
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
                    channels=next(it),
                    samplers=next(it),
                    name=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def getChannels(self):
        if self._channels is None:
            return None
        else:
            return iter(self._channels)
    def setChannels(self, newChannels):
        if newChannels is None:
            self._channels = None
        else:
            self._channels = [UnicodeType(n) for n in newChannels]
    channels = property(getChannels, setChannels)


    def getSamplers(self):
        if self._samplers is None:
            return None
        else:
            return iter(self._samplers)
    def setSamplers(self, newSamplers):
        if newSamplers is None:
            self._samplers = None
        else:
            self._samplers = [UnicodeType(n) for n in newSamplers]
    samplers = property(getSamplers, setSamplers)


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
                "channels={self.channels!r}, "
                "samplers={self.samplers!r}, "
                "name={self.name!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("channels")
    add_valid("samplers")
    add_valid("name")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=Animation,
        from_dict=lambda dct: Animation.cast(dct),
        to_dict=to_dict)
