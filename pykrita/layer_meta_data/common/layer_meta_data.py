from krita import Krita

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtCore import \
        QTimer

from PyQt5.QtWidgets import \
        QDialog, QApplication, QTextEdit

from .utils_py import \
        print_console, first, last, UnicodeType, BytesType

from .utils_kis import \
        keep_active_node


def get_layer_meta_data(node):
    def _get_layer_meta_data(_result):
        qapp = QApplication.instance()
        for w in qapp.topLevelWidgets():
            if isinstance(w, QDialog):
                if w.metaObject().className() == "KisMetaDataEditor":
                    dialog = w
                    edit_description = dialog.findChild(QTextEdit, "editDescription")
                    _result.append(edit_description.toPlainText())
                    dialog.reject()

    with keep_active_node(new_node=node):
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
                    edit_description = dialog.findChild(QTextEdit, "editDescription")
                    edit_description.setPlainText(_new_meta_data)
                    dialog.accept()

    with keep_active_node(new_node=node):
        QTimer.singleShot(0, lambda nmd=new_meta_data: _set_layer_meta_data(nmd))
        Krita.instance().action("EditLayerMetaData").trigger()
