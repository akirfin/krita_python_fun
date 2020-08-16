"""

Layer meta data extension

Note:
    - this module is currently unused. (no user interface needed?)

"""

import re
from urllib import request
from urllib.parse import urlparse

from krita import Krita, Extension

from PyQt5.QtCore import \
        QSettings

from layer_meta_data.common.utils_py import \
        first, last, underscore

from layer_meta_data.common.utils_qt import \
        make_menus, create_action

from layer_meta_data.ui.layer_properties_hook import \
        LayerPropertiesHook


class LayerMetaDataExtension(Extension):
    settings_path = "plugin_settings/layer_meta_data"


    def __init__(self, parent):
        super(LayerMetaDataExtension, self).__init__(parent)
        self._show_meta_data_state = False


    def setup(self):
        """
        Called once in Krita startup.
        """
        # hook app closing
        notifier = Krita.instance().notifier()
        notifier.applicationClosing.connect(self.shuttingDown)

        # or is this done automaticaly for registered actions using .action file?
        settings = QSettings()
        self._show_meta_data_state = settings.value(
                self.settings_path +"/show_meta_data_state",
                defaultValue=True,
                type=bool)

        # create actions here and share "instance" to other places.
        self._show_meta_data_action = create_action(
                name="show_meta_data",
                text="Show Meta Data",
                checkable=True,
                checked=self._show_meta_data_state,
                triggered=self.show_meta_data,
                parent=self)  # I own the action!

        # set initial state
        self.show_meta_data(self._show_meta_data_state)


    def shuttingDown(self):
        """
        Called once in Krita shutting down.
        """
        settings = QSettings()
        settings.setValue(
                self.settings_path +"/show_meta_data_state",
                self._show_meta_data_state)


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
                self._show_meta_data_action)


    def show_meta_data(self, checked=None):
        if (checked is None) or (checked is True):
            self._show_meta_data_state = True
            if not LayerPropertiesHook.is_registered():
                LayerPropertiesHook.register()
        else:
            self._show_meta_data_state = False
            if LayerPropertiesHook.is_registered():
                LayerPropertiesHook.unregister()
