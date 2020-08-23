"""

I can see you!

https://code.qt.io/cgit/pyside/pyside-setup.git/tree/examples/multimedia/camera.py

ToDo:
    - handle custom layer properties widget

"""

from krita import Krita, Extension

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtCore import \
        QObject, QSettings, QTimer

from PyQt5.QtGui import \
        QImage

from PyQt5.QtWidgets import \
        QPlainTextEdit, QWidget, QComboBox, QPushButton

from PyQt5.QtMultimedia import \
        QCameraInfo, QCamera, QCameraImageCapture

from camera_layer.common.utils_kis import \
        find_document_for, write_extension_action_file, read_setting, write_setting

from camera_layer.common.utils_py import \
        first, last, underscore

from camera_layer.common.utils_qt import \
        find_menu, create_menu, create_action

from camera_layer.camera_layer import \
        CameraLayer

from camera_layer.data_types.camera_layer_data import \
        CameraLayerData


class CameraLayerExtension(Extension):
    """
    Add layer type to Krita.
    (this NOT official way to add layer types.)
    """

    def __init__(self, parent):
        super(CameraLayerExtension, self).__init__(parent)
        self.setObjectName("camera_layer_extension")
        self._camera_layers = list()  # [(node, camera_layer), ...]


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
        self._create_camera_layer_action = create_action(
                name="create_camera_layer",
                text="Create Camera Layer",
                triggered=self.create_camera_layer,
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
        experimental_menu.addAction(self._create_camera_layer_action)


    def attach_camera_layer(self, node):
        for n, camera_layer in self._camera_layers:
            if n == node:
                raise RuntimeError("Node is already attached to camera layer! (did get: {node})".format(**locals()))
        camera_layer = CameraLayer()
        camera_layer.node = node
        camera_layer.push_data()
        self._camera_layers.append((node, camera_layer))
        return camera_layer


    def detach_camera_layer(self, node):
        self._camera_layers[:] = ((n, cl) for n, cl in self._camera_layers if n != node)


    def get_camera_layer(self, node):
        for n, camera_layer in self._camera_layers:
            if n == node:
                return camera_layer


    def create_camera_layer(self):
        """
        create new layer, insert above active node.
        """
        app = Krita.instance()
        document = app.activeDocument()
        active_node = document.activeNode()
        parent_node = active_node.parentNode()

        new_node = document.createNode("Camera layer", "paintlayer")
        parent_node.addChildNode(new_node, active_node)
        self.attach_camera_layer(new_node)
