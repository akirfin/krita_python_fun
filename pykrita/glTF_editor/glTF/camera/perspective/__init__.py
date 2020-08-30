from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class Perspective(object):
    """
    ...
    """

    def __init__(self,
                yfov=None,
                znear=None,
                zfar=None,
                aspectRatio=None,
                extensions=None,
                extras=None):

        self._yfov = 0.25 * math.pi
        self._znear = 1.0
        self._zfar = 1000.0
        self._aspectRatio = None
        self._extensions = None
        self._extras = None

        if yfov is not None:
            self.yfov = yfov
        if znear is not None:
            self.znear = znear
        if zfar is not None:
            self.zfar = zfar
        if aspectRatio is not None:
            self.aspectRatio = aspectRatio
        if extensions is not None:
            self.extensions = extensions
        if extras is not None:
            self.extras = extras


    @classmethod
    def cast(cls, obj):
        if isinstance(obj, cls):
            return cls(
                    yfov=obj.yfov,
                    znear=obj.znear,
                    zfar=obj.zfar,
                    aspectRatio=obj.aspectRatio,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    yfov=obj.get("yfov"),
                    znear=obj.get("znear"),
                    zfar=obj.get("zfar"),
                    aspectRatio=obj.get("aspectRatio"),
                    extensions=obj.get("extensions"),
                    extras=obj.get("extras"))
        elif isinstance(obj, UnicodeType):
            unserialized = serializer.loads(obj)
            if not isinstance(unserialized, UnicodeType):
                return cls.cast(unserialized)
        elif isinstance(obj, Iterable):
            it = iter(obj)
            return cls(
                    yfov=next(it),
                    znear=next(it),
                    zfar=next(it),
                    aspectRatio=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def getYfov(self):
        if self._yfov is None:
            return None
        else:
            return iter(self._yfov)
    def setYfov(self, newYfov):
        if newYfov is None:
            self._yfov = None
        else:
            self._yfov = [UnicodeType(n) for n in newYfov]
    yfov = property(getYfov, setYfov)


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


    def getAspectRatio(self):
        if self._aspectRatio is None:
            return None
        else:
            return iter(self._aspectRatio)
    def setAspectRatio(self, newAspectRatio):
        if newAspectRatio is None:
            self._aspectRatio = None
        else:
            self._aspectRatio = [UnicodeType(n) for n in newAspectRatio]
    aspectRatio = property(getAspectRatio, setAspectRatio)


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
                "yfov={self.yfov!r}, "
                "znear={self.znear!r}, "
                "zfar={self.zfar!r}, "
                "aspectRatio={self.aspectRatio!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("yfov")
    add_valid("znear")
    add_valid("zfar")
    add_valid("aspectRatio")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=Perspective,
        from_dict=lambda dct: Perspective.cast(dct),
        to_dict=to_dict)
