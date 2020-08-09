

from krita import Krita
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtMultimedia import QCameraInfo, QCamera, QCameraImageCapture

from .common.utils_qt import \
        get_enum_str

from .common.utils_kis import \
        find_document_for


class CameraLayer(QPlainTextEdit):
    """
    serves as debug console.
    """

    def __init__(self, node):
        super(CameraLayer, self).__init__()
        self._node = node
        self._document = find_document_for(self._node)

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
        return super(CameraLayer, self).closeEvent(event)
