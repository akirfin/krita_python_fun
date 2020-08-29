from krita import Krita, Extension

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from .common.utils_kis import \
        find_document_for, write_extension_action_file, read_setting, write_setting

from .common.utils_py import \
        first, last, underscore

from .common.utils_qt import \
        find_menu, create_menu, create_action

from .glTF import GLTF


class GLTFEditorExtension(Extension):
    """

    """


    def __init__(self, parent):
        super(GLTFEditorExtension, self).__init__(parent)
        self.setObjectName("gltf_editor_extension")


    def setup(self):
        """
        Called once in Krita startup.
        """
        # hook app closing
        notifier = Krita.instance().notifier()
        notifier.applicationClosing.connect(self.shuttingDown)

        extension_name = self.objectName()
        # value = read_setting(extension_name, "setting_name", default=None)

        # create actions here and share "instance" to other places.
        self._show_glTF_editor_action = create_action(
                name="show_gltf_editor_action",
                text="Show glTF Editor",
                triggered=self.show_glTF_editor,
                parent=self)  # I own the action!

        # when is .action file applied?
        # write_extension_action_file(self)


    def shuttingDown(self):
        """
        Called once in Krita shutting down.
        """
        extension_name = self.objectName()
        # write_setting(extension_name, "setting_name", value)


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
        experimental_menu.addAction(self._show_glTF_editor_action)


    def show_glTF_editor(self):
        """
        Show editor
        """
        app = Krita.instance()
        document = app.activeDocument()
        active_node = document.activeNode()
