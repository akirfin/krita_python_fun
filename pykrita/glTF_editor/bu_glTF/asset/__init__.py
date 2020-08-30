from getpass import getuser

from glTF_editor.common.data_serializer import \
        serializer


class Asset(object):
    def __init__(self,
                version=None,
                minVersion=None,
                generator=None,
                copyright=None,
                extensions=None,
                extras=None):

        self._version = "2.0"
        self._minVersion = None
        self._generator = "Krita glTF Editor Extension"
        self._copyright = getuser()
        self._extensions = None
        self._extras = None

        if version is not None:
            self.version = version
        if minVersion is not None:
            self.minVersion = minVersion
        if generator is not None:
            self.generator = generator
        if copyright is not None:
            self.copyright = copyright
        if extensions is not None:
            self.extensions = extensions
        if extras is not None:
            self.extras = extras


    @classmethod
    def cast(cls, obj):
        if isinstance(obj, cls):
            return cls(
                    version=obj.version,
                    minVersion=obj.minVersion,
                    generator=obj.generator,
                    copyright=obj.copyright,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    version=obj.get("version"),
                    minVersion=obj.get("minVersion"),
                    generator=obj["generator"],
                    copyright=obj.get("copyright"),
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
                    minVersion=next(it),
                    generator=next(it),
                    copyright=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))



    def __str__(self):
        return serializer.dumps(self, type_hints=False)


    def __repr__(self):
        cls = type(self)
        return ("{cls.__name__}("
                "version={self.version!r}, "
                "minVersion={self.minVersion!r}, "
                "generator={self.generator!r}, "
                "copyright={self.copyright!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r})").format(**locals())


def to_dict(obj):
    result = oDict(asset = obj.asset)
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value
    result["version"] = obj.version
    add_valid("minVersion")
    add_valid("generator")
    add_valid("copyright")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=Asset,
        from_dict=lambda dct: Asset.cast(dct),
        to_dict=to_dict)
