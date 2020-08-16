"""

Let’s have some fun with python coding 01

"""

import re
from urllib import request
from urllib.parse import urlparse

from krita import Krita, Extension

from PyQt5.QtCore import \
        QSettings

from fetch_gallery.common.utils_py import \
        first, last, underscore

from fetch_gallery.common.utils_qt import \
        fetch_qimage_from_url, make_menus, create_action

from fetch_gallery.common.utils_kis import \
        create_document_from_qimage


class FetchGalleryExtension(Extension):
    settings_path = "plugin_settings/fetch_gallery"

    gallery_url = "https://krita-artists.org/tag/featured"
    image_element_re = re.compile(r"<meta itemprop='image' content='(https://krita-artists\.org/uploads/default/optimized/2X/[a-zA-Z0-9_/]+\.jpeg)'>")
    limit = 4

    def __init__(self, parent):
        super(FetchGalleryExtension, self).__init__(parent)


    def setup(self):
        """
        Called once in Krita startup.
        """
        # hook app closing
        notifier = Krita.instance().notifier()
        notifier.applicationClosing.connect(self.shuttingDown)

        settings = QSettings()
        # some_value = settings.value(self.settings_path +"/some_name", defaultValue=?, type=?)

        # create actions here and share "instance" to other places.
        self._fetch_gallery_action = create_action(
                name="fetch_gallery",
                text="Fetch Gallery",
                triggered=self.act_fetch_gallery,
                parent=self)  # I own the action!


    def shuttingDown(self):
        """
        Called once in Krita shutting down.
        """
        settings = QSettings()
        # settings.setValue(self.settings_path +"/some_name", some_value)


    def createActions(self, window):
        """
        Called once for each new window opened in Krita.
        """
        menu_bar = window.qwindow().menuBar()
        parent_menu = make_menus(
                menu_bar,
                [("tools", "&Tools"),
                    ("experimental_plugins", "&Experimental Plugins")],
                exist_ok=True)

        # add action "instance"
        parent_menu.addAction(
                self._fetch_gallery_action)


    def act_fetch_gallery(self, cheched=None):
        r = request.urlopen(self.gallery_url)
        text = r.read().decode('utf-8')
        for index, image_url in enumerate(self.image_element_re.findall(text)):
            qimage = fetch_qimage_from_url(image_url)
            name_ext = urlparse(image_url).path.rsplit("/")[-1]
            name = name_ext.split(".")[0]
            create_document_from_qimage(qimage, name=name, add_view=True)
            if index >= self.limit:
                break # limit reached!
        app = Krita.instance()
        app.action("windows_tile").trigger()
