"""

ToDo:
    - cleaning!
    - re-write to CameraLayerNG
    - solve QTransform & how to serialize

"""

from collections import OrderedDict as oDict

from krita import Krita, Node

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
        walk_menu, get_enum_str

from camera_layer.data_types.camera_layer_data import \
        CameraLayerData

from layer_meta_data.common.data_serializer import \
        serializer

from layer_meta_data.layer_meta_data import \
        get_layer_meta_data, set_layer_meta_data


class CameraLayer(QObject):
    """
    Function set for camera layer.
    serves as debug console.
    """
    meta_data_id = "camera_layer"

    def __init__(self):
        super(CameraLayer, self).__init__()
        self._camera_layer_data = CameraLayerData()
        self._node = None

        try:
            cam_info = QCameraInfo.availableCameras()[0]
        except:
            raise RuntimeError("Can't find first available Camera!")
        cam_info_desc = cam_info.description()
        # self.appendPlainText("First camera device connected to computer: {cam_info_desc}".format(**locals()))

        self._camera = QCamera(cam_info)
        self._camera.setCaptureMode(QCamera.CaptureStillImage)
        self._cap = QCameraImageCapture(self._camera)
        self._cap.setCaptureDestination(QCameraImageCapture.CaptureToBuffer)  # CaptureToFile

        self._cap.readyForCaptureChanged.connect(self.on_ready_changed)
        self._cap.error.connect(self.on_error)
        self._cap.imageCaptured.connect(self.on_image_captured)
        self._camera.statusChanged.connect(self.on_status_changed)
        self._camera.error.connect(self.on_camera_error)

        # self.appendPlainText("Warming up, the camera!")
        self._camera.start()
        self.startTimer(int(1000 / 15))  # 15 fps


    def on_ready_changed(self, is_ready):
        # self.appendPlainText("on_ready_changed({is_ready!r})".format(**locals()))
        pass


    def on_status_changed(self, status):
        status_name = get_enum_str(QCamera, QCamera.Status, status)
        # self.appendPlainText("on_status_changed({status_name!r})".format(**locals()))


    def on_image_captured(self, id, preview):
        # self.appendPlainText("on_image_captured(...)")
        if not preview.isNull():
            preview.convertToFormat(QImage.Format_RGBA8888)
            ptr = preview.constBits()
            ptr.setsize(preview.byteCount())
            self._node.setPixelData(bytes(ptr.asarray()), 0, 0, preview.width(), preview.height())
            document = find_document_for(self._node)
            if document is None:
                self._camera.stop()
            else:
                document.refreshProjection()


    def on_camera_error(self, error):
        # error_name = get_enum_str(QCamera, QCamera.Error, error)
        # self.appendPlainText("on_camera_error({error_name!r})".format(**locals()))
        self._camera.stop()


    def on_error(self, id, error, errorString):
        # self.appendPlainText("on_error({errorString!r})".format(**locals()))
        self._camera.stop()


    def timerEvent(self, event):
        if self._cap.isReadyForCapture():
            # self.appendPlainText("\n*** Say cheese! ***\n".format(**locals()))
            self._cap.capture()  # "C:/tmp/cam_test.jpg"


    def closeEvent(self, event):
        self._camera.stop()
        return super(CameraLayerFS, self).closeEvent(event)


    def get_node(self):
        return self._node


    @QSlot(object)
    def set_node(self, new_node):
        if not isinstance(new_node, (Node, type(None))):
            raise RuntimeError("Bad node, must be Node or None. (did get: {new_node})".format(**locals()))
        old_node = self.get_node()
        if new_node != old_node:
            self._node = new_node
            self.pull_data()
            self.node_changed.emit(self.get_node())


    node_changed = QSignal(object)
    node = QProperty(object, fget=get_node, fset=set_node, notify=node_changed)


    def get_data(self):
        return CameraLayerData.cast(self._camera_layer_data)


    QSlot(CameraLayerData)
    def set_data(self, new_data):
        new_data = CameraLayerData.cast(new_data)
        old_data = self.get_data()
        if new_data != old_data:
            self._camera_layer_data = new_data
            self.data_changed.emit(self.get_data())

    data_changed = QSignal(CameraLayerData)
    data = QProperty(CameraLayerData, fget=get_data, fset=set_data, notify=data_changed)


    def pull_data(self):
        meta_data = get_layer_meta_data(self._node)
        try:
            data = serializer.loads(meta_data)
        except:
            data = oDict()
        self._camera_layer = data.get(self.meta_data_id, CameraLayerData())


    def push_data(self):
        meta_data = get_layer_meta_data(self._node)
        try:
            data = serializer.loads(meta_data)
        except:
            data = oDict()
        data[self.meta_data_id] = self._camera_layer
        meta_data = serializer.dumps(data)
        set_layer_meta_data(self._node, meta_data)


class CameraLayerNG(QObject):
    def __init__(self, node):
        self._data = CameraLayerData()
        self._node = None
        if node is not None:
            self.node = node


    def get_node(self):
        return self._node


    def set_node(self, new_node):
        old_node = self.get_node()
        if new_node != old_node:
            if old_node is not None:
                self.push_data(old_node, self._data)
            self._node = new_node
            if new_node is not None:
                data = self.pull_data(new_node)
                self._data = CameraLayerData() if data is None else data


    @classmethod
    def pull_data(cls, node):
        data = get_layer_meta_data(node)
        data = serializer.loads(data)
        return data.get("camera_layer")


    @classmethod
    def push_data(cls, node, data):
        json_data = get_layer_meta_data(node)
        meta_data = serializer.loads(json_data)
        meta_data["camera_layer"] = data
        json_data = serializer.dumps(meta_data)
        set_layer_meta_data(node, json_data)
