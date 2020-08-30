from enum import Enum

from glTF_editor.common.data_serializer import \
        serializer

from .accessor import \
        Accessor, Sparse, Indices, Values
from .animation import \
        Animation, AnimationSampler, Channel, Target
from .asset import \
        Asset
from .buffer import \
        Buffer
from .bufferView import \
        BufferView
from .camera import \
        Camera, CameraType, Orthographic, Perspective
from .light import \
        Light, LightType, AmbientInfo, DirectionalInfo, PointInfo, SpotInfo
from .extension import \
        Extension
from .extras import \
        Extras, Image
from .material import \
        Material, NormalTextureInfo, OcclusionTextureInfo, PbrMetallicRoughness
from .mesh import \
        Mesh, Primitive
from .node import \
        Node
from .sampler import \
        Sampler
from .scene import \
        Scene
from .skin import \
        Skin
from .texture import \
        Texture
from .textureInfo import \
        TextureInfo


class AlphaMode(Enum):
    OPAQUE = "OPAQUE"
    MASK = "MASK"
    BLEND = "BLEND"


class AnimationTargetPath(Enum):
    """
    issue: evil lowercase!
    """
    TRANSLATION = "translation"
    ROTATION = "rotation"
    SCALE = "scale"
    WEIGHTS = "weights"


class BufferTarget(Enum):
    """
    issue: evil magic numbers!
    """
    ARRAY_BUFFER = 34962
    ELEMENT_ARRAY_BUFFER = 34963


class Interpolation(Enum):
    LINEAR = "LINEAR"
    STEP = "STEP"
    CUBICSPLINE = "CUBICSPLINE"


class PrimitiveMode(Enum):
    """
    issue: evil magic numbers!
    """
    POINTS = 0
    LINES = 1
    LINE_LOOP = 2
    LINE_STRIP = 3
    TRIANGLES = 4
    TRIANGLE_STRIP = 5


class ImageFormat(Enum):
    DATA_URI = "DATA_URI"
    IMAGE_FILE = "IMAGE_FILE"
    BUFFER_VIEW = "BUFFER_VIEW"


class BufferFormat(Enum):
    DATA_URI = "DATA_URI"
    BINARY_BLOB = "BINARY_BLOB"
    BIN_FILE = "BIN_FILE"



class GLTF(object):
    """
    lowercase and uppercase, conventions thrown to trashbin. (There is no winning with this one!)

    The document object for a glTF asset.
    Additional properties are allowed. (allowed and ignored :P)
    """

    def __init__(self,
                asset=None,
                extensionsUsed=None,
                extensionsRequired=None,
                scene=None,
                scenes=None,
                cameras=None,
                lights=None,
                nodes=None,
                images=None,
                textures=None,
                samplers=None,
                materials=None,
                bufferViews=None,
                accessors=None,
                skins=None,
                buffers=None,
                meshes=None,
                animations=None,
                extensions=None,
                extras=None):

        self._asset = Asset()
        self._extensionsUsed = None
        self._extensionsRequired = None
        self._scene = None
        self._scenes = None
        self._cameras = None
        self._lights = None
        self._nodes = None
        self._images = None
        self._textures = None
        self._samplers = None
        self._materials = None
        self._bufferViews = None
        self._accessors = None
        self._skins = None
        self._buffers = None
        self._meshes = None
        self._animations = None
        self._extensions = None
        self._extras = None

        if asset is not None:
            self.asset = asset
        if extensionsUsed is not None:
            self.extensionsUsed = extensionsUsed
        if extensionsRequired is not None:
            self.extensionsRequired = extensionsRequired
        if scene is not None:
            self.scene = scene
        if scenes is not None:
            self.scenes = scenes
        if cameras is not None:
            self.cameras = cameras
        if lights is not None:
            self.lights = lights
        if nodes is not None:
            self.nodes = nodes
        if images is not None:
            self.images = images
        if textures is not None:
            self.textures = textures
        if samplers is not None:
            self.samplers = samplers
        if materials is not None:
            self.materials = materials
        if bufferViews is not None:
            self.bufferViews = bufferViews
        if accessors is not None:
            self.accessors = accessors
        if skins is not None:
            self.skins = skins
        if buffers is not None:
            self.buffers = buffers
        if meshes is not None:
            self.meshes = meshes
        if animations is not None:
            self.animations = animations
        if extensions is not None:
            self.extensions = extensions
        if extras is not None:
            self.extras = extras


    @classmethod
    def cast(cls, obj):
        if isinstance(obj, cls):
            return cls(
                    asset=obj.asset,
                    extensionsUsed=obj.extensionsUsed,
                    extensionsRequired=obj.extensionsRequired,
                    scene=obj.scene,
                    scenes=obj.scenes,
                    cameras=obj.cameras,
                    lights=obj.lights,
                    nodes=obj.nodes,
                    images=obj.images,
                    textures=obj.textures,
                    samplers=obj.samplers,
                    materials=obj.materials,
                    bufferViews=obj.bufferViews,
                    accessors=obj.accessors,
                    skins=obj.skins,
                    buffers=obj.buffers,
                    meshes=obj.meshes,
                    animations=obj.animations,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    asset=obj["asset"],
                    extensionsUsed=obj.get("extensionsUsed"),
                    extensionsRequired=obj.get("extensionsRequired"),
                    scene=obj.get("scene"),
                    scenes=obj.get("scenes"),
                    cameras=obj.get("cameras"),
                    lights=obj.get("lights"),
                    nodes=obj.get("nodes"),
                    images=obj.get("images"),
                    textures=obj.get("textures"),
                    samplers=obj.get("samplers"),
                    materials=obj.get("materials"),
                    bufferViews=obj.get("bufferViews"),
                    accessors=obj.get("accessors"),
                    skins=obj.get("skins"),
                    buffers=obj.get("buffers"),
                    meshes=obj.get("meshes"),
                    animations=obj.get("animations"),
                    extensions=obj.get("extensions"),
                    extras=obj.get("extras"))
        elif isinstance(obj, UnicodeType):
            unserialized = serializer.loads(obj)
            if not isinstance(unserialized, UnicodeType):
                return cls.cast(unserialized)
        elif isinstance(obj, Iterable):
            it = iter(obj)
            return cls(
                    asset=next(it),
                    extensionsUsed=next(it),
                    extensionsRequired=next(it),
                    scene=next(it),
                    scenes=next(it),
                    cameras=next(it),
                    lights=next(it),
                    nodes=next(it),
                    images=next(it),
                    textures=next(it),
                    samplers=next(it),
                    materials=next(it),
                    bufferViews=next(it),
                    accessors=next(it),
                    skins=next(it),
                    buffers=next(it),
                    meshes=next(it),
                    animations=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def getAsset(self):
        return self._asset
    def setAsset(self, newAsset):
        self._asset = Asset.cast(newAsset)
    asset = property(getAsset, setAsset)


    def getExtensionsUsed(self):
        return self._extensionsUsed
    def setExtensionsUsed(self, newExtensions):
        if newExtensions is None:
            self._extensionsUsed = None
        else:
            self._extensionsUsed = [UnicodeType(e) for e in newExtensions]
    extensionsUsed = property(getExtensionsUsed, setExtensionsUsed)


    def getExtensionsRequired(self):
        return self._extensionsRequired
    def setExtensionsRequired(self, newRequired):
        if newRequired is None:
            self._extensionsRequired = None
        else:
            self._extensionsRequired = [UnicodeType(r) for r in newRequired]
    extensionsRequired = property(getExtensionsRequired, setExtensionsRequired)


    def getScene(self):
        return self._extensionsRequired
    def setScene(self, newScene):
        if newExtensions is None:
            self._scene = None
        else:
            self._scene = int(newScene)
    extensionsRequired = property(getExtensionsRequired, setExtensionsRequired)


    def __str__(self):
        return serializer.dumps(self, type_hints=False)


    def __repr__(self):
        cls = type(self)
        return ("{cls.__name__}("
                "asset={self.asset!r}, "
                "extensionsUsed={self.extensionsUsed!r}, "
                "extensionsRequired={self.extensionsRequired!r}, "
                "scene={self.scene!r}, "
                "scenes={self.scenes!r}, "
                "cameras={self.cameras!r}, "
                "lights={self.lights!r}, "
                "nodes={self.nodes!r}, "
                "images={self.images!r}, "
                "textures={self.textures!r}, "
                "samplers={self.samplers!r}, "
                "materials={self.materials!r}, "
                "bufferViews={self.bufferViews!r}, "
                "accessors={self.accessors!r}, "
                "skins={self.skins!r}, "
                "buffers={self.buffers!r}, "
                "meshes={self.meshes!r}, "
                "animations={self.animations!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r})").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value
    result["asset"] = obj.asset
    add_valid("extensionsRequired")
    add_valid("extensionsUsed")
    add_valid("scene")
    add_valid("scenes")
    add_valid("cameras")
    add_valid("lights")
    add_valid("nodes")
    add_valid("images")
    add_valid("textures")
    add_valid("samplers")
    add_valid("materials")
    add_valid("bufferViews")
    add_valid("accessors")
    add_valid("skins")
    add_valid("buffers")
    add_valid("meshes")
    add_valid("animations")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=GLTF,
        from_dict=lambda dct: GLTF.cast(dct),
        to_dict=to_dict)
