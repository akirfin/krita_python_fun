import re
from urllib import request

from PyQt5.QtGui import QImage


@contextmanager
def create_painter(obj):
    """
    Create QPainter context.
    (newer again app hangs, because exeption while painting!)
    """
    p = QPainter(obj)
    try:
        yield p
    finally:
        p.end()


def get_enum_str(owner_cls, enum_cls, enum_value):
    """
    Translate Qt enum to enum name string.
    I am not a number! I'm a free man!
    """
    for attr_name in dir(owner_cls):
        attr = getattr(owner_cls, attr_name)
        if isinstance(attr, enum_cls) and (attr == enum_value):
            return attr_name


def fetch_qimage_from_url(image_url):
    """
    Download image from url. (blocking!)
    Uses python standard library. (can be done with Qt)
    """
    app = Krita.instance()
    name = image_url.rsplit("/", 1)[-1]  # strip path
    name = name.split(".", 1)[0]  # strip ext
    r = request.urlopen(image_url)
    if r.getcode() == 200:
        image = QImage()
        image.loadFromData(r.read())
        return qimage_to_document(image, name)
