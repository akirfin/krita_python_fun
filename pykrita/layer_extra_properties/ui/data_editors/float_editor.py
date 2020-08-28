from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtWidgets import QDoubleSpinBox

from .data_editor_mapper import data_editor_mapper


class FloatEditor(QDoubleSpinBox):
    def __init__(self, parent=None):
        super(FloatEditor, self).__init__(parent=parent)
        self.setRange(float("-inf"), float("inf"))
        self.setDecimals(323)
        self.valueChanged.connect(self.data_changed)


    def textFromValue(self, val):
        return "{:.2f}".format(float(val))


    def get_data(self):
        return self.value()


    QSlot(float)
    def set_data(self, new_data):
        new_data = float(new_data)
        old_data = self.get_data()
        if new_data != old_data:
            self.setValue(new_data)


    data_changed = QSignal(float)
    data = QProperty(float, fget=get_data, fset=set_data, notify=data_changed, user=True)


data_editor_mapper.register(float, FloatEditor)
