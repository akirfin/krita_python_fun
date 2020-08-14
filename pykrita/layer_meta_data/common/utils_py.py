"""

Small common scripts for Python.
uses standard library

"""

import os
import sys
import re
import math
import time
import base64
import getpass
from contextlib import contextmanager

Undefined = object()
UnicodeType = type(u"")
BytesType = type(b"")


def print_console(*obj, newline="\n"):
    sys.__stdout__.write(str(obj[0]) if len(obj) == 1 else str(obj))
    sys.__stdout__.write(newline)
    sys.__stdout__.flush()


@contextmanager
def open_new(file_path, exists_ok=True):
    try:
        fd = os.open(file_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        f = os.fdopen(fd, "w")
    except OSError as e:
        if not ((e.errno == errno.EEXIST) and exists_ok):
            raise  # skipped only if exits and exists_ok
    else:
        try:
            yield f
        finally:
            f.close()


def first(iterable, default=Undefined):
    try:
        return next(iter(iterable))
    except:
        if default is Undefined:
            raise
        else:
            return default


def last(iterable, default=Undefined):
    try:
        return next(reversed(iterable))
    except StopIteration:
        if default is Undefined:
            raise
        else:
            return default


def int_floor(x):
    return int(math.floor(x))


def str_cast(obj):
    return u"" if obj is None else UnicodeType(obj)


def mix(a, b, ratio):
    r = float(ratio)
    return (1.0 - r) * float(a) + r * float(b)


def user():
    return getpass.getuser()


def now_utc_ms():
    return int(time.time() * 1000)


def uniques(seq):
    memo = set()
    memo_add = memo.add
    for item in seq:
        if item not in memo:
            memo_add(item)
            yield item


def new_id(memo=None, byte_length=5, retry=64):
    memo = set() if memo is None else memo
    while retry > 0:
        id_ = base64.b32encode(os.urandom(byte_length)).decode("utf-8")
        if id_ not in memo:
            memo.add(id_)
            return id_
        retry -= 1
    raise RuntimeError("Failed to generate unique new_id!")


def natural(s, _split_re=re.compile(r"(\d+)", flags=re.UNICODE)):
    """ for natural sorting. now with unicode support!"""
    return tuple((int(c) if c.isdecimal() else c) for c in _split_re.split(s))


def f_range(*args, **kwargs):
    """
    ToDo: test this!
    """
    include_stop = bool(kwargs.get("include_stop", True))
    if len(args) == 1:
        start = 0.0
        end = args[0]
        step = 1.0
    elif len(args) == 2:
        start = args[0]
        end = args[1]
        step = 1.0
    elif len(args) == 3:
        start = args[0]
        end = args[1]
        step = args[2]

    op = None
    if step == 0.0:
        raise ValueError("Going nowhere fast. (step = 0.0)")
    elif (step > 0.0) and include_stop:
        op = lambda s, c, e: s <= c <= e
    elif (step > 0.0) and not include_stop:
        op = lambda s, c, e: s <= c < e
    elif (step < 0.0) and include_stop:
        op = lambda s, c, e: s >= c >= e
    elif (step < 0.0) and not include_stop:
        op = lambda s, c, e: s >= c > e

    cursor = start
    while op(start, cursor, end):
        yield cursor
        cursor += step


def cap_words(text):
    return " ".join(w.capitalize() for w in text.split("_"))


def camel_to_under(camel_text, _splitter_re=re.compile(r"([A-Z]+[^A-Z]*)", flags=re.UNICODE)):
    return "_".join((token.strip().lower() for token in _splitter_re.split(camel_text) if token.strip()))


def nice_name(text, _split_re=re.compile(r"([A-Z]+[^A-Z]*)", flags=re.UNICODE)):
    return "_".join((t.lower() for t in _split_re.split(text) if t))


def underscore(text,
               _splitter_re=re.compile(r"([A-Z]+[^A-Z]*)"),
               _dethunder_re=re.compile(r"_+")):
    tokens = []
    for token in _splitter_re.split(text):
        for t in filter(None, _dethunder_re.split(token)):
            tokens.append(t.lower())
    return "_".join(tokens)


def fit_size(size, target_size):
    """
    fit (width, height) to (trg_width, trg_height), keep aspect.
    """
    width, height = size
    aspect = width / float(height)

    target_width, target_height = target_size
    target_aspect = target_width / float(target_height)

    return (target_height * aspect, target_height) if target_aspect > aspect else (target_width, target_width / aspect)


def vector_length(*args):
    return math.sqrt(sum(a**2.0 for a in args))


def to_spherical_coord(x, y, z):
    r = vector_length(x, y, z)
    theta = math.atan2(x, -z)  # moving seam to back of identity camera
    phi = math.acos(y / r)
    return theta / tau + 0.5, phi / pi


def spherical_coordinate_to_cartesian(a, i, r=1.0):
    """
    a = azimuth, i = inclination, r = radius
    """
    a = float(a)
    i = float(i)
    r = float(r)
    x = r * math.sin(i) * math.cos(a)
    y = r * math.sin(i) * math.sin(a)
    z = r * math.cos(i)
    return x, y, z
