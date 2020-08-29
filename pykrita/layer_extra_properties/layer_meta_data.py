"""

from krita import Krita

from layer_extra_properties.layer_meta_data import \
        get_layer_meta_data, set_layer_meta_data

node = Krita.instance().activeDocument().activeNode()
set_layer_meta_data(node, "my nice meta dada duu!")

data = get_layer_meta_data(node)

ToDo: move to doublin core title ?

"""

from contextlib import contextmanager

from krita import Krita

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtCore import \
        QObject, QTimer, QEvent, QRect

from PyQt5.QtWidgets import \
        QDialog, QApplication, QTextEdit, QLineEdit

from .common.utils_py import \
        first, last, UnicodeType, BytesType

from .common.utils_kis import \
        keep_active_node


def get_layer_meta_data(node):
    def _get_layer_meta_data(_result):
        qapp = QApplication.instance()
        for w in qapp.topLevelWidgets():
            if isinstance(w, QDialog):
                if w.metaObject().className() == "KisMetaDataEditor":
                    dialog = w
                    edit_description = dialog.findChild(QLineEdit, "editPublisher")  # editDescription bug not saved!
                    _result.append(edit_description.text())
                    dialog.reject()

    with keep_active_node(new_node=node), hook_context(SizeZeroHook()):
        result = list()
        QTimer.singleShot(0, lambda rs=result: _get_layer_meta_data(rs))
        Krita.instance().action("EditLayerMetaData").trigger()
        return first(result)


def set_layer_meta_data(node, new_meta_data):
    def _set_layer_meta_data(_new_meta_data):
        qapp = QApplication.instance()
        for w in qapp.topLevelWidgets():
            if isinstance(w, QDialog):
                if w.metaObject().className() == "KisMetaDataEditor":
                    dialog = w
                    edit_description = dialog.findChild(QLineEdit, "editPublisher")  # editDescription bug not saved!
                    edit_description.selectAll()
                    edit_description.insert(_new_meta_data)
                    dialog.accept()

    with keep_active_node(new_node=node), hook_context(SizeZeroHook()):
        QTimer.singleShot(0, lambda nmd=new_meta_data: _set_layer_meta_data(nmd))
        Krita.instance().action("EditLayerMetaData").trigger()


class SizeZeroHook(QObject):
    def eventFilter(self, obj, event):
        meta_name = obj.metaObject().className()
        if isinstance(obj, QDialog) and (meta_name == "KisMetaDataEditor") and (event.type() == QEvent.Resize):
            obj.setFixedSize(0, 0)
            return True
        return super(SizeZeroHook, self).eventFilter(obj, event)


@contextmanager
def hook_context(hook):
    qapp = QApplication.instance()
    qapp.installEventFilter(hook)
    try:
        yield
    finally:
        qapp.removeEventFilter(hook)
