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

from PyQt5.QtGui import \
        QPalette, QColor

from PyQt5.QtWidgets import \
        QWidget, QFrame, QLabel, QLineEdit, QSpinBox, QDoubleSpinBox, QCheckBox, \
        QMenuBar, QFormLayout, QHBoxLayout, QVBoxLayout, QToolButton

from layer_meta_data.common.utils_py import \
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
    spanning = True  # special attribute!

    def __init__(self, parent=None):
        super(DictWidget, self).__init__(parent=parent)
        self.create_ui()


    def create_ui(self):
        # section (collapsing title bar)
        # Title bar + menubar
        #   - add, remove, rename, retype attributes
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        self.title_bar = QFrame()
        self.title_bar.setAutoFillBackground(True)
        self.title_bar.setBackgroundRole(QPalette.Window)
        layout.addWidget(self.title_bar)

        title_bar_layout = QHBoxLayout()
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.title_bar.setLayout(title_bar_layout)

        self._folding = QToolButton()
        self._folding.setArrowType(Qt.RightArrow)
        title_bar_layout.addWidget(self._folding)

        self._title_widget = QLabel("")
        self._title_widget.setContentsMargins(8, 0, 8, 0)
        title_bar_layout.addWidget(self._title_widget)

        title_bar_layout.addStretch(stretch=100)

        self.menu_bar = QMenuBar()
        self.menu_bar.addMenu("Edit")
        title_bar_layout.addWidget(self.menu_bar)

        self.items = QWidget()
        # self.items.setAutoFillBackground(True)
        # self.items.setBackgroundRole(QPalette.Window)
        layout.addWidget(self.items)

        self.items_layout = QFormLayout()
        self.items_layout.setHorizontalSpacing(5)
        self.items_layout.setVerticalSpacing(2)
        self.items_layout.setContentsMargins(48, 4, 0, 8)
        # self.items.setAlignment(Qt.AlignTop)
        # self.items.setLabelAlignment(Qt.AlignRight)
        self.items.setLayout(self.items_layout)


    def adjust_label_widths(self, width):
        layout = self.items_layout
        for i in range(layout.rowCount()):
            item = layout.itemAt(i, QFormLayout.LabelRole)
            if item is not None:
                # item.setAlignment(Qt.AlignRight)
                label_widget = item.widget()
                if label_widget is not None:
                    # label_widget.setMaximumWidth(width)
                    label_widget.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    label_widget.setFixedWidth(width)  # elide right missing...


    def clear(self):
        layout = self.items_layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deletelater()
                widget.setParent(None)


    def get_data(self):
        result = oDict()
        layout = self.items_layout
        for i in range(layout.rowCount()):
            item = layout.itemAt(i, QFormLayout.LabelRole)
            label_widget = None if item is None else item.widget()
            item = layout.itemAt(i, QFormLayout.FieldRole)
            value_widget = None if item is None else item.widget()
            item = layout.itemAt(i, QFormLayout.SpanningRole)
            spanning_widget = None if item is None else item.widget()
            if spanning_widget is not None:
                label = spanning_widget.objectName()
                result[label] = spanning_widget.data
            elif (label_widget is not None) and (value_widget is not None):
                label = value_widget.objectName()
                result[label] = value_widget.data
        return result


    QSlot(object)
    def set_data(self, new_data):
        it = new_data.items() if isinstance(new_data, Mapping) else new_data
        self.clear()
        layout = self.items_layout
        for name, value in it:
            widget = widget_mapper.create_widget(value)
            widget.setObjectName(name)
            if getattr(widget, "spanning", False):
                widget.title = widget.objectName()
                layout.addRow(widget)
            else:
                layout.addRow(widget.objectName(), widget)
        self.adjust_label_widths(110)  # nice label widths!
        self.data_changed.emit(self.get_data())


    data_changed = QSignal(object)
    data = QProperty(object, fget=get_data, fset=set_data, notify=data_changed, user=True)


    def get_title(self):
        return self._title_widget.text()


    QSlot(UnicodeType)
    def set_title(self, new_title):
        new_title = UnicodeType(new_title)
        old_title = self.get_title()
        if new_title != old_title:
            self._title_widget.setText(new_title)
            self.title_changed.emit(self.get_title())


    title_changed = QSignal(UnicodeType)
    title = QProperty(UnicodeType, fget=get_title, fset=set_title, notify=title_changed, user=True)


class ListWidget(QWidget):
    spanning = True  # special attribute!

    def __init__(self, parent=None):
        super(ListWidget, self).__init__(parent=parent)
        self.create_ui()


    def create_ui(self):
        # section (collapsing title bar)
        # Title bar + menubar
        #   - add, remove, rename, retype attributes
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        self.title_bar = QFrame()
        self.title_bar.setAutoFillBackground(True)
        self.title_bar.setBackgroundRole(QPalette.Window)
        layout.addWidget(self.title_bar)

        title_bar_layout = QHBoxLayout()
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.title_bar.setLayout(title_bar_layout)

        self._folding = QToolButton()
        self._folding.setArrowType(Qt.RightArrow)
        title_bar_layout.addWidget(self._folding)

        self._title_widget = QLabel("")
        self._title_widget.setContentsMargins(8, 0, 8, 0)
        title_bar_layout.addWidget(self._title_widget)

        title_bar_layout.addStretch(stretch=100)

        self.menu_bar = QMenuBar()
        self.menu_bar.addMenu("Edit")
        title_bar_layout.addWidget(self.menu_bar)

        self.items = QFormLayout()
        self.items.setHorizontalSpacing(5)
        self.items.setVerticalSpacing(2)
        self.items.setContentsMargins(48, 4, 0, 8)
        # self.items.setAlignment(Qt.AlignTop)
        # self.items.setLabelAlignment(Qt.AlignRight)
        layout.addLayout(self.items)


    def adjust_label_widths(self, width):
        layout = self.items
        for i in range(layout.rowCount()):
            item = layout.itemAt(i, QFormLayout.LabelRole)
            if item is not None:
                # item.setAlignment(Qt.AlignRight)
                label_widget = item.widget()
                if label_widget is not None:
                    # label_widget.setMaximumWidth(width)
                    label_widget.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    label_widget.setFixedWidth(width)  # elide right missing...


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
            if spanning_widget is not None:
                label = spanning_widget.objectName() # not used
                result.append(spanning_widget.data)
            elif (label_widget is not None) and (value_widget is not None):
                label = value_widget.objectName() # not used
                result.append(value_widget.data)
        return result


    QSlot(object)
    def set_data(self, new_data):
        self.clear()
        layout = self.items
        for index, value in enumerate(new_data):
            widget = widget_mapper.create_widget(value)
            widget.setObjectName(str(index))
            label = "[ {} ]".format(widget.objectName())
            if getattr(widget, "spanning", False):
                widget.title = label
                layout.addRow(widget)
            else:
                layout.addRow(label, widget)
        self.adjust_label_widths(80)  # nice index label widths!
        self.data_changed.emit(self.get_data())


    data_changed = QSignal(object)
    data = QProperty(object, fget=get_data, fset=set_data, notify=data_changed, user=True)


    def get_title(self):
        return self._title_widget.text()


    QSlot(UnicodeType)
    def set_title(self, new_title):
        new_title = UnicodeType(new_title)
        old_title = self.get_title()
        if new_title != old_title:
            self._title_widget.setText(new_title)
            self.title_changed.emit(self.get_title())


    title_changed = QSignal(UnicodeType)
    title = QProperty(UnicodeType, fget=get_title, fset=set_title, notify=title_changed, user=True)


class NoneWidget(QLabel):
    def __init__(self, parent=None):
        super(NoneWidget, self).__init__("None", parent=parent)


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
