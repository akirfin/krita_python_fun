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
        QSettings, QTimer

from layer_meta_data.common.utils_py import \
        first, last, underscore

from layer_meta_data.common.utils_qt import \
        make_menus, create_action

from layer_meta_data.ui.layer_properties_hook import \
        LayerPropertiesHook


class LayerMetaDataExtension(Extension):
    settings_path = "plugin_settings/layer_meta_data"
    show_meta_data_setting = settings_path + "/show_meta_data"

    parent_menu_path = (
            ("tools", "&Tools"),
                ("experimental_plugins", "&Experimental Plugins"))

    def __init__(self, parent):
        super(LayerMetaDataExtension, self).__init__(parent)


    def setup(self):
        """
        Called once in Krita startup.
        """
        # hook app closing
        notifier = Krita.instance().notifier()
        notifier.applicationClosing.connect(self.shuttingDown)

        # when is .action file applied?
        settings = QSettings()
        show_meta_data = settings.value(
                self.show_meta_data_setting,
                defaultValue=True,
                type=bool)

        # create actions here and share "instance" to other places.
        self._show_meta_data_action = create_action(
                name="show_meta_data",
                text="Show Meta Data",
                checkable=True,
                checked=show_meta_data,
                triggered=self.show_meta_data,
                parent=self)  # I own the action!

        # set initial state
        self.show_meta_data(show_meta_data)


    def shuttingDown(self):
        """
        Called once in Krita shutting down.
        """
        settings = QSettings()
        settings.setValue(
                self.show_meta_data_setting,
                self._show_meta_data_action.isChecked())


    def createActions(self, window):
        """
        Krita bug, in Linux. (create actions later.)
        """
        QTimer.singleShot(0, lambda menu_bar=window.qwindow().menuBar(): self.delayed_create_actions(menu_bar))


    def delayed_create_actions(self, menu_bar):
        """
        Called once for each new window opened in Krita.
        """
        parent_menu = make_menus(
                menu_bar,
                self.parent_menu_path,
                exist_ok=True)

        # add action "instance"
        parent_menu.addAction(
                self._show_meta_data_action)


    def show_meta_data(self, checked=None):
        if (checked is None) or (checked is True):
            if not LayerPropertiesHook.is_registered():
                LayerPropertiesHook.register()
        else:
            if LayerPropertiesHook.is_registered():
                LayerPropertiesHook.unregister()
