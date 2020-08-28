from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtWidgets import QLineEdit

from layer_extra_properties.common.utils_py import \
        first, last, UnicodeType, BytesType

from .data_editor_mapper import data_editor_mapper


class StrEditor(QLineEdit):
    def __init__(self, parent=None):
        super(StrEditor, self).__init__(parent=parent)
        self.setStyleSheet(".StrEditor {padding-left: 3px;}")
        self.textChanged.connect(self.data_changed)


    def get_data(self):
        return self.text()


    @QSlot(UnicodeType)
    def set_data(self, new_data):
        new_data = UnicodeType(new_data)
        old_data = self.get_data()
        if new_data != old_data:
            self.setText(new_data)


    data_changed = QSignal(UnicodeType)
    data = QProperty(UnicodeType, fget=get_data, fset=set_data, notify=data_changed, user=True)


data_editor_mapper.register(UnicodeType, StrEditor)
