from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtWidgets import QCheckBox

from .data_editor_mapper import data_editor_mapper


class BoolEditor(QCheckBox):
    def __init__(self, parent=None):
        super(BoolEditor, self).__init__(parent=parent)
        self.toggled.connect(self.data_changed)


    def get_data(self):
        return self.isChecked()


    QSlot(bool)
    def set_data(self, new_data):
        new_data = bool(new_data)
        old_data = self.get_data()
        if new_data != old_data:
            self.setChecked(new_data)


    data_changed = QSignal(bool)
    data = QProperty(bool, fget=get_data, fset=set_data, notify=data_changed, user=True)


data_editor_mapper.register(bool, BoolEditor)
