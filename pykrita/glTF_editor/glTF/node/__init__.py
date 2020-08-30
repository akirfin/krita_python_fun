from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class Node(object):
    """
    ...
    """

    def __init__(self,
                translation=None,
                rotation=None,
                scale=None,
                matrix=None,
                children=None,
                camera=None,
                skin=None,
                mesh=None,
                weights=None,
                name=None,
                extensions=None,
                extras=None):

        self._translation = Vector3(0.0, 0.0, 0.0)
        self._rotation = Quaternion(0.0, 0.0, 0.0, 1.0)
        self._scale = Vector3(1.0, 1.0, 1.0)
        self._matrix = None
        self._children = None
        self._camera = None
        self._skin = None
        self._mesh = None
        self._weights = None
        self._name = None
        self._extensions = None
        self._extras = None

        if translation is not None:
            self.translation = translation
        if rotation is not None:
            self.rotation = rotation
        if scale is not None:
            self.scale = scale
        if matrix is not None:
            self.matrix = matrix
        if children is not None:
            self.children = children
        if camera is not None:
            self.camera = camera
        if skin is not None:
            self.skin = skin
        if mesh is not None:
            self.mesh = mesh
        if weights is not None:
            self.weights = weights
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
                    translation=obj.translation,
                    rotation=obj.rotation,
                    scale=obj.scale,
                    matrix=obj.matrix,
                    children=obj.children,
                    camera=obj.camera,
                    skin=obj.skin,
                    mesh=obj.mesh,
                    weights=obj.weights,
                    name=obj.name,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    translation=obj.get("translation"),
                    rotation=obj.get("rotation"),
                    scale=obj.get("scale"),
                    matrix=obj.get("matrix"),
                    children=obj.get("children"),
                    camera=obj.get("camera"),
                    skin=obj.get("skin"),
                    mesh=obj.get("mesh"),
                    weights=obj.get("weights"),
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
                    translation=next(it),
                    rotation=next(it),
                    scale=next(it),
                    matrix=next(it),
                    children=next(it),
                    camera=next(it),
                    skin=next(it),
                    mesh=next(it),
                    weights=next(it),
                    name=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def getTranslation(self):
        if self._translation is None:
            return None
        else:
            return iter(self._translation)
    def setTranslation(self, newTranslation):
        if newTranslation is None:
            self._translation = None
        else:
            self._translation = [UnicodeType(n) for n in newTranslation]
    translation = property(getTranslation, setTranslation)


    def getRotation(self):
        if self._rotation is None:
            return None
        else:
            return iter(self._rotation)
    def setRotation(self, newRotation):
        if newRotation is None:
            self._rotation = None
        else:
            self._rotation = [UnicodeType(n) for n in newRotation]
    rotation = property(getRotation, setRotation)


    def getScale(self):
        if self._scale is None:
            return None
        else:
            return iter(self._scale)
    def setScale(self, newScale):
        if newScale is None:
            self._scale = None
        else:
            self._scale = [UnicodeType(n) for n in newScale]
    scale = property(getScale, setScale)


    def getMatrix(self):
        if self._matrix is None:
            return None
        else:
            return iter(self._matrix)
    def setMatrix(self, newMatrix):
        if newMatrix is None:
            self._matrix = None
        else:
            self._matrix = [UnicodeType(n) for n in newMatrix]
    matrix = property(getMatrix, setMatrix)


    def getChildren(self):
        if self._children is None:
            return None
        else:
            return iter(self._children)
    def setChildren(self, newChildren):
        if newChildren is None:
            self._children = None
        else:
            self._children = [UnicodeType(n) for n in newChildren]
    children = property(getChildren, setChildren)


    def getCamera(self):
        if self._camera is None:
            return None
        else:
            return iter(self._camera)
    def setCamera(self, newCamera):
        if newCamera is None:
            self._camera = None
        else:
            self._camera = [UnicodeType(n) for n in newCamera]
    camera = property(getCamera, setCamera)


    def getSkin(self):
        if self._skin is None:
            return None
        else:
            return iter(self._skin)
    def setSkin(self, newSkin):
        if newSkin is None:
            self._skin = None
        else:
            self._skin = [UnicodeType(n) for n in newSkin]
    skin = property(getSkin, setSkin)


    def getMesh(self):
        if self._mesh is None:
            return None
        else:
            return iter(self._mesh)
    def setMesh(self, newMesh):
        if newMesh is None:
            self._mesh = None
        else:
            self._mesh = [UnicodeType(n) for n in newMesh]
    mesh = property(getMesh, setMesh)


    def getWeights(self):
        if self._weights is None:
            return None
        else:
            return iter(self._weights)
    def setWeights(self, newWeights):
        if newWeights is None:
            self._weights = None
        else:
            self._weights = [UnicodeType(n) for n in newWeights]
    weights = property(getWeights, setWeights)


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
                "translation={self.translation!r}, "
                "rotation={self.rotation!r}, "
                "scale={self.scale!r}, "
                "matrix={self.matrix!r}, "
                "children={self.children!r}, "
                "camera={self.camera!r}, "
                "skin={self.skin!r}, "
                "mesh={self.mesh!r}, "
                "weights={self.weights!r}, "
                "name={self.name!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("translation")
    add_valid("rotation")
    add_valid("scale")
    add_valid("matrix")
    add_valid("children")
    add_valid("camera")
    add_valid("skin")
    add_valid("mesh")
    add_valid("weights")
    add_valid("name")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=Node,
        from_dict=lambda dct: Node.cast(dct),
        to_dict=to_dict)
