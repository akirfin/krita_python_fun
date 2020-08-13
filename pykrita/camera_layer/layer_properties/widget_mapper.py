"""

Maps data_types to widgets
by default JSON object are supported, register more data types if needed.

"""

from collections import OrderedDict as oDict
try:
    from collections.abc import Mapping, Iterable
except:
    from collections import Mapping, Iterable

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtWidgets import \
        QWidget, QFormLayout, QLabel, QLineEdit, \
        QSpinBox, QDoubleSpinBox, QCheckBox, QVBoxLayout, QMenuBar

from camera_layer.common.utils_py import \
        first, last, UnicodeType, BytesType


class WidgetMapper(object):
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._registry = oDict()

    def register(self, data_type, widget_type):
        self._registry[data_type] = widget_type

    def create_widget(self, obj):
        data_type = type(obj)
        if data_type in self._registry:
            widget_type = self._registry[data_type]
            widget = widget_type()
            widget.data = obj
            return widget
        elif issubclass(data_type, Mapping):
            widget = DictWidget()
            widget.data = obj
            return widget
        elif issubclass(data_type, Iterable):
            widget = ListWidget()
            widget.data = obj
            return widget
        raise RuntimeError("Unable to create widget for {obj!r}".format(**locals()))

widget_mapper = WidgetMapper.instance()


class DictWidget(QWidget):
    def __init__(self, parent=None):
        super(DictWidget, self).__init__(parent=parent)
        self.setObjectName("dict_widget")
        self.create_ui()


    def create_ui(self):
        # section (collapsing title bar)
        # Title bar + menubar
        #   - add, remove, rename, retype attributes
        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        self.menu_bar = QMenuBar()
        self.menu_bar.addMenu("Edit")
        layout.addWidget(self.menu_bar)  # , alignment=Qt.AlignRight)

        self.items = QFormLayout()
        self.items.setContentsMargins(32, 0, 0, 8)
        self.items.setAlignment(Qt.AlignTop)
        layout.addLayout(self.items)


    def clear(self):
        layout = self.items
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deletelater()
                widget.setParent(None)


    def get_data(self):
        result = oDict()
        layout = self.items
        for i in range(layout.rowCount()):
            item = layout.itemAt(i, QFormLayout.LabelRole)
            label_widget = None if item is None else item.widget()
            item = layout.itemAt(i, QFormLayout.FieldRole)
            value_widget = None if item is None else item.widget()
            item = layout.itemAt(i, QFormLayout.SpanningRole)
            spanning_widget = None if item is None else item.widget()
            if (label_widget is not None) and (value_widget is not None):
                label = label_widget.text()
                result[label] = value_widget.data
        return result
    QSlot(object)
    def set_data(self, new_data):
        it = new_data.items() if isinstance(new_data, Mapping) else new_data
        self.clear()
        layout = self.items
        for label, value in it:
            widget = widget_mapper.create_widget(value)
            layout.addRow(label, widget)
        self.data_changed.emit(self.get_data())

    data_changed = QSignal(object)
    data = QProperty(object, fget=get_data, fset=set_data, notify=data_changed, user=True)


class ListWidget(QWidget):
    def __init__(self, parent=None):
        super(ListWidget, self).__init__(parent=parent)
        self.setObjectName("list_widget")
        self.create_ui()


    def create_ui(self):
        # section (collapsing title bar)
        # Title bar + menubar
        #   - add, remove, rename, retype attributes
        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        self.menu_bar = QMenuBar()
        self.menu_bar.addMenu("Edit")
        layout.addWidget(self.menu_bar)  # , alignment=Qt.AlignRight)

        self.items = QFormLayout()
        self.items.setContentsMargins(32, 0, 0, 8)
        self.items.setAlignment(Qt.AlignTop)
        layout.addLayout(self.items)


    def clear(self):
        layout = self.items
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deletelater()
                widget.setParent(None)


    def get_data(self):
        result = list()
        layout = self.items
        for i in range(layout.rowCount()):
            item = layout.itemAt(i, QFormLayout.LabelRole)
            label_widget = None if item is None else item.widget()
            item = layout.itemAt(i, QFormLayout.FieldRole)
            value_widget = None if item is None else item.widget()
            item = layout.itemAt(i, QFormLayout.SpanningRole)
            spanning_widget = None if item is None else item.widget()
            if (label_widget is not None) and (value_widget is not None):
                result.append(value_widget.data)
        return result
    QSlot(object)
    def set_data(self, new_data):
        self.clear()
        layout = self.items
        for index, value in enumerate(new_data):
            widget = widget_mapper.create_widget(value)
            layout.addRow("[{}]".format(index), widget)
        self.data_changed.emit(self.get_data())

    data_changed = QSignal(object)
    data = QProperty(object, fget=get_data, fset=set_data, notify=data_changed, user=True)


class NoneWidget(QLabel):
    def __init__(self, parent=None):
        super(NoneWidget, self).__init__("None", parent=parent)
        self.setObjectName("none_widget")

    def get_data(self):
        return None
    QSlot(type(None))
    def set_data(self, new_data):
        if not isinstance(new_data, type(None)):
            raise RuntimeError("Not None instance!")
        # self.data_changed.emit(self.get_data())  # will newer happen!
    data_changed = QSignal(type(None))
    data = QProperty(type(None), fget=get_data, fset=set_data, notify=data_changed, user=True)

widget_mapper.register(type(None), NoneWidget)


class BoolWidget(QCheckBox):
    def __init__(self, parent=None):
        super(BoolWidget, self).__init__(parent=parent)
        self.setObjectName("bool_widget")

    def get_data(self):
        return self.isChecked()
    QSlot(bool)
    def set_data(self, new_data):
        new_data = bool(new_data)
        old_data = self.get_data()
        if new_data != old_data:
            self.setChecked(new_data)
            self.data_changed.emit(self.get_data())
    data_changed = QSignal(bool)
    data = QProperty(bool, fget=get_data, fset=set_data, notify=data_changed, user=True)

widget_mapper.register(bool, BoolWidget)


class IntWidget(QSpinBox):
    def __init__(self, parent=None):
        super(IntWidget, self).__init__(parent=parent)
        self.setObjectName("int_widget")
        self.setRange(-2147483648, 2147483647)  # c int min / max

    def get_data(self):
        return self.value()
    QSlot(int)
    def set_data(self, new_data):
        new_data = int(new_data)
        old_data = self.get_data()
        if new_data != old_data:
            self.setValue(new_data)
            self.data_changed.emit(self.get_data())
    data_changed = QSignal(int)
    data = QProperty(int, fget=get_data, fset=set_data, notify=data_changed, user=True)

widget_mapper.register(int, IntWidget)


class FloatWidget(QDoubleSpinBox):
    def __init__(self, parent=None):
        super(FloatWidget, self).__init__(parent=parent)
        self.setObjectName("float_widget")
        self.setRange(float("-inf"), float("inf"))
        self.setDecimals(323)

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
            self.data_changed.emit(self.get_data())
    data_changed = QSignal(float)
    data = QProperty(float, fget=get_data, fset=set_data, notify=data_changed, user=True)


widget_mapper.register(float, FloatWidget)


class StringWidget(QLineEdit):
    def __init__(self, parent=None):
        super(StringWidget, self).__init__(parent=parent)
        self.setObjectName("string_widget")
        self.setStyleSheet(".StringWidget {padding-left: 3px;}")


    def get_data(self):
        return self.text()
    @QSlot(UnicodeType)
    def set_data(self, new_data):
        new_data = UnicodeType(new_data)
        old_data = self.get_data()
        if new_data != old_data:
            self.setText(new_data)
            self.data_changed.emit(self.get_data())
    data_changed = QSignal(UnicodeType)
    data = QProperty(UnicodeType, fget=get_data, fset=set_data, notify=data_changed, user=True)


widget_mapper.register(UnicodeType, StringWidget)
