"""
Let’s have some fun with python coding 02
"""

import re
from urllib import request

from krita import Krita, Extension

from PyQt5.QtGui import QImage


class FetchGallery(Extension):
    def __init__(self, parent):
        super(LetsHaveFun01, self).__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        prefix = self.objectName()
        fetch_gallery = window.createAction(prefix +"_fetch_gallery", "Fetch Gallery", "")
        fetch_gallery.triggered.connect(self.act_fetch_gallery)


    def act_fetch_gallery(self, cheched=None):
        image_element_re = re.compile(r"<meta itemprop='image' content='https://krita-artists\.org/uploads/default/optimized/2X/[a-zA-Z0-9_/]+\.jpeg'>")
        url = "https://krita-artists.org/tag/featured"

        r = request.urlopen(url)
        text = r.read().decode('utf-8')
        for index, meta_str in enumerate(image_element_re.findall(text)):
            qimage = get_qimage_from_url(meta_str[32:-2])  # crop url from string
            set_node_pixel_data(node, qimage)
            if index > 8:
                return  # limit to 8 first images




def get_qimage_from_url(image_url):
    app = Krita.instance()
    name = image_url.rsplit("/", 1)[-1]  # strip path
    name = name.split(".", 1)[0]  # strip ext
    r = request.urlopen(image_url)
    if r.getcode() == 200:
        image = QImage()
        image.loadFromData(r.read())
        return qimage_to_document(image, name)


def qimage_to_document(qimage, name=""):
    app = Krita.instance()
    if not qimage.isNull():
        qimage.convertToFormat(QImage.Format_RGBA8888)
        w = qimage.width()
        h = qimage.height()

        document = app.createDocument(w, h, name, "RGBA", "U8", "", 72.0)
        app.activeWindow().addView(document)

        node = document.topLevelNodes()[0]

        ptr = qimage.constBits()
        ptr.setsize(qimage.byteCount())
        node.setPixelData(bytes(ptr.asarray()), 0, 0, w, h)
        node.setOpacity(255)
        document.refreshProjection()
        return document


def get_images_from_gallery():
    image_element_re = re.compile(r"<meta itemprop='image' content='https://krita-artists\.org/uploads/default/optimized/2X/[a-zA-Z0-9_/]+\.jpeg'>")
    url = "https://krita-artists.org/tag/featured"
    r = request.urlopen(url)
    text = r.read().decode('utf-8')
    for index, meta_str in enumerate(image_element_re.findall(text)):
        get_qimage_from_url(meta_str[32:-2])  # crop url from string
        if index > 8:
            return  # limit to 8 first images
