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
        menubar = window.qwindow().menuBar()
        first_tools = first(a for a, _ in walk_menu(menubar) if a.objectName() == "tools")

        fetch_gallery_action = first_tools.menu().addAction("Fetch Gallery")
        fetch_gallery_action.setObjectName("create_camera_layer")
        fetch_gallery_action.triggered.connect(self.act_fetch_gallery)


    def act_fetch_gallery(self, cheched=None):
        r = request.urlopen(self.gallery_url)
        text = r.read().decode('utf-8')
        for index, image_url in enumerate(self.image_element_re.findall(text)):
            qimage = get_qimage_from_url(image_url)
            create_document_from_qimage(qimage)
            if index >= self.limit:
                return  # limit reached!
