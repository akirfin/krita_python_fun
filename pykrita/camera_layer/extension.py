"""

Let’s have some fun with python coding 02

I can see you!

"""

from krita import Krita, Extension

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtCore import \
        QObject, QSettings

from PyQt5.QtGui import \
        QImage

from PyQt5.QtWidgets import \
        QPlainTextEdit, QWidget, QComboBox, QPushButton

from PyQt5.QtMultimedia import \
        QCameraInfo, QCamera, QCameraImageCapture

from camera_layer.common.utils_kis import \
        find_document_for

from camera_layer.common.utils_py import \
        first, last, underscore

from camera_layer.common.utils_qt import \
        make_menus, create_action

from camera_layer.camera_layer import \
        CameraLayer

from camera_layer.data_types.camera_layer_data import \
        CameraLayerData



class CameraLayerExtension(Extension):
    """
    Add layer type to Krita.
    (this NOT official way to add layer types.)
    """
    settings_path = "plugin_settings/camera_layer"

    def __init__(self, parent):
        super(CameraLayerExtension, self).__init__(parent)
        self._camera_layers = list()  # [(node, camera_layer), ...]


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
        self._create_camera_layer_action = create_action(
                name="create_camera_layer",
                text="Create Camera Layer",
                triggered=self.create_camera_layer,
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
                self._create_camera_layer_action)


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
