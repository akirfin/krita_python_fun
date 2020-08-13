"""

How to use:

from camera_layer.layer_properties.layer_properties_widget import \
        LayerMetaDataHook

LayerMetaDataHook.register()

"""
from collections import OrderedDict as oDict
try:
    from collections.abc import Mapping, Iterable
except:
    from collections import Mapping, Iterable

from krita import Krita

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtCore import \
        QObject, QEvent, QSize, QTimer

from PyQt5.QtWidgets import \
        QWidget, QDialog, QStackedLayout, QFormLayout,  QScrollArea, \
        QLabel, QLineEdit, QSpinBox, QDoubleSpinBox, QCheckBox, QApplication

from camera_layer.common.utils_py import \
        print_console, first, last, UnicodeType, BytesType

from camera_layer.common.utils_kis import \
        get_active_node

from camera_layer.common.data_serializer import \
        serializer


class LayerMetaDataWidget(QWidget):
    def __init__(self, node, parent=None):
        super(LayerMetaDataWidget, self).__init__(parent=parent)
        self._node = node
        self.setObjectName("layer_meta_data_widget")
        self.create_ui()


    def create_ui(self):
        layout = QStackedLayout()
        self.setLayout(layout)

        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        layout.addWidget(self._scroll_area)


    def pull_data(self):
        test = StringWidget()
        test.data = "1234"
        print(test.data)

        def get_meta_data(_result):
            qapp = QApplication.instance()
            for w in qapp.topLevelWidgets():
                if isinstance(w, QDialog):
                    if w.metaObject().className() == "KisMetaDataEditor":
                        dialog = w
                        edit_publisher = dialog.findChild(QLineEdit, "editPublisher")
                        _result.append(edit_publisher.text())
                        dialog.reject()

        # target node must be activeNode!
        result = list()
        QTimer.singleShot(0, lambda rs=result: get_meta_data(rs))
        Krita.instance().action("EditLayerMetaData").trigger()

        try:
            data = serializer.loads(first(result))
        except:
            data = oDict()
        content = widget_mapper.create_widget(data)
        old_widget = self._scroll_area.widget()
        self._scroll_area.setWidget(content)
        if old_widget is not None:
            old_widget.deletelater()
            old_widget.setParent(None)


    @QSlot()
    def push_data(self):
        widget = self._scroll_area.widget()
        data = "{}" if widget is None else serializer.dumps(widget.data)

        def set_text(_new_text):
            qapp = QApplication.instance()
            for w in qapp.topLevelWidgets():
                if isinstance(w, QDialog):
                    if w.metaObject().className() == "KisMetaDataEditor":
                        dialog = w
                        edit_publisher = dialog.findChild(QLineEdit, "editPublisher")
                        edit_publisher.selectAll()
                        edit_publisher.insert(_new_text)
                        dialog.accept()

        # target node must be activeNode!
        QTimer.singleShot(0, lambda text=data: set_text(text))
        Krita.instance().action("EditLayerMetaData").trigger()


    def minimumSizeHint(self):
        return QSize(200, 200)


class LayerMetaDataHook(QObject):
    _alive = list()
    _hook = None

    @classmethod
    def register(cls):
        cls.unregister()
        cls._hook = LayerMetaDataHook()
        qapp = QApplication.instance()
        qapp.installEventFilter(cls._hook)


    @classmethod
    def unregister(cls):
        if cls._hook is not None:
            qapp = QApplication.instance()
            qapp.removeEventFilter(cls._hook)
        cls._hook = None


    @classmethod
    def keep_alive(cls, qobj):
        if qobj not in cls._alive:
            cls._alive.append(qobj)

    @classmethod
    def drop_dead(cls, qobj):
        cls._alive[:] = (q for q in cls._alive if q != qobj)


    def eventFilter(self, obj, event):
        if isinstance(obj, QDialog):
            dialog = obj
            if dialog.metaObject().className() == "KisDlgLayerProperties":
                if event.type() == QEvent.WindowIconChange:  # done only once in init.
                # if event.type() == 216:  # done only once in init.
                    layout = dialog.layout()  # QVBoxLayout
                    node = get_active_node()
                    widget = LayerMetaDataWidget(node)
                    self.keep_alive(dialog)
                    widget.pull_data()
                    layout.insertWidget(1, widget, stretch=100)
                    dialog.destroyed.connect(lambda target=dialog: self.drop_dead(target))
                    dialog.accepted.connect(widget.push_data)
        return super(LayerMetaDataHook, self).eventFilter(obj, event)


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
        layout = QFormLayout()
        layout.setContentsMargins(16, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)


    def clear(self):
        layout = self.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deletelater()
                widget.setParent(None)


    def get_data(self):
        result = oDict()
        layout = self.layout()
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
        layout = self.layout()
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
        layout = QFormLayout()
        layout.setContentsMargins(16, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)


    def clear(self):
        layout = self.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deletelater()
                widget.setParent(None)


    def get_data(self):
        result = list()
        layout = self.layout()
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
        layout = self.layout()
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
