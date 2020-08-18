

from krita import Krita, Node

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtWidgets import \
        QWidget, QComboBox, QPushButton, QFormLayout

from camera_layer.common.utils_qt import \
        get_enum_str

from camera_layer.common.utils_kis import \
        find_document_for

from camera_layer.camera_layer import \
        CameraLayer

from camera_layer.data_types.camera_layer_data import \
        CameraLayerData


class CameraLayerWidget(QWidget):
    def __init__(self, parent=None):
        super(CameraLayerWidget, self).__init__(parent=parent)
        self._camera_layer = None
        self.create_ui()


    def create_ui(self):
        layout = QFormLayout()
        self.setLayout(layout)

        self._camera_id = QComboBox()
        layout.addRow(i18n("camera_id"), self._camera_id)

        self._mode = QComboBox()
        layout.addRow(i18n("mode"), self._mode)

        #self._transform = TranformWidget()
        #layout.addRow("transform", self._transform)

        self._capture = QPushButton(i18n("Capture"))  # toggle/click button with red dot
        layout.addRow(self._capture)


    def on_capture(self):
        self.camera_layer.capture()


    def update(self):
        self._camera_id.setText()
        self._mode.setText()
        self._transform.setText()
        return super(CameraLayerWidget, self).update()


    def get_node(self):
        return self._node


    @QSlot(object)
    def set_node(self, new_node):
        if not isinstance(new_node, (Node, type(None))):
            raise RuntimeError("Bad node, must be Node or None. (did get: {new_node})".format(**locals()))
        old_node = self.get_node()
        if new_node != old_node:
            self._node = new_node
            self.camera_layer = extension.instance().get_camera_layer(self._node)
            self.node_changed.emit(self.get_node())


    node_changed = QSignal(object)
    node = QProperty(object, fget=get_node, fset=set_node, notify=node_changed)


    def get_camera_layer(self):
        return self._camera_layer
    QSlot(object)
    def set_camera_layer(self, new_camera_layer):
        old_camera_layer = self._camera_layer
        if new_camera_layer != old_camera_layer:
            if old_camera_layer is not None:
                old_camera_layer.data_changed.disconnect(self.on_camera_layer_data_changed)
            self._camera_layer = new_camera_layer
            if new_camera_layer is not None:
                new_camera_layer.data_changed.connect(self.on_camera_layer_data_changed)
            self.update()
            self.camera_layer_changed.emit(self.get_camera_layer())
    camera_layer_changed = QSignal(object)
    camera_layer = QProperty(object, fget=get_camera_layer, fset=set_camera_layer, notify=camera_layer_changed)


    def on_camera_layer_data_changed(self, new_data):
        self.update()
        self.data_changed.emit(new_data)


    def get_data(self):
        return self._camera_layer.data
    QSlot(CameraLayerData)
    def set_data(self, new_data):
        self._camera_layer.data = new_data
    data_changed = QSignal(CameraLayerData)
    data = QProperty(CameraLayerData, fget=get_data, fset=set_data, notify=data_changed, user=True)
