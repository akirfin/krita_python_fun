"""

Let’s have some fun with python coding 01

"""

import re
from urllib import request
from urllib.parse import urlparse

from krita import Krita, Extension

from .common.utils_py import \
        first, last, underscore

from .common.utils_qt import \
        walk_menu


class LayerMetaDataExtension(Extension):
    def __init__(self, parent):
        super(LayerMetaDataExtension, self).__init__(parent)


    def setup(self):
        if not LayerPropertiesHook.is_registered():
            LayerPropertiesHook.register()


    def createActions(self, window):
        pass
