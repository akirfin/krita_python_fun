from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class Skin(object):
    """
    ...
    """

    def __init__(self,
                joints=None,
                inverseBindMatrices=None,
                skeleton=None,
                extensions=None,
                extras=None):

        self._joints = list()
        self._inverseBindMatrices = None
        self._skeleton = None
        self._extensions = None
        self._extras = None

        if joints is not None:
            self.joints = joints
        if inverseBindMatrices is not None:
            self.inverseBindMatrices = inverseBindMatrices
        if skeleton is not None:
            self.skeleton = skeleton
        if extensions is not None:
            self.extensions = extensions
        if extras is not None:
            self.extras = extras


    @classmethod
    def cast(cls, obj):
        if isinstance(obj, cls):
            return cls(
                    joints=obj.joints,
                    inverseBindMatrices=obj.inverseBindMatrices,
                    skeleton=obj.skeleton,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    joints=obj.get("joints"),
                    inverseBindMatrices=obj.get("inverseBindMatrices"),
                    skeleton=obj.get("skeleton"),
                    extensions=obj.get("extensions"),
                    extras=obj.get("extras"))
        elif isinstance(obj, UnicodeType):
            unserialized = serializer.loads(obj)
            if not isinstance(unserialized, UnicodeType):
                return cls.cast(unserialized)
        elif isinstance(obj, Iterable):
            it = iter(obj)
            return cls(
                    joints=next(it),
                    inverseBindMatrices=next(it),
                    skeleton=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def getJoints(self):
        if self._joints is None:
            return None
        else:
            return iter(self._joints)
    def setJoints(self, newJoints):
        if newJoints is None:
            self._joints = None
        else:
            self._joints = [UnicodeType(n) for n in newJoints]
    joints = property(getJoints, setJoints)


    def getInverseBindMatrices(self):
        if self._inverseBindMatrices is None:
            return None
        else:
            return iter(self._inverseBindMatrices)
    def setInverseBindMatrices(self, newInverseBindMatrices):
        if newInverseBindMatrices is None:
            self._inverseBindMatrices = None
        else:
            self._inverseBindMatrices = [UnicodeType(n) for n in newInverseBindMatrices]
    inverseBindMatrices = property(getInverseBindMatrices, setInverseBindMatrices)


    def getSkeleton(self):
        if self._skeleton is None:
            return None
        else:
            return iter(self._skeleton)
    def setSkeleton(self, newSkeleton):
        if newSkeleton is None:
            self._skeleton = None
        else:
            self._skeleton = [UnicodeType(n) for n in newSkeleton]
    skeleton = property(getSkeleton, setSkeleton)


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
                "joints={self.joints!r}, "
                "inverseBindMatrices={self.inverseBindMatrices!r}, "
                "skeleton={self.skeleton!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("joints")
    add_valid("inverseBindMatrices")
    add_valid("skeleton")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=Skin,
        from_dict=lambda dct: Skin.cast(dct),
        to_dict=to_dict)
