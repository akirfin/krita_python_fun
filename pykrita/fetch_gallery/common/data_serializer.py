# -*- coding: utf-8 -*-

"""

And once again new serializer to / from JSON.
Getting better at this :)

"""

import re
import json
import base64
from fractions import Fraction
from uuid import UUID
from datetime import datetime, date, time
from array import array
from collections import OrderedDict as oDict
from collections import namedtuple
try:
    from collections.abc import Mapping, Iterable
except:
    from collections import Mapping, Iterable


UnicodeType = type(u"")
BytesType = type(b"")


class Coder(tuple):
    __slots__ = ()

    def __new__(cls, data_cls=None, from_dict=None, to_dict=None):
        return super(Coder, cls).__new__(cls, (data_cls, from_dict, to_dict))


    @classmethod
    def cast(cls, obj):
        if isinstance(obj, cls):
            return cls(
                    data_cls=obj.data_cls,
                    from_dict=obj.from_dict,
                    to_dict=obj.to_dict)
        elif isinstance(obj, Mapping):
            return cls(
                    data_cls=obj[u"data_cls"],
                    from_dict=obj[u"from_dict"],
                    to_dict=obj[u"to_dict"])
        elif isinstance(obj, (UnicodeType, BytesType)):
            pass
        elif isinstance(obj, Iterable):
            it = iter(obj)
            return cls(
                    data_cls=it.next(),
                    from_dict=it.next(),
                    to_dict=it.next())
        raise RuntimeError("Can not cast {obj}!".format(**locals()))


    @property
    def data_cls(self):
        """ there is no winning with naming of this. """
        return self[0]


    @property
    def from_dict(self):
        return self[1]


    @property
    def to_dict(self):
        return self[2]


    def __str__(self):
        cls = type(self)
        return ("{cls.__name__}("
                    "data_cls={self.data_cls!s}, "
                    "from_dict={self.from_dict!s}, "
                    "to_dict={self.to_dict!s})").format(**locals())


    def __repr__(self):
        cls = type(self)
        return ("{cls.__name__}("
                    "data_cls={self.data_cls!r}, "
                    "from_dict={self.from_dict!r}, "
                    "to_dict={self.to_dict!r})").format(**locals())


class DataSerializer(object):
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


    def __init__(self, dict_factory=None, registry=None):
        self._dict_factory = oDict
        self._registry = oDict()
        if dict_factory is not None:
            self.dict_factory = dict_factory
        if registry is not None:
            self.registry = registry


    def get_dict_factory(self):
        return self._dict_factory
    def set_dict_factory(self, new_dict_factory):
        # validation of new_dict_factory is left as an exercise for the reader!
        old_dict_factory = self.dict_factory
        if new_dict_factory != old_dict_factory:
            self._dict_factory = new_dict_factory
    dict_factory = property(get_dict_factory, set_dict_factory)


    def get_registry(self):
        return iter(self._registry)
    def set_registry(self, new_registry):
        it = new_registry.items() if isinstance(new_registry, Mapping) else iter(new_registry)
        new_registry = oDict((k, Coder.cast(v)) for k, v in it)
        old_registry = self.registry
        if new_registry != old_registry:
            self._registry.clear()
            self._registry.update(new_registry)
    registry = property(get_registry, set_registry)


    def register(self, data_cls, from_dict=None, to_dict=None):
        self._registry[data_cls.__name__] = Coder(
                data_cls=data_cls,
                from_dict=from_dict,
                to_dict=to_dict)


    def is_registered_type(self, obj_type):
        return obj_type in self._registry


    def is_registered_instance(self, obj):
        return self.is_registered_type(type(obj))


    def get_coder(self, obj):
        obj_type = type(obj)
        for cls_name, coder in self._registry.items():
            if obj_type == coder.data_cls:
                return cls_name, coder


    def to_dict(self, obj, type_hints=True):
        result = None
        cls_name_coder = self.get_coder(obj)
        if cls_name_coder:
            cls_name, coder = cls_name_coder
            result = self._dict_factory()
            if type_hints:
                result["__type__"] = cls_name
            result.update(
                    (self.to_dict(k, type_hints=type_hints), self.to_dict(v, type_hints=type_hints))
                    for k, v in coder.to_dict(obj).items())
            return result
        elif isinstance(obj, (type(None), bool, int, float, UnicodeType, BytesType)):
            return obj
        elif isinstance(obj, Mapping):
            return self._dict_factory(
                    (self.to_dict(k, type_hints=type_hints), self.to_dict(v, type_hints=type_hints))
                    for k, v in obj.items())
        elif isinstance(obj, Iterable):
            return list(self.to_dict(v, type_hints=type_hints) for v in obj)
        raise RuntimeError("Can NOT handle {obj!r}!".format(**locals()))


    def from_dict(self, obj):
        if isinstance(obj, (type(None), bool, int, float, UnicodeType, BytesType)):
            return obj
        elif isinstance(obj, Mapping):
            cls_name = obj.get("__type__")
            if cls_name in self._registry:
                dct = self._dict_factory((self.from_dict(k), self.from_dict(v)) for k, v in obj.items() if k != "__type__")
                coder = self._registry[cls_name]
                if coder.from_dict is None:
                    return coder.data_cls(**dct)
                else:
                    return coder.from_dict(dct)
            else:
                dct = self._dict_factory((self.from_dict(k), self.from_dict(v)) for k, v in obj.items())
                return dct
        elif isinstance(obj, Iterable):
            return [self.from_dict(v) for v in obj]
        else:
            return obj  # what ?


    def __str__(self):
        cls = type(self)
        registry = "[" + "\n".join("{!s}".format(v) for v in self._registry.values()) + "]"
        return ("{cls.__name__}("
                    "dict_factory={self._dict_factory!s}, "
                    "registry={registry}").format(**locals())


    def __repr__(self):
        cls = type(self)
        registry = "[" + "\n".join("{!r}".format(v) for v in self._registry.values()) + "]"
        return ("{cls.__name__}("
                    "dict_factory={self._dict_factory!r}, "
                    "registry={registry}").format(**locals())


    def dump(self, obj, file_handle, type_hints=True):
        json.dump(self.to_dict(obj, type_hints=type_hints), file_handle, indent=2)


    def dumps(self, obj, type_hints=True):
        return json.dumps(self.to_dict(obj, type_hints=type_hints), indent=2)


    def load(self, file_handle):
        return self.from_dict(json.load(file_handle, object_pairs_hook=self._dict_factory))


    def loads(self, obj):
        return self.from_dict(json.loads(obj, object_pairs_hook=self._dict_factory))


##
#
# the primary insnace!
#

serializer = DataSerializer.instance()


##
#
# register some basic python types, that have no support in json
#

serializer.register(
        data_cls=Fraction,
        from_dict=lambda dct: Fraction(numerator=dct[u"numerator"], denominator=dct[u"denominator"]),
        to_dict=lambda obj: oDict([
                (u"numerator", obj.numerator),
                (u"denominator", obj.denominator)
                ]))

serializer.register(
        data_cls=UUID,
        from_dict=lambda dct: UUID(dct[u"uuid"]),
        to_dict=lambda obj: oDict([
                (u"uuid", str(obj))
                ]))

serializer.register(
        data_cls=set,
        from_dict=lambda dct: set(dct[u"items"]),
        to_dict=lambda obj: oDict([
                (u"items", tuple(obj))
                ]))

serializer.register(
        data_cls=bytes,
        from_dict=lambda dct: bytes(base64.b64decode(dct[u"base64"])),
        to_dict=lambda obj: oDict([
                (u"base64", base64.b64encode(obj).decode('ascii'))
                ]))


ToDo_check_details = """
serializer.register(
        data_cls=datetime,
        from_dict=lambda dct: DataTime(dct[u"utc_ms"]),
        to_dict=lambda obj: oDict([
                (u"utc_ms", tuple(obj))
                ]))

serializer.register(
        data_cls=time,
        from_dict=lambda dct: Time(dct[u"utc_ms"]),
        to_dict=lambda obj: oDict([
                (u"utc_ms", tuple(obj))
                ]))

serializer.register(
        data_cls=date,
        from_dict=lambda dct: Date(dct[u"utc_ms"]),
        to_dict=lambda obj: oDict([
                (u"utc_ms", tuple(obj))
                ]))

serializer.register(
        data_cls=array,
        from_dict=lambda dct: array(dct[u"typecode"], base64.urlsafe_b64decode(dct[u"base64"])),
        to_dict=lambda obj: oDict([
                (u"typecode", obj.typecode)
                (u"base64", base64.urlsafe_b64encode(obj.tobytes()))
                ]))

serializer.register(
        data_cls=bytearray,
        from_dict=lambda dct: bytearray(base64.urlsafe_b64decode(dct[u"base64"])),
        to_dict=lambda obj: oDict([
                (u"base64", base64.urlsafe_b64decode(obj))
                ]))
"""
