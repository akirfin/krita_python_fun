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
        QObject

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
        walk_menu

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
        self._camera_layers = list()  # [(node, camera_layer), ...]


    def setup(self):
        pass


    def createActions(self, window):
        # menubar = window.qwindow().menuBar()
        # first_tools = first(a for a, _ in walk_menu(menubar) if a.objectName() == "tools")

        # create_camera_layer_action = first_tools.menu().addAction("Create camera layer")
        # create_camera_layer_action.setObjectName("create_camera_layer")
        # create_camera_layer_action.triggered.connect(self.act_create_camera_layer)
        create_camera_layer_action = window.createAction("create_camera_layer", "Create camera layer")
        create_camera_layer_action.triggered.connect(self.create_camera_layer)


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
