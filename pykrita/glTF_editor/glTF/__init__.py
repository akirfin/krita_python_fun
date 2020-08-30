from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class GLTF(object):
    """
    ...
    """

    def __init__(self,
                asset=None,
                extensionsUsed=None,
                extensionsRequired=None,
                scene=None,
                scenes=None,
                nodes=None,
                cameras=None,
                meshes=None,
                skins=None,
                images=None,
                textures=None,
                samplers=None,
                materials=None,
                accessors=None,
                bufferViews=None,
                buffers=None,
                animations=None,
                extensions=None,
                extras=None):

        self._asset = Asset()
        self._extensionsUsed = None
        self._extensionsRequired = None
        self._scene = None
        self._scenes = None
        self._nodes = None
        self._cameras = None
        self._meshes = None
        self._skins = None
        self._images = None
        self._textures = None
        self._samplers = None
        self._materials = None
        self._accessors = None
        self._bufferViews = None
        self._buffers = None
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
        if nodes is not None:
            self.nodes = nodes
        if cameras is not None:
            self.cameras = cameras
        if meshes is not None:
            self.meshes = meshes
        if skins is not None:
            self.skins = skins
        if images is not None:
            self.images = images
        if textures is not None:
            self.textures = textures
        if samplers is not None:
            self.samplers = samplers
        if materials is not None:
            self.materials = materials
        if accessors is not None:
            self.accessors = accessors
        if bufferViews is not None:
            self.bufferViews = bufferViews
        if buffers is not None:
            self.buffers = buffers
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
                    nodes=obj.nodes,
                    cameras=obj.cameras,
                    meshes=obj.meshes,
                    skins=obj.skins,
                    images=obj.images,
                    textures=obj.textures,
                    samplers=obj.samplers,
                    materials=obj.materials,
                    accessors=obj.accessors,
                    bufferViews=obj.bufferViews,
                    buffers=obj.buffers,
                    animations=obj.animations,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    asset=obj.get("asset"),
                    extensionsUsed=obj.get("extensionsUsed"),
                    extensionsRequired=obj.get("extensionsRequired"),
                    scene=obj.get("scene"),
                    scenes=obj.get("scenes"),
                    nodes=obj.get("nodes"),
                    cameras=obj.get("cameras"),
                    meshes=obj.get("meshes"),
                    skins=obj.get("skins"),
                    images=obj.get("images"),
                    textures=obj.get("textures"),
                    samplers=obj.get("samplers"),
                    materials=obj.get("materials"),
                    accessors=obj.get("accessors"),
                    bufferViews=obj.get("bufferViews"),
                    buffers=obj.get("buffers"),
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
                    nodes=next(it),
                    cameras=next(it),
                    meshes=next(it),
                    skins=next(it),
                    images=next(it),
                    textures=next(it),
                    samplers=next(it),
                    materials=next(it),
                    accessors=next(it),
                    bufferViews=next(it),
                    buffers=next(it),
                    animations=next(it),
                    extensions=next(it),
                    extras=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def getAsset(self):
        if self._asset is None:
            return None
        else:
            return iter(self._asset)
    def setAsset(self, newAsset):
        if newAsset is None:
            self._asset = None
        else:
            self._asset = [UnicodeType(n) for n in newAsset]
    asset = property(getAsset, setAsset)


    def getExtensionsUsed(self):
        if self._extensionsUsed is None:
            return None
        else:
            return iter(self._extensionsUsed)
    def setExtensionsUsed(self, newExtensionsUsed):
        if newExtensionsUsed is None:
            self._extensionsUsed = None
        else:
            self._extensionsUsed = [UnicodeType(n) for n in newExtensionsUsed]
    extensionsUsed = property(getExtensionsUsed, setExtensionsUsed)


    def getExtensionsRequired(self):
        if self._extensionsRequired is None:
            return None
        else:
            return iter(self._extensionsRequired)
    def setExtensionsRequired(self, newExtensionsRequired):
        if newExtensionsRequired is None:
            self._extensionsRequired = None
        else:
            self._extensionsRequired = [UnicodeType(n) for n in newExtensionsRequired]
    extensionsRequired = property(getExtensionsRequired, setExtensionsRequired)


    def getScene(self):
        if self._scene is None:
            return None
        else:
            return iter(self._scene)
    def setScene(self, newScene):
        if newScene is None:
            self._scene = None
        else:
            self._scene = [UnicodeType(n) for n in newScene]
    scene = property(getScene, setScene)


    def getScenes(self):
        if self._scenes is None:
            return None
        else:
            return iter(self._scenes)
    def setScenes(self, newScenes):
        if newScenes is None:
            self._scenes = None
        else:
            self._scenes = [UnicodeType(n) for n in newScenes]
    scenes = property(getScenes, setScenes)


    def getNodes(self):
        if self._nodes is None:
            return None
        else:
            return iter(self._nodes)
    def setNodes(self, newNodes):
        if newNodes is None:
            self._nodes = None
        else:
            self._nodes = [UnicodeType(n) for n in newNodes]
    nodes = property(getNodes, setNodes)


    def getCameras(self):
        if self._cameras is None:
            return None
        else:
            return iter(self._cameras)
    def setCameras(self, newCameras):
        if newCameras is None:
            self._cameras = None
        else:
            self._cameras = [UnicodeType(n) for n in newCameras]
    cameras = property(getCameras, setCameras)


    def getMeshes(self):
        if self._meshes is None:
            return None
        else:
            return iter(self._meshes)
    def setMeshes(self, newMeshes):
        if newMeshes is None:
            self._meshes = None
        else:
            self._meshes = [UnicodeType(n) for n in newMeshes]
    meshes = property(getMeshes, setMeshes)


    def getSkins(self):
        if self._skins is None:
            return None
        else:
            return iter(self._skins)
    def setSkins(self, newSkins):
        if newSkins is None:
            self._skins = None
        else:
            self._skins = [UnicodeType(n) for n in newSkins]
    skins = property(getSkins, setSkins)


    def getImages(self):
        if self._images is None:
            return None
        else:
            return iter(self._images)
    def setImages(self, newImages):
        if newImages is None:
            self._images = None
        else:
            self._images = [UnicodeType(n) for n in newImages]
    images = property(getImages, setImages)


    def getTextures(self):
        if self._textures is None:
            return None
        else:
            return iter(self._textures)
    def setTextures(self, newTextures):
        if newTextures is None:
            self._textures = None
        else:
            self._textures = [UnicodeType(n) for n in newTextures]
    textures = property(getTextures, setTextures)


    def getSamplers(self):
        if self._samplers is None:
            return None
        else:
            return iter(self._samplers)
    def setSamplers(self, newSamplers):
        if newSamplers is None:
            self._samplers = None
        else:
            self._samplers = [UnicodeType(n) for n in newSamplers]
    samplers = property(getSamplers, setSamplers)


    def getMaterials(self):
        if self._materials is None:
            return None
        else:
            return iter(self._materials)
    def setMaterials(self, newMaterials):
        if newMaterials is None:
            self._materials = None
        else:
            self._materials = [UnicodeType(n) for n in newMaterials]
    materials = property(getMaterials, setMaterials)


    def getAccessors(self):
        if self._accessors is None:
            return None
        else:
            return iter(self._accessors)
    def setAccessors(self, newAccessors):
        if newAccessors is None:
            self._accessors = None
        else:
            self._accessors = [UnicodeType(n) for n in newAccessors]
    accessors = property(getAccessors, setAccessors)


    def getBufferViews(self):
        if self._bufferViews is None:
            return None
        else:
            return iter(self._bufferViews)
    def setBufferViews(self, newBufferViews):
        if newBufferViews is None:
            self._bufferViews = None
        else:
            self._bufferViews = [UnicodeType(n) for n in newBufferViews]
    bufferViews = property(getBufferViews, setBufferViews)


    def getBuffers(self):
        if self._buffers is None:
            return None
        else:
            return iter(self._buffers)
    def setBuffers(self, newBuffers):
        if newBuffers is None:
            self._buffers = None
        else:
            self._buffers = [UnicodeType(n) for n in newBuffers]
    buffers = property(getBuffers, setBuffers)


    def getAnimations(self):
        if self._animations is None:
            return None
        else:
            return iter(self._animations)
    def setAnimations(self, newAnimations):
        if newAnimations is None:
            self._animations = None
        else:
            self._animations = [UnicodeType(n) for n in newAnimations]
    animations = property(getAnimations, setAnimations)


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
                "asset={self.asset!r}, "
                "extensionsUsed={self.extensionsUsed!r}, "
                "extensionsRequired={self.extensionsRequired!r}, "
                "scene={self.scene!r}, "
                "scenes={self.scenes!r}, "
                "nodes={self.nodes!r}, "
                "cameras={self.cameras!r}, "
                "meshes={self.meshes!r}, "
                "skins={self.skins!r}, "
                "images={self.images!r}, "
                "textures={self.textures!r}, "
                "samplers={self.samplers!r}, "
                "materials={self.materials!r}, "
                "accessors={self.accessors!r}, "
                "bufferViews={self.bufferViews!r}, "
                "buffers={self.buffers!r}, "
                "animations={self.animations!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("asset")
    add_valid("extensionsUsed")
    add_valid("extensionsRequired")
    add_valid("scene")
    add_valid("scenes")
    add_valid("nodes")
    add_valid("cameras")
    add_valid("meshes")
    add_valid("skins")
    add_valid("images")
    add_valid("textures")
    add_valid("samplers")
    add_valid("materials")
    add_valid("accessors")
    add_valid("bufferViews")
    add_valid("buffers")
    add_valid("animations")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=GLTF,
        from_dict=lambda dct: GLTF.cast(dct),
        to_dict=to_dict)
