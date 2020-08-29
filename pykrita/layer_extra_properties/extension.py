"""

Layer extra properties extension

ToDo:
    - option to suppress JSON path in LayerExtraPropertiesWidget (used when custom layer properties widget exits.)

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
        find_menu, create_menu, create_action

from .common.utils_kis import \
        write_extension_action_file, read_setting, write_setting

from .ui.layer_properties_hook import \
        LayerPropertiesHook


class LayerExtraPropertiesExtension(Extension):
    show_layer_extra_properties_setting = "show_layer_extra_properties"

    def __init__(self, parent):
        super(LayerExtraPropertiesExtension, self).__init__(parent)
        self.setObjectName("layer_extra_properties_extension")


    def setup(self):
        """
        Called once in Krita startup.
        """
        # hook app closing
        notifier = Krita.instance().notifier()
        notifier.applicationClosing.connect(self.shuttingDown)

        extension_name = self.objectName()
        show_layer_extra_properties = read_setting(
                extension_name,
                self.show_layer_extra_properties_setting,
                default=True)

        # create actions here and share "instance" to other places.
        self._show_layer_extra_properties = create_action(
                name="show_layer_extra_properties",
                text=i18n("Show Layer Extra Properties"),
                checkable=True,
                checked=show_layer_extra_properties,
                triggered=self.show_layer_extra_properties,
                parent=self)  # I own the action!

        # when is .action file applied?
        # write_extension_action_file(self)

        # set initial state
        self.show_layer_extra_properties(show_layer_extra_properties)


    def shuttingDown(self):
        """
        Called once in Krita shutting down.
        """
        extension_name = self.objectName()
        write_setting(
                extension_name,
                self.show_layer_extra_properties_setting,
                self._show_layer_extra_properties.isChecked())
        LayerPropertiesHook.unregister()


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
        experimental_menu.addAction(self._show_layer_extra_properties)


    def show_layer_extra_properties(self, checked=None):
        if (checked is None) or (checked is True):
            if not LayerPropertiesHook.is_registered():
                LayerPropertiesHook.register()
        else:
            if LayerPropertiesHook.is_registered():
                LayerPropertiesHook.unregister()
