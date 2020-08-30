from enum import Enum

from glTF_editor.common.data_serializer import \
        serializer

from .sparse import \
        Sparse, Indices, Values


class AccessorType(Enum):
    SCALAR = "SCALAR"
    VEC2 = "VEC2"
    VEC3 = "VEC3"
    VEC4 = "VEC4"
    MAT2 = "MAT2"
    MAT3 = "MAT3"
    MAT4 = "MAT4"


class ComponentType(Enum):
    """
    issue: evil magic numbers!
    """
    BYTE = 5120
    UNSIGNED_BYTE = 5121
    SHORT = 5122
    UNSIGNED_SHORT = 5123
    UNSIGNED_INT = 5125
    FLOAT = 5126


class Accessor(object):
    """
    type 	string 	Specifies if the attribute is a scalar, vector, or matrix. 	Yes
    componentType 	integer 	The datatype of components in the attribute. 	Yes
    count 	integer 	The number of attributes referenced by this accessor. 	Yes
    name 	string 	The user-defined name of this object. 	No
    bufferView 	integer 	The index of the bufferView. 	No
    byteOffset 	integer 	The offset relative to the start of the bufferView in bytes. 	No, default: 0
    normalized 	boolean 	Specifies whether integer data values should be normalized. 	No, default: false
    max 	number [1-16] 	Maximum value of each component in this attribute. 	No
    min 	number [1-16] 	Minimum value of each component in this attribute. 	No
    sparse 	object 	Sparse storage of attributes that deviate from their initialization value. 	No
    extensions 	object 	Dictionary object with extension-specific objects. 	No
    extras 	any 	Application-specific data. 	No
    """

    def __init__(self):
        self._type = AccessorType.SCALAR
        self._componentType = ComponentType.FLOAT
        self._count = 0
        self._name = None
        self._bufferView = None
        self._byteOffset = None  # return 0
        self._normalized = None  # return False
        self._max = None
        self._min = None
        self._sparse = None
        self._extensions = None
        self._extra = None
