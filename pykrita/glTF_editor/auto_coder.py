import os


def init_args(attrs):
    return ",\n".join(f"""\
                {attr}=None""" for attr in attrs)

def init_defaults(attrs):
    return "\n".join(f"""\
        self._{attr} = {default}""" for attr, default in attrs.items())

def init_set_attrs(attrs):
    return "\n".join(f"""\
        if {attr} is not None:
            self.{attr} = {attr}""" for attr in attrs)

def cast_cls(attrs):
    return ",\n".join(f"""\
                    {attr}=obj.{attr}""" for attr in attrs)

def cast_mapping(attrs):
    return ",\n".join(f"""\
                    {attr}=obj.get(\"{attr}\")""" for attr in attrs)

def cast_it(attrs):
    return ",\n".join(f"""\
                    {attr}=next(it)""" for attr in attrs)

def get_set(attrs):
    up_attrs = [a[0].upper() + a[1:] for a in attrs]
    return "\n\n\n".join(f"""\
    def get{up_attr}(self):
        if self._{attr} is None:
            return None
        else:
            return iter(self._{attr})
    def set{up_attr}(self, new{up_attr}):
        if new{up_attr} is None:
            self._{attr} = None
        else:
            self._{attr} = [UnicodeType(n) for n in new{up_attr}]
    {attr} = property(get{up_attr}, set{up_attr})""" for attr, up_attr in zip(attrs, up_attrs))

def repr_attrs(attrs):
    seps = [", " for _ in range(len(attrs) - 1)] + [""]
    return "\n".join(f"""\
                \"{attr}={{self.{attr}!r}}{sep}\"""" for attr, sep in zip(attrs, seps))

def to_dict_attrs(attrs):
    return "\n".join(f"""\
    add_valid(\"{attr}\")""" for attr in attrs)

def write_file(filename, cls_name, attrs):
    code = f"""\
from enum import Enum

from glTF_editor.common.utils_py import \\
        UnicodeType

from glTF_editor.common.data_serializer import \\
        serializer


class {cls_name}(object):
    \"\"\"
    ...
    \"\"\"

    def __init__(self,
{init_args(attrs)}):

{init_defaults(attrs)}

{init_set_attrs(attrs)}


    @classmethod
    def cast(cls, obj):
        if isinstance(obj, cls):
            return cls(
{cast_cls(attrs)})
        elif isinstance(obj, Mapping):
            return cls(
{cast_mapping(attrs)})
        elif isinstance(obj, UnicodeType):
            unserialized = serializer.loads(obj)
            if not isinstance(unserialized, UnicodeType):
                return cls.cast(unserialized)
        elif isinstance(obj, Iterable):
            it = iter(obj)
            return cls(
{cast_it(attrs)})
        raise RuntimeError("Unable to Cast {{obj!r}} to {{cls}} instance.".format(**locals()))


{get_set(attrs)}


    def __str__(self):
        return serializer.dumps(self, type_hints=False)


    def __repr__(self):
        cls = type(self)
        return ("{{cls.__name__}}("
{repr_attrs(attrs)})").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
{to_dict_attrs(attrs)}
    return result


serializer.register(
        data_cls={cls_name},
        from_dict=lambda dct: {cls_name}.cast(dct),
        to_dict=to_dict)
"""
    dir_path = os.path.dirname(filename)
    # print(dir_path, filename, code)
    os.makedirs(dir_path, exist_ok=True)
    with open(filename, "wb") as f:
        f.write(code.encode("utf-8"))


if __name__ == "__main__":
    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\__init__.py",
            "GLTF",
            dict(
                asset="Asset()",  # Metadata about the glTF asset.
                extensionsUsed=None,  # Names of glTF extensions used somewhere in this asset
                extensionsRequired=None,  # Names of glTF extensions required to properly load this asset.
                scene=None,  # The index of the default scene.
                scenes=None,  # An array of scenes.
                nodes=None,  # An array of nodes.
                cameras=None,  # An array of cameras.
                meshes=None,  # An array of meshes.
                skins=None,  # An array of skins.
                images=None,  # An array of images.
                textures=None,  # An array of textures.
                samplers=None,  # An array of samplers.
                materials=None,  # An array of materials.
                accessors=None,  # An array of accessors.
                bufferViews=None,  # An array of bufferViews.
                buffers=None,  # An array of buffers.
                animations=None,  # An array of keyframe animations.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\accessor\__init__.py",
            "Accessor",
            dict(
                type="AccessorType.SCALAR",  # Specifies if the attribute is a scalar, vector, or matrix.
                componentType="ComponentType.FLOAT",  # The datatype of components in the attribute.
                count=0,  # The number of attributes referenced by this accessor.
                byteOffset=0,  # The offset relative to the start of the bufferView in bytes.
                normalized=False,  # Specifies whether integer data values should be normalized.
                name=None,  # The user-defined name of this object.
                bufferView=None,  # The index of the bufferView.
                max=None,  # Maximum value of each component in this attribute.
                min=None,  # Minimum value of each component in this attribute.
                sparse=None,  # Sparse storage of attributes that deviate from their initialization value.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\accessor\sparse\__init__.py",
            "Sparse",
            dict(
                indices="Indices()",  # Index array of size count that points to those accessor attributes that deviate from their initialization value. Indices must strictly increase.
                values="Values()",  # Array of size count times number of components, storing the displaced accessor attributes pointed by indices. Substituted values must have the same componentType and number of components as the base accessor.
                count=0,  # Number of entries stored in the sparse array.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\accessor\sparse\indices\__init__.py",
            "Indices",
            dict(
                bufferView=0,  # The index of the bufferView with sparse indices. Referenced bufferView can't have ARRAY_BUFFER or ELEMENT_ARRAY_BUFFER target.
                componentType="ComponentType.FLOAT",  # The indices data type.
                byteOffset=0,  # The offset relative to the start of the bufferView in bytes. Must be aligned.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\accessor\sparse\values\__init__.py",
            "Values",
            dict(
                bufferView=0,  # The index of the bufferView with sparse values. Referenced bufferView can't have ARRAY_BUFFER or ELEMENT_ARRAY_BUFFER target.
                byteOffset=0,  # The offset relative to the start of the bufferView in bytes. Must be aligned.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None,  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\animation\__init__.py",
            "Animation",
            dict(
                channels="list()",  # An array of channels, each of which targets an animation's sampler at a node's property. Different channels of the same animation can't have equal targets.
                samplers="list()",  # An array of samplers that combines input and output accessors with an interpolation algorithm to define a keyframe graph (but not its target).
                name=None,  # The user-defined name of this object.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\animation\animationSampler\__init__.py",
            "AnimationSampler",
            dict(
                input=0,  # The index of an accessor containing keyframe input values, e.g., time.
                output=0,  # The index of an accessor, containing keyframe output values.
                interpolation="Interpolation.LINEAR",  # Interpolation algorithm.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\animation\channel\__init__.py",
            "Channel",
            dict(
                sampler=0,  # The index of a sampler in this animation used to compute the value for the target.
                target="Target()",  # The index of the node and TRS property to target.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\animation\channel\target\__init__.py",
            "Target",
            dict(
                path="AnimationTargetPath.TRANSLATION",  # The name of the node's TRS property to modify, or the "weights" of the Morph Targets it instantiates. For the "translation" property, the values that are provided by the sampler are the translation along the x, y, and z axes. For the "rotation" property, the values are a quaternion in the order (x, y, z, w), where w is the scalar. For the "scale" property, the values are the scaling factors along the x, y, and z axes.
                node=0,  # The index of the node to target.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))
    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\asset\__init__.py",
            "Asset",
            dict(
                version="2.0",  # The glTF version that this asset targets.
                copyright="getpass.getuser()",  # A copyright message suitable for display to credit the content creator.
                generator="Krita glTF Editor",  # Tool that generated this glTF model. Useful for debugging.
                minVersion=None,  # The minimum glTF version that this asset targets.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\buffer\__init__.py",
            "Buffer",
            dict(
                byteLength=0,  # The total byte length of the buffer view.
                uri=None,  # The uri of the buffer.
                name=None,  # The user-defined name of this object.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\bufferView\__init__.py",
            "BufferView",
            dict(
                buffer=0,  # The index of the buffer.
                byteLength=0,  # The length of the bufferView in bytes.
                byteOffset=0,  # The offset into the buffer in bytes.
                byteStride=None,  # The stride, in bytes.
                target=None,  # The target that the GPU buffer should be bound to.
                name=None,  # The user-defined name of this object.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\camera\__init__.py",
            "Camera",
            dict(
                type="CameraType.PERSPECTIVE",  # Specifies if the camera uses a perspective or orthographic projection.
                orthographic=None,  # An orthographic camera containing properties to create an orthographic projection matrix.
                perspective=None,  # A perspective camera containing properties to create a perspective projection matrix.
                name=None,  # The user-defined name of this object.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\camera\orthographic\__init__.py",
            "Orthographic",
            dict(
                xmag=1.0,  # The floating-point horizontal magnification of the view.
                ymag=1.0,  # The floating-point vertical magnification of the view.
                znear=0.0,  # near clipping plane distance.
                zfar=1000.0,  # far clipping plane distance. (must be greater than znear.)
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\camera\perspective\__init__.py",
            "Perspective",
            dict(
                yfov="0.25 * math.pi",  # The floating-point vertical field of view in radians.
                znear=1.0,  # The floating-point distance to the near clipping plane.
                zfar=1000.0,  # The floating-point distance to the far clipping plane.
                aspectRatio=None,  # The floating-point aspect ratio of the field of view.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\extension\__init__.py",
            "Extension",
            dict(
                items="oDict()"
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\extras\__init__.py",
            "Extras",
            dict(
                items="oDict()"
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\extras\image\__init__.py",
            "Image",
            dict(
                uri=None,  # The uri of the image.
                mimeType=None,  # The image's MIME type.
                bufferView=None,  # The index of the bufferView that contains the image. Use this instead of the image's uri property.
                name=None,  # The user-defined name of this object.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\light\__init__.py",
            "Light",
            dict(
                type="LightType.DIRECTIONAL",  # Specifies the light type. {"directional", "point", "spot"}
                color="Color(1.0, 1.0, 1.0)",  # Color of the light source.
                intensity=1.0,  # Intensity of the light source. `point` and `spot` lights use luminous intensity in candela (lm/sr) while `directional` lights use illuminance in lux (lm/m^2)
                name=None,
                spot=None,
                range=None,  # maximum distance of light. (point / spot)
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\light\spot\__init__.py",
            "Spot",
            dict(
                innerConeAngle="0.0",  # Angle in radians from centre of spotlight where falloff begins.
                outerConeAngle="0.25 * math.pi",  # Angle in radians from centre of spotlight where falloff ends.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\material\__init__.py",
            "Material",
            dict(
                emissiveFactor="Color(0.0, 0.0, 0.0)",  # The emissive color of the material.
                alphaMode="AlphaMode.OPAQUE",  # The alpha rendering mode of the material.
                alphaCutoff=0.5,  # The alpha cutoff value of the material.
                doubleSided=False,  # Specifies whether the material is double sided.
                pbrMetallicRoughness=None,  # A set of parameter values that are used to define the metallic-roughness material model from Physically-Based Rendering (PBR) methodology. When not specified, all the default values of pbrMetallicRoughness apply.
                normalTexture=None,  # The normal map texture.
                occlusionTexture=None,  # The occlusion map texture.
                emissiveTexture=None,  # The emissive map texture.
                name=None,  # The user-defined name of this object.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\material\normalTextureInfo\__init__.py",
            "NormalTextureInfo",
            dict(
                index=0,  # The index of the texture.
                texCoord=0,  # The set index of texture's TEXCOORD attribute used for texture coordinate mapping.
                scale=1.0,  # The scalar multiplier applied to each normal vector of the normal texture.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\material\occlusionTextureInfo\__init__.py",
            "OcclusionTextureInfo",
            dict(
                index=0,  # The index of the texture.
                texCoord=0,  # The set index of texture's TEXCOORD attribute used for texture coordinate mapping.
                strength=1.0,  # A scalar multiplier controlling the amount of occlusion applied.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\material\pbrMetallicRoughness\__init__.py",
            "PbrMetallicRoughness",
            dict(
                baseColorFactor="Color(1.0, 1.0, 1.0)",  # The material's base color factor.
                metallicFactor=1.0,  # The metalness of the material.
                roughnessFactor=1.0,  # The roughness of the material.
                baseColorTexture=None,  # The base color texture.
                metallicRoughnessTexture=None,  # The metallic-roughness texture.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\mesh\__init__.py",
            "Mesh",
            dict(
                primitives="list()",  # An array of primitives, each defining geometry to be rendered with a material.
                weights=None,  # Array of weights to be applied to the Morph Targets.
                name=None,  # The user-defined name of this object.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\mesh\primitive\__init__.py",
            "Primitive",
            dict(
                mode="PrimitiveType.TRIANGLES",  # The type of primitives to render.
                attributes="oDict()",  # A dictionary object, where each key corresponds to mesh attribute semantic and each value is the index of the accessor containing attribute's data.
                indices=None,  # The index of the accessor that contains the indices.
                material=None,  # The index of the material to apply to this primitive when rendering.
                targets=None,  # An array of Morph Targets, each Morph Target is a dictionary mapping attributes (only POSITION, NORMAL, and TANGENT supported) to their deviations in the Morph Target.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\node\__init__.py",
            "Node",
            dict(
                translation="Vector3(0.0, 0.0, 0.0)",  # The node's translation along the x, y, and z axes.
                rotation="Quaternion(0.0, 0.0, 0.0, 1.0)",  # The node's unit quaternion rotation in the order (x, y, z, w), where w is the scalar.
                scale="Vector3(1.0, 1.0, 1.0)",  # The node's non-uniform scale, given as the scaling factors along the x, y, and z axes.
                matrix=None,  # A floating-point 4x4 transformation matrix stored in column-major order.  # interface to TRS!
                children=None,  # The indices of this node's children.
                camera=None,  # The index of the camera referenced by this node.
                skin=None,  # The index of the skin referenced by this node.
                mesh=None,  # The index of the mesh in this node.
                weights=None,  # The weights of the instantiated Morph Target. Number of elements must match number of Morph Targets of used mesh.
                name=None,  # The user-defined name of this object.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\sampler\__init__.py",
            "Sampler",
            dict(
                wrapS="WarpingMode.REPEAT",  # s wrapping mode.
                wrapT="WarpingMode.REPEAT",  # t wrapping mode.
                magFilter="MagnificationFilter.LINEAR",  # Magnification filter.
                minFilter="MinificationFilter.LINEAR",  # Minification filter.
                name=None,  # The user-defined name of this object.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\scene\__init__.py",
            "Scene",
            dict(
                nodes=None,  # The indices of each root node.
                name=None,  # The user-defined name of this object.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\skin\__init__.py",
            "Skin",
            dict(
                joints="list()",  # Indices of skeleton nodes, used as joints in this skin.
                inverseBindMatrices=None,  # The index of the accessor containing the floating-point 4x4 inverse-bind matrices. The default is that each matrix is a 4x4 identity matrix, which implies that inverse-bind matrices were pre-applied.
                skeleton=None,  # The index of the node used as a skeleton root.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\texture\__init__.py",
            "Texture",
            dict(
                sampler=None,  # The index of the sampler used by this texture. When undefined, a sampler with repeat wrapping and auto filtering should be used.
                source=None,  # The index of the image used by this texture. When undefined, it is expected that an extension or other mechanism will supply an alternate texture source, otherwise behavior is undefined.
                name=None,  # The user-defined name of this object.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))

    write_file(r"D:\projects\krita_python_fun\pykrita\glTF_editor\glTF\textureInfo\__init__.py",
            "TextureInfo",
            dict(
                index=0,  # The index of the texture.
                texCoord=0,  # The set index of texture's TEXCOORD attribute used for texture coordinate mapping.
                extensions=None,  # Dictionary object with extension-specific objects.
                extras=None  # Application-specific data.
            ))
