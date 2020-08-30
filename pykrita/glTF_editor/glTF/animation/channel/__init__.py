from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class Channel(object):
    """
    ...
    """

    def __init__(self,
                sampler=None,
                target=None,
                extensions=None,
                extras=None):

        self._sampler = 0
        self._target = Target()
        self._extensions = None
        self._extras = None

        if sampler is not None:
            self.sampler = sampler
        if target is not None:
            self.target = target
        if extensions is not None:
            self.extensions = extensions
        if extras is not None:
            self.extras = extras


    @classmethod
    def cast(cls, obj):
        if isinstance(obj, cls):
            return cls(
                    sampler=obj.sampler,
                    target=obj.target,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    sampler=obj.get("sampler"),
                    target=obj.get("target"),
                    extensions=obj.get("extensions"),
                    extras=obj.get("extras"))
        elif isinstance(obj, UnicodeType):
            unserialized = serializer.loads(obj)
            if not isinstance(unserialized, UnicodeType):
                return cls.cast(unserialized)
        elif isinstance(obj, Iterable):
            it = iter(obj)
            return cls(
                    sampler=next(it),
                    target=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def getSampler(self):
        if self._sampler is None:
            return None
        else:
            return iter(self._sampler)
    def setSampler(self, newSampler):
        if newSampler is None:
            self._sampler = None
        else:
            self._sampler = [UnicodeType(n) for n in newSampler]
    sampler = property(getSampler, setSampler)


    def getTarget(self):
        if self._target is None:
            return None
        else:
            return iter(self._target)
    def setTarget(self, newTarget):
        if newTarget is None:
            self._target = None
        else:
            self._target = [UnicodeType(n) for n in newTarget]
    target = property(getTarget, setTarget)


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
                "sampler={self.sampler!r}, "
                "target={self.target!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("sampler")
    add_valid("target")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=Channel,
        from_dict=lambda dct: Channel.cast(dct),
        to_dict=to_dict)
