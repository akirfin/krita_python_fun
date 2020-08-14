

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

from camera_layer.data_types.camera_layer_data import \
        CameraLayerData


class CameraLayerWidget(QWidget):
    def __init__(self, parent=None):
        super(NoneWidget, self).__init__("None", parent=parent)
        self._camera = CameraLayerFS()
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


    def get_data(self):
        return CameraLayerData(
                camera_id=self._camera_id.selectedText(),
                mode=self._mode.selectedText(),
                transform=self._transform.data)


    QSlot(CameraLayerData)  # non-QObject?
    def set_data(self, new_data):
        new_data = CameraLayerData.cast(new_data)
        old_data = self.get_data()
        if new_data != old_data:
            self._camera_id.setSelectedText(new_data.camera_id)
            self._mode.setSelectedText(new_data.mode)
            self._transform.data = new_data.transform
            self.data_changed.emit(self.get_data())


    data_changed = QSignal(CameraLayerData)
    data = QProperty(CameraLayerData, fget=get_data, fset=set_data, notify=data_changed, user=True)


    def on_capture(self):
        node = None
        for anc in walk_qobject_ancestors(self):
            if isinstance(anc, LayerMetaDataWidget):
                node = anc.node
                break
        if node is not None:
            camera = self._camera
            camera.node = node
            camera.capture()
