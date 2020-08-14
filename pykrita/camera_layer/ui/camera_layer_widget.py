

from krita import Krita

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtWidgets import \
        QWidget, QComboBox, QPushButton

from camera_layer.common.utils_qt import \
        get_enum_str

from camera_layer.common.utils_kis import \
        find_document_for

from camera_layer.nodes.camera_layer import \
        CameraLayer

from camera_layer.data_types.camera_layer_data import \
        CameraLayerData


class CameraLayerWidget(QWidget):
    def __init__(self, camera_layer, parent=None):
        super(CameraLayerWidget, self).__init__("None", parent=parent)
        self._camera_layer = camera_layer
        self.create_ui()


    def create_ui(self):
        layout = QFormLayout()
        self.setLayout(layout)

        self._camera_id = QComboBox()
        layout.addRow("camera_id", self._camera_id)

        self._mode = QComboBox()
        layout.addRow("mode", self._mode)

        #self._transform = TranformWidget()
        #layout.addRow("transform", self._transform)

        self._capture = QPushButton("Capture")  # toggle/click button with red dot
        layout.addRow(self._capture)

        self._camera_layer.data_changed.connect(self.on_camera_layer_data_changed)


    def get_camera_layer(self):
        return self._camera_layer


    def set_camera_layer(self, new_camera_layer):
        self._camera_layer = new_camera_layer


    def get_data(self):
        return self._camera_layer.data


    QSlot(CameraLayerData)  # non-QObject?
    def set_data(self, new_data):
        self._camera_layer.data = new_data


    data_changed = QSignal(CameraLayerData)
    data = QProperty(CameraLayerData, fget=get_data, fset=set_data, notify=data_changed, user=True)


    def on_camera_layer_data_changed(self, new_data):
        self._camera_id.setText(camera_layer_data.camera_id)
        self._mode.setText(camera_layer_data.mode)
        self._transform.setText(camera_layer_data.transform)
        self.data_changed.emit(new_data)


    def on_capture(self):
        self.camera_layer.capture()
