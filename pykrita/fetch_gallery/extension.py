"""

Let’s have some fun with python coding 01

"""

import re
from urllib import request

from krita import Krita, Extension


class FetchGalleryExtension(Extension):
    gallery_url = "https://krita-artists.org/tag/featured"
    image_element_re = re.compile(r"<meta itemprop='image' content='(https://krita-artists\.org/uploads/default/optimized/2X/[a-zA-Z0-9_/]+\.jpeg)'>")
    limit = 8

    def __init__(self, parent):
        super(FetchGalleryExtension, self).__init__(parent)


    def setup(self):
        pass


    def createActions(self, window):
        prefix = self.objectName()
        fetch_gallery = window.createAction(prefix +"_fetch_gallery", "Fetch Gallery", "")
        fetch_gallery.triggered.connect(self.act_fetch_gallery)


    def act_fetch_gallery(self, cheched=None):
        r = request.urlopen(self.gallery_url)
        text = r.read().decode('utf-8')
        for index, image_url in enumerate(self.image_element_re.findall(text)):
            qimage = get_qimage_from_url(image_url)
            create_document_from_qimage(qimage)
            if index >= self.limit:
                return  # limit reached!



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
