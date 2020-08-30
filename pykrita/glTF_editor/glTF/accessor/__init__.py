from enum import Enum

from glTF_editor.common.utils_py import \
        UnicodeType

from glTF_editor.common.data_serializer import \
        serializer


class Accessor(object):
    """
    ...
    """

    def __init__(self,
                type=None,
                componentType=None,
                count=None,
                byteOffset=None,
                normalized=None,
                name=None,
                bufferView=None,
                max=None,
                min=None,
                sparse=None,
                extensions=None,
                extras=None):

        self._type = AccessorType.SCALAR
        self._componentType = ComponentType.FLOAT
        self._count = 0
        self._byteOffset = 0
        self._normalized = False
        self._name = None
        self._bufferView = None
        self._max = None
        self._min = None
        self._sparse = None
        self._extensions = None
        self._extras = None

        if type is not None:
            self.type = type
        if componentType is not None:
            self.componentType = componentType
        if count is not None:
            self.count = count
        if byteOffset is not None:
            self.byteOffset = byteOffset
        if normalized is not None:
            self.normalized = normalized
        if name is not None:
            self.name = name
        if bufferView is not None:
            self.bufferView = bufferView
        if max is not None:
            self.max = max
        if min is not None:
            self.min = min
        if sparse is not None:
            self.sparse = sparse
        if extensions is not None:
            self.extensions = extensions
        if extras is not None:
            self.extras = extras


    @classmethod
    def cast(cls, obj):
        if isinstance(obj, cls):
            return cls(
                    type=obj.type,
                    componentType=obj.componentType,
                    count=obj.count,
                    byteOffset=obj.byteOffset,
                    normalized=obj.normalized,
                    name=obj.name,
                    bufferView=obj.bufferView,
                    max=obj.max,
                    min=obj.min,
                    sparse=obj.sparse,
                    extensions=obj.extensions,
                    extras=obj.extras)
        elif isinstance(obj, Mapping):
            return cls(
                    type=obj.get("type"),
                    componentType=obj.get("componentType"),
                    count=obj.get("count"),
                    byteOffset=obj.get("byteOffset"),
                    normalized=obj.get("normalized"),
                    name=obj.get("name"),
                    bufferView=obj.get("bufferView"),
                    max=obj.get("max"),
                    min=obj.get("min"),
                    sparse=obj.get("sparse"),
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
                    componentType=next(it),
                    count=next(it),
                    byteOffset=next(it),
                    normalized=next(it),
                    name=next(it),
                    bufferView=next(it),
                    max=next(it),
                    min=next(it),
                    sparse=next(it),
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


    def getComponentType(self):
        if self._componentType is None:
            return None
        else:
            return iter(self._componentType)
    def setComponentType(self, newComponentType):
        if newComponentType is None:
            self._componentType = None
        else:
            self._componentType = [UnicodeType(n) for n in newComponentType]
    componentType = property(getComponentType, setComponentType)


    def getCount(self):
        if self._count is None:
            return None
        else:
            return iter(self._count)
    def setCount(self, newCount):
        if newCount is None:
            self._count = None
        else:
            self._count = [UnicodeType(n) for n in newCount]
    count = property(getCount, setCount)


    def getByteOffset(self):
        if self._byteOffset is None:
            return None
        else:
            return iter(self._byteOffset)
    def setByteOffset(self, newByteOffset):
        if newByteOffset is None:
            self._byteOffset = None
        else:
            self._byteOffset = [UnicodeType(n) for n in newByteOffset]
    byteOffset = property(getByteOffset, setByteOffset)


    def getNormalized(self):
        if self._normalized is None:
            return None
        else:
            return iter(self._normalized)
    def setNormalized(self, newNormalized):
        if newNormalized is None:
            self._normalized = None
        else:
            self._normalized = [UnicodeType(n) for n in newNormalized]
    normalized = property(getNormalized, setNormalized)


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


    def getBufferView(self):
        if self._bufferView is None:
            return None
        else:
            return iter(self._bufferView)
    def setBufferView(self, newBufferView):
        if newBufferView is None:
            self._bufferView = None
        else:
            self._bufferView = [UnicodeType(n) for n in newBufferView]
    bufferView = property(getBufferView, setBufferView)


    def getMax(self):
        if self._max is None:
            return None
        else:
            return iter(self._max)
    def setMax(self, newMax):
        if newMax is None:
            self._max = None
        else:
            self._max = [UnicodeType(n) for n in newMax]
    max = property(getMax, setMax)


    def getMin(self):
        if self._min is None:
            return None
        else:
            return iter(self._min)
    def setMin(self, newMin):
        if newMin is None:
            self._min = None
        else:
            self._min = [UnicodeType(n) for n in newMin]
    min = property(getMin, setMin)


    def getSparse(self):
        if self._sparse is None:
            return None
        else:
            return iter(self._sparse)
    def setSparse(self, newSparse):
        if newSparse is None:
            self._sparse = None
        else:
            self._sparse = [UnicodeType(n) for n in newSparse]
    sparse = property(getSparse, setSparse)


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
                "componentType={self.componentType!r}, "
                "count={self.count!r}, "
                "byteOffset={self.byteOffset!r}, "
                "normalized={self.normalized!r}, "
                "name={self.name!r}, "
                "bufferView={self.bufferView!r}, "
                "max={self.max!r}, "
                "min={self.min!r}, "
                "sparse={self.sparse!r}, "
                "extensions={self.extensions!r}, "
                "extras={self.extras!r}")").format(**locals())


def to_dict(obj):
    result = oDict()
    def add_valid(attr_name):
        value = getattr(obj, attr_name, None)
        if value is not None:
            result[attr_name] = value.value if isinstance(value, Enum) else value
    add_valid("type")
    add_valid("componentType")
    add_valid("count")
    add_valid("byteOffset")
    add_valid("normalized")
    add_valid("name")
    add_valid("bufferView")
    add_valid("max")
    add_valid("min")
    add_valid("sparse")
    add_valid("extensions")
    add_valid("extras")
    return result


serializer.register(
        data_cls=Accessor,
        from_dict=lambda dct: Accessor.cast(dct),
        to_dict=to_dict)
