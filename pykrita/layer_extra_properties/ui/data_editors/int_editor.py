from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtWidgets import QSpinBox

from .data_editor_mapper import data_editor_mapper


class IntEditor(QSpinBox):
    def __init__(self, parent=None):
        super(IntEditor, self).__init__(parent=parent)
        self.setRange(-2147483648, 2147483647)  # c int min / max
        self.valueChanged.connect(self.data_changed)


    def get_data(self):
        return self.value()


    QSlot(int)
    def set_data(self, new_data):
        new_data = int(new_data)
        old_data = self.get_data()
        if new_data != old_data:
            self.setValue(new_data)


    data_changed = QSignal(int)
    data = QProperty(int, fget=get_data, fset=set_data, notify=data_changed, user=True)


data_editor_mapper.register(int, IntEditor)
