from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class Camera(object):
    """
    ...
    """

    def __init__(self,
                type=None,
                orthographic=None,
                perspective=None,
                name=None,
                extensions=None,
                extras=None):

        self._type = CameraType.PERSPECTIVE
        self._orthographic = None
        self._perspective = None
        self._name = None
        self._extensions = None
        self._extras = None

        if type is not None:
            self.type = type
        if orthographic is not None:
            self.orthographic = orthographic
        if perspective is not None:
            self.perspective = perspective
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
                    type=obj.type,
                    orthographic=obj.orthographic,
                    perspective=obj.perspective,
                    name=obj.name,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    type=obj.get("type"),
                    orthographic=obj.get("orthographic"),
                    perspective=obj.get("perspective"),
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
                    type=next(it),
                    orthographic=next(it),
                    perspective=next(it),
                    name=next(it),
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


    def getOrthographic(self):
        if self._orthographic is None:
            return None
        else:
            return iter(self._orthographic)
    def setOrthographic(self, newOrthographic):
        if newOrthographic is None:
            self._orthographic = None
        else:
            self._orthographic = [UnicodeType(n) for n in newOrthographic]
    orthographic = property(getOrthographic, setOrthographic)


    def getPerspective(self):
        if self._perspective is None:
            return None
        else:
            return iter(self._perspective)
    def setPerspective(self, newPerspective):
        if newPerspective is None:
            self._perspective = None
        else:
            self._perspective = [UnicodeType(n) for n in newPerspective]
    perspective = property(getPerspective, setPerspective)


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
                "type={self.type!r}, "
                "orthographic={self.orthographic!r}, "
                "perspective={self.perspective!r}, "
                "name={self.name!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("type")
    add_valid("orthographic")
    add_valid("perspective")
    add_valid("name")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=Camera,
        from_dict=lambda dct: Camera.cast(dct),
        to_dict=to_dict)
