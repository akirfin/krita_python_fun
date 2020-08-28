from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtWidgets import QLabel

from .data_editor_mapper import data_editor_mapper


class NoneEditor(QLabel):
    def __init__(self, parent=None):
        super(NoneEditor, self).__init__("None", parent=parent)


    def get_data(self):
        return None


    QSlot(type(None))
    def set_data(self, new_data):
        """
        Nothing will change, trust me!
        """
        if new_data is not None:
            raise RuntimeError("Not None. (did get: {new_data})".format(**locals()))


    data_changed = QSignal(type(None))  # will newer fire!
    data = QProperty(type(None), fget=get_data, fset=set_data, notify=data_changed, user=True)


data_editor_mapper.register(type(None), NoneEditor)
