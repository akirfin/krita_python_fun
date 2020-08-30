from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class Primitive(object):
    """
    ...
    """

    def __init__(self,
                mode=None,
                attributes=None,
                indices=None,
                material=None,
                targets=None,
                extensions=None,
                extras=None):

        self._mode = PrimitiveType.TRIANGLES
        self._attributes = oDict()
        self._indices = None
        self._material = None
        self._targets = None
        self._extensions = None
        self._extras = None

        if mode is not None:
            self.mode = mode
        if attributes is not None:
            self.attributes = attributes
        if indices is not None:
            self.indices = indices
        if material is not None:
            self.material = material
        if targets is not None:
            self.targets = targets
        if extensions is not None:
            self.extensions = extensions
        if extras is not None:
            self.extras = extras


    @classmethod
    def cast(cls, obj):
        if isinstance(obj, cls):
            return cls(
                    mode=obj.mode,
                    attributes=obj.attributes,
                    indices=obj.indices,
                    material=obj.material,
                    targets=obj.targets,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    mode=obj.get("mode"),
                    attributes=obj.get("attributes"),
                    indices=obj.get("indices"),
                    material=obj.get("material"),
                    targets=obj.get("targets"),
                    extensions=obj.get("extensions"),
                    extras=obj.get("extras"))
        elif isinstance(obj, UnicodeType):
            unserialized = serializer.loads(obj)
            if not isinstance(unserialized, UnicodeType):
                return cls.cast(unserialized)
        elif isinstance(obj, Iterable):
            it = iter(obj)
            return cls(
                    mode=next(it),
                    attributes=next(it),
                    indices=next(it),
                    material=next(it),
                    targets=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def getMode(self):
        if self._mode is None:
            return None
        else:
            return iter(self._mode)
    def setMode(self, newMode):
        if newMode is None:
            self._mode = None
        else:
            self._mode = [UnicodeType(n) for n in newMode]
    mode = property(getMode, setMode)


    def getAttributes(self):
        if self._attributes is None:
            return None
        else:
            return iter(self._attributes)
    def setAttributes(self, newAttributes):
        if newAttributes is None:
            self._attributes = None
        else:
            self._attributes = [UnicodeType(n) for n in newAttributes]
    attributes = property(getAttributes, setAttributes)


    def getIndices(self):
        if self._indices is None:
            return None
        else:
            return iter(self._indices)
    def setIndices(self, newIndices):
        if newIndices is None:
            self._indices = None
        else:
            self._indices = [UnicodeType(n) for n in newIndices]
    indices = property(getIndices, setIndices)


    def getMaterial(self):
        if self._material is None:
            return None
        else:
            return iter(self._material)
    def setMaterial(self, newMaterial):
        if newMaterial is None:
            self._material = None
        else:
            self._material = [UnicodeType(n) for n in newMaterial]
    material = property(getMaterial, setMaterial)


    def getTargets(self):
        if self._targets is None:
            return None
        else:
            return iter(self._targets)
    def setTargets(self, newTargets):
        if newTargets is None:
            self._targets = None
        else:
            self._targets = [UnicodeType(n) for n in newTargets]
    targets = property(getTargets, setTargets)


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
                "mode={self.mode!r}, "
                "attributes={self.attributes!r}, "
                "indices={self.indices!r}, "
                "material={self.material!r}, "
                "targets={self.targets!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("mode")
    add_valid("attributes")
    add_valid("indices")
    add_valid("material")
    add_valid("targets")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=Primitive,
        from_dict=lambda dct: Primitive.cast(dct),
        to_dict=to_dict)
