

from krita import Krita

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

from camera_layer.common.utils_qt import \
        get_enum_str

from camera_layer.common.utils_kis import \
        find_document_for

from camera_layer.data_types.camera_layer_data import \
        CameraLayerData


class CameraLayer(QObject):
    """
    Function set for camera layer.
    serves as debug console.
    """
    meta_data_id = "akir:camera_layer"

    def __init__(self, node):
        super(CameraLayer, self).__init__()
        self._camera_layer_data = CameraLayerData()
        self._node = node

        cam_info = QCameraInfo.availableCameras()[0]
        cam_info_desc = cam_info.description()
        self.appendPlainText("First camera device connected to computer: {cam_info_desc}".format(**locals()))

        self._camera = QCamera(cam_info)
        self._camera.setCaptureMode(QCamera.CaptureStillImage)
        self._cap = QCameraImageCapture(self._camera)
        self._cap.setCaptureDestination(QCameraImageCapture.CaptureToBuffer)  # CaptureToFile

        self._cap.readyForCaptureChanged.connect(self.on_ready_changed)
        self._cap.error.connect(self.on_error)
        self._cap.imageCaptured.connect(self.on_image_captured)
        self._camera.statusChanged.connect(self.on_status_changed)
        self._camera.error.connect(self.on_camera_error)

        self.appendPlainText("Warming up, the camera!")
        self._camera.start()
        self.startTimer(int(1000 / 15))  # 15 fps


    def on_ready_changed(self, is_ready):
        self.appendPlainText("on_ready_changed({is_ready!r})".format(**locals()))


    def on_status_changed(self, status):
        status_name = get_enum_str(QCamera, QCamera.Status, status)
        self.appendPlainText("on_status_changed({status_name!r})".format(**locals()))


    def on_image_captured(self, id, preview):
        self.appendPlainText("on_image_captured(...)")
        if not preview.isNull():
            preview.convertToFormat(QImage.Format_RGBA8888)
            ptr = preview.constBits()
            ptr.setsize(preview.byteCount())
            self._node.setPixelData(bytes(ptr.asarray()), 0, 0, preview.width(), preview.height())
            self._document.refreshProjection()


    def on_camera_error(self, error):
        error_name = get_enum_str(QCamera, QCamera.Error, error)
        self.appendPlainText("on_camera_error({error_name!r})".format(**locals()))
        self._camera.stop()


    def on_error(self, id, error, errorString):
        self.appendPlainText("on_error({errorString!r})".format(**locals()))
        self._camera.stop()


    def timerEvent(self, event):
        if self._cap.isReadyForCapture():
            self.appendPlainText("\n*** Say cheese! ***\n".format(**locals()))
            self._cap.capture()  # "C:/tmp/cam_test.jpg"


    def closeEvent(self, event):
        self._camera.stop()
        return super(CameraLayerFS, self).closeEvent(event)


    def get_data(self):
        return CameraLayerData.cast(self._camera_layer_data)


    QSlot(CameraLayerData)  # non-QObject?
    def set_data(self, new_data):
        new_data = CameraLayerData.cast(new_data)
        old_data = self.get_data()
        if new_data != old_data:
            self._camera_layer_data = new_data
            self.data_changed.emit(self.get_data())


    def pull_data(self):
        meta_data = get_layer_meta_data(self._node)
        try:
            data = serializer.loads(meta_data)
        except:
            data = oDict()
        self._camera_layer = data[self.meta_data_id]


    def push_data(self):
        meta_data = get_layer_meta_data(self._node)
        try:
            data = serializer.loads(meta_data)
        except:
            data = oDict()
        data[self.meta_data_id] = self._camera_layer
        meta_data = serializer.dumps(data)
        set_layer_meta_data(self._node, meta_data)


    data_changed = QSignal(CameraLayerData)
    data = QProperty(CameraLayerData, fget=get_data, fset=set_data, notify=data_changed, user=True)
