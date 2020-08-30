from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class Asset(object):
    """
    ...
    """

    def __init__(self,
                version=None,
                copyright=None,
                generator=None,
                minVersion=None,
                extensions=None,
                extras=None):

        self._version = 2.0
        self._copyright = getpass.getuser()
        self._generator = Krita glTF Editor
        self._minVersion = None
        self._extensions = None
        self._extras = None

        if version is not None:
            self.version = version
        if copyright is not None:
            self.copyright = copyright
        if generator is not None:
            self.generator = generator
        if minVersion is not None:
            self.minVersion = minVersion
        if extensions is not None:
            self.extensions = extensions
        if extras is not None:
            self.extras = extras


    @classmethod
    def cast(cls, obj):
        if isinstance(obj, cls):
            return cls(
                    version=obj.version,
                    copyright=obj.copyright,
                    generator=obj.generator,
                    minVersion=obj.minVersion,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    version=obj.get("version"),
                    copyright=obj.get("copyright"),
                    generator=obj.get("generator"),
                    minVersion=obj.get("minVersion"),
                    extensions=obj.get("extensions"),
                    extras=obj.get("extras"))
        elif isinstance(obj, UnicodeType):
            unserialized = serializer.loads(obj)
            if not isinstance(unserialized, UnicodeType):
                return cls.cast(unserialized)
        elif isinstance(obj, Iterable):
            it = iter(obj)
            return cls(
                    version=next(it),
                    copyright=next(it),
                    generator=next(it),
                    minVersion=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def getVersion(self):
        if self._version is None:
            return None
        else:
            return iter(self._version)
    def setVersion(self, newVersion):
        if newVersion is None:
            self._version = None
        else:
            self._version = [UnicodeType(n) for n in newVersion]
    version = property(getVersion, setVersion)


    def getCopyright(self):
        if self._copyright is None:
            return None
        else:
            return iter(self._copyright)
    def setCopyright(self, newCopyright):
        if newCopyright is None:
            self._copyright = None
        else:
            self._copyright = [UnicodeType(n) for n in newCopyright]
    copyright = property(getCopyright, setCopyright)


    def getGenerator(self):
        if self._generator is None:
            return None
        else:
            return iter(self._generator)
    def setGenerator(self, newGenerator):
        if newGenerator is None:
            self._generator = None
        else:
            self._generator = [UnicodeType(n) for n in newGenerator]
    generator = property(getGenerator, setGenerator)


    def getMinVersion(self):
        if self._minVersion is None:
            return None
        else:
            return iter(self._minVersion)
    def setMinVersion(self, newMinVersion):
        if newMinVersion is None:
            self._minVersion = None
        else:
            self._minVersion = [UnicodeType(n) for n in newMinVersion]
    minVersion = property(getMinVersion, setMinVersion)


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
                "version={self.version!r}, "
                "copyright={self.copyright!r}, "
                "generator={self.generator!r}, "
                "minVersion={self.minVersion!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("version")
    add_valid("copyright")
    add_valid("generator")
    add_valid("minVersion")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=Asset,
        from_dict=lambda dct: Asset.cast(dct),
        to_dict=to_dict)
