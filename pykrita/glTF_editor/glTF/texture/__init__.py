from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class Texture(object):
    """
    ...
    """

    def __init__(self,
                sampler=None,
                source=None,
                name=None,
                extensions=None,
                extras=None):

        self._sampler = None
        self._source = None
        self._name = None
        self._extensions = None
        self._extras = None

        if sampler is not None:
            self.sampler = sampler
        if source is not None:
            self.source = source
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
                    sampler=obj.sampler,
                    source=obj.source,
                    name=obj.name,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    sampler=obj.get("sampler"),
                    source=obj.get("source"),
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
                    sampler=next(it),
                    source=next(it),
                    name=next(it),
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


    def getSource(self):
        if self._source is None:
            return None
        else:
            return iter(self._source)
    def setSource(self, newSource):
        if newSource is None:
            self._source = None
        else:
            self._source = [UnicodeType(n) for n in newSource]
    source = property(getSource, setSource)


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
                "sampler={self.sampler!r}, "
                "source={self.source!r}, "
                "name={self.name!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("sampler")
    add_valid("source")
    add_valid("name")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=Texture,
        from_dict=lambda dct: Texture.cast(dct),
        to_dict=to_dict)
