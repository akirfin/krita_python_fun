from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class Target(object):
    """
    ...
    """

    def __init__(self,
                path=None,
                node=None,
                extensions=None,
                extras=None):

        self._path = AnimationTargetPath.TRANSLATION
        self._node = 0
        self._extensions = None
        self._extras = None

        if path is not None:
            self.path = path
        if node is not None:
            self.node = node
        if extensions is not None:
            self.extensions = extensions
        if extras is not None:
            self.extras = extras


    @classmethod
    def cast(cls, obj):
        if isinstance(obj, cls):
            return cls(
                    path=obj.path,
                    node=obj.node,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    path=obj.get("path"),
                    node=obj.get("node"),
                    extensions=obj.get("extensions"),
                    extras=obj.get("extras"))
        elif isinstance(obj, UnicodeType):
            unserialized = serializer.loads(obj)
            if not isinstance(unserialized, UnicodeType):
                return cls.cast(unserialized)
        elif isinstance(obj, Iterable):
            it = iter(obj)
            return cls(
                    path=next(it),
                    node=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def getPath(self):
        if self._path is None:
            return None
        else:
            return iter(self._path)
    def setPath(self, newPath):
        if newPath is None:
            self._path = None
        else:
            self._path = [UnicodeType(n) for n in newPath]
    path = property(getPath, setPath)


    def getNode(self):
        if self._node is None:
            return None
        else:
            return iter(self._node)
    def setNode(self, newNode):
        if newNode is None:
            self._node = None
        else:
            self._node = [UnicodeType(n) for n in newNode]
    node = property(getNode, setNode)


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
                "path={self.path!r}, "
                "node={self.node!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("path")
    add_valid("node")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=Target,
        from_dict=lambda dct: Target.cast(dct),
        to_dict=to_dict)
