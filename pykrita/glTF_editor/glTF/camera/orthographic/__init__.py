from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class Orthographic(object):
    """
    ...
    """

    def __init__(self,
                xmag=None,
                ymag=None,
                znear=None,
                zfar=None,
                extensions=None,
                extras=None):

        self._xmag = 1.0
        self._ymag = 1.0
        self._znear = 0.0
        self._zfar = 1000.0
        self._extensions = None
        self._extras = None

        if xmag is not None:
            self.xmag = xmag
        if ymag is not None:
            self.ymag = ymag
        if znear is not None:
            self.znear = znear
        if zfar is not None:
            self.zfar = zfar
        if extensions is not None:
            self.extensions = extensions
        if extras is not None:
            self.extras = extras


    @classmethod
    def cast(cls, obj):
        if isinstance(obj, cls):
            return cls(
                    xmag=obj.xmag,
                    ymag=obj.ymag,
                    znear=obj.znear,
                    zfar=obj.zfar,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    xmag=obj.get("xmag"),
                    ymag=obj.get("ymag"),
                    znear=obj.get("znear"),
                    zfar=obj.get("zfar"),
                    extensions=obj.get("extensions"),
                    extras=obj.get("extras"))
        elif isinstance(obj, UnicodeType):
            unserialized = serializer.loads(obj)
            if not isinstance(unserialized, UnicodeType):
                return cls.cast(unserialized)
        elif isinstance(obj, Iterable):
            it = iter(obj)
            return cls(
                    xmag=next(it),
                    ymag=next(it),
                    znear=next(it),
                    zfar=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def getXmag(self):
        if self._xmag is None:
            return None
        else:
            return iter(self._xmag)
    def setXmag(self, newXmag):
        if newXmag is None:
            self._xmag = None
        else:
            self._xmag = [UnicodeType(n) for n in newXmag]
    xmag = property(getXmag, setXmag)


    def getYmag(self):
        if self._ymag is None:
            return None
        else:
            return iter(self._ymag)
    def setYmag(self, newYmag):
        if newYmag is None:
            self._ymag = None
        else:
            self._ymag = [UnicodeType(n) for n in newYmag]
    ymag = property(getYmag, setYmag)


    def getZnear(self):
        if self._znear is None:
            return None
        else:
            return iter(self._znear)
    def setZnear(self, newZnear):
        if newZnear is None:
            self._znear = None
        else:
            self._znear = [UnicodeType(n) for n in newZnear]
    znear = property(getZnear, setZnear)


    def getZfar(self):
        if self._zfar is None:
            return None
        else:
            return iter(self._zfar)
    def setZfar(self, newZfar):
        if newZfar is None:
            self._zfar = None
        else:
            self._zfar = [UnicodeType(n) for n in newZfar]
    zfar = property(getZfar, setZfar)


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
                "xmag={self.xmag!r}, "
                "ymag={self.ymag!r}, "
                "znear={self.znear!r}, "
                "zfar={self.zfar!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("xmag")
    add_valid("ymag")
    add_valid("znear")
    add_valid("zfar")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=Orthographic,
        from_dict=lambda dct: Orthographic.cast(dct),
        to_dict=to_dict)
