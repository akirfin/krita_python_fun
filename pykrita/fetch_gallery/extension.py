"""

Fetch gallery

ToDo:
    - custom dialog
    - dir(krita) there was fome pixelformat thingies..

"""

import re
from urllib import request
from urllib.parse import urlparse

from krita import Krita, Extension

from PyQt5.QtCore import \
        QSettings, QTimer

from .common.utils_py import \
        first, last, underscore

from .common.utils_qt import \
        fetch_qimage_from_url, find_menu, create_menu, create_action

from .common.utils_kis import \
        create_document_from_qimage, write_extension_action_file, read_setting, write_setting


class FetchGalleryExtension(Extension):
    gallery_url_setting = "gallery_url"
    load_limit_setting = "load_limit"
    image_element_re_setting = "image_element_re"

    def __init__(self, parent):
        super(FetchGalleryExtension, self).__init__(parent)
        self.setObjectName("fetch_gallery_extension")


    def setup(self):
        """
        Called once in Krita startup.
        """
        # hook app closing
        app = Krita.instance()
        extension_name = self.objectName()

        notifier = app.notifier()
        notifier.applicationClosing.connect(self.shuttingDown)

        self._gallery_url = read_setting(
                extension_name,
                self.gallery_url_setting,
                default="https://krita-artists.org/tag/featured")
        self._image_element_re = re.compile(read_setting(
                extension_name,
                self.image_element_re_setting,
                default=r"<meta itemprop='image' content='(https://krita-artists\.org/uploads/default/optimized/2X/[a-zA-Z0-9_/]+\.jpeg)'>"))
        self._load_limit = read_setting(
                extension_name,
                self.load_limit_setting,
                default=4)

        # create actions here and share "instance" to other places.
        self._fetch_gallery_action = create_action(
                name="fetch_gallery",
                text=i18n("Fetch Gallery"),
                triggered=self.fetch_gallery,
                parent=self)  # I own the action!

        # when is .action file applied?
        # write_extension_action_file(self)


    def shuttingDown(self):
        """
        Called once in Krita shutting down.
        """
        extension_name = self.objectName()
        write_setting(
                extension_name,
                self.gallery_url_setting,
                self._gallery_url)
        write_setting(
                extension_name,
                self.image_element_re_setting,
                self._image_element_re.pattern)
        write_setting(
                extension_name,
                self.load_limit_setting,
                self._load_limit)


    def createActions(self, window):
        """
        Called once for each new window opened in Krita.
        """
        menu_bar = window.qwindow().menuBar()
        tools_menu = find_menu(menu_bar, "tools")
        experimental_menu = find_menu(tools_menu, "experimental")
        if experimental_menu is None:
            experimental_menu = create_menu("experimental", i18n("Experimental"), parent=tools_menu)
            tools_menu.addAction(experimental_menu.menuAction())

        # add action "instance"
        experimental_menu.addAction(self._fetch_gallery_action)


    def fetch_gallery(self, cheched=None):
        r = request.urlopen(self._gallery_url)
        text = r.read().decode('utf-8')
        for index, image_url in enumerate(self._image_element_re.findall(text)):
            qimage = fetch_qimage_from_url(image_url)
            name_ext = urlparse(image_url).path.rsplit("/")[-1]
            name = name_ext.split(".")[0]
            create_document_from_qimage(qimage, name=name, add_view=True)
            if index >= self._load_limit:
                break
        # and finally do nice layout.
        app = Krita.instance()
        app.action("windows_tile").trigger()
