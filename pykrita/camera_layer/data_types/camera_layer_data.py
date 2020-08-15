from collections import OrderedDict as oDict
try:
    from collections.abc import Mapping, Iterable
except:
    from collections import Mapping, Iterable

from camera_layer.common.utils_py import \
        UnicodeType, BytesType

from layer_meta_data.common.data_serializer import \
        serializer


class CameraLayerData(object):
    def __init__(self, camera_id=None, mode=None, transform=None):
        self._camera_id = ""
        self._mode = ""
        self._transform = None
        if camera_id is not None:
            self.camera_id = camera_id
        if mode is not None:
            self.mode = mode
        if transform is not None:
            self.transform = transform


    @classmethod
    def cast(cls, obj):
        if isinstance(obj, cls):
            return cls(
                    camera_id=obj.camera_id,
                    mode=obj.mode,
                    transform=obj.transform)
        elif isinstance(obj, Mapping):
            return cls(
                    camera_id=obj[u"camera_id"],
                    mode=obj[u"mode"],
                    transform=obj[u"transform"])
        elif isinstance(obj, (UnicodeType, BytesType)):
            unserialized = serializer.loads(obj)
            if not isinstance(unserialized, (UnicodeType, BytesType)):
                return cls.cast(unserialized)
        elif isinstance(obj, Iterable):
            it = iter(obj)
            return cls(
                    camera_id=next(it),
                    mode=next(it),
                    transform=next(it))
        raise RuntimeError("Unable to Cast {obj!r} to {cls} instance.".format(**locals()))


    def get_camera_id(self):
        return self._camera_id


    def set_camera_id(self, new_camera_id):
        new_camera_id = UnicodeType(new_camera_id)
        old_camera_id = self.get_camera_id()
        if new_camera_id != old_camera_id:
            self._camera_id = new_camera_id


    camera_id = property(get_camera_id, set_camera_id)


    def get_mode(self):
        return self._mode


    def set_mode(self, new_mode):
        new_mode = UnicodeType(new_mode)
        old_mode = self.get_mode()
        if new_mode != old_mode:
            self._mode = new_mode


    mode = property(get_mode, set_mode)


    def get_transform(self):
        return self._transform


    def set_transform(self, new_transform):
        new_transform = None
        old_transform = self.get_transform()
        if new_transform != old_transform:
            self._transform = new_transform


    transform = property(get_transform, set_transform)


    def __str__(self):
        return serializer.dumps(self)


    def __repr__(self):
        cls = type(self)
        return ("{cls.__name__}("
                "camera_id={self.camera_id!r}, "
                "mode={self.mode!r}, "
                "transform={self.transform!r})").format(**locals())


serializer.register(
        data_cls=CameraLayerData,
        from_dict=lambda dct: CameraLayerData.cast(dct) ,
        to_dict=lambda camera_layer_data: oDict([
                ("camera_id", camera_layer_data.camera_id),
                ("mode", camera_layer_data.mode),
                ("transform", camera_layer_data.transform)
                ]))
