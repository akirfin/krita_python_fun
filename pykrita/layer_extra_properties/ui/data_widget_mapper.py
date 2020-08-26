"""

Maps data_types to widgets
by default JSON object are supported, register more data types if needed.

"""

from abc import ABCMeta
from collections import OrderedDict as oDict
try:
    from collections.abc import Mapping, MutableMapping, Sequence, MutableSequence, Iterable
except:
    from collections import Mapping, MutableMapping, Sequence, MutableSequence, Iterable

from krita import Krita, Node

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtCore import \
        QObject, QSize

from PyQt5.QtGui import \
        QPalette, QColor, QFont

from PyQt5.QtWidgets import \
        QWidget, QFrame, QLabel, QLineEdit, QSpinBox, QDoubleSpinBox, QCheckBox, \
        QLayout, QMenuBar, QFormLayout, QHBoxLayout, QVBoxLayout, QToolButton, QScrollArea, \
        QGraphicsDropShadowEffect, QPlainTextEdit

from layer_extra_properties.common.utils_py import \
        first, last, UnicodeType, BytesType

from layer_extra_properties.ui.section import \
        Section


class DataWidgetMapper(object):
    """
    Mapping of data_object to data_widget
    """
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance


    def __init__(self):
        self._registry = oDict()


    def register(self, data_type, data_widget_type):
        self._registry[data_type] = data_widget_type


    def create_widget(self, data, name=None):
        data_type = type(data)
        data_widget_type = None

        if data_type in self._registry:
            data_widget_type = self._registry[data_type]
        elif issubclass(data_type, Mapping):
            # generic Mapping type
            data_widget_type = DictWidget
        elif issubclass(data_type, Iterable):
            # generic Iterable type
            data_widget_type = ListWidget

        if data_widget_type is not None:
            data_widget = data_widget_type()
            data_widget.data = data
            if name is not None:
                if isinstance(data_widget, Section):
                    data_widget.title = name
                data_widget.setObjectName(name)
            return data_widget

        raise RuntimeError("Unable to create widget for {data!r}".format(**locals()))

data_widget_mapper = DataWidgetMapper.instance()


class MetaMeta(type(QObject), ABCMeta):
    """
    Too meta for me, so thats why the name!
    (Nothing to see, move along...)

    Union of Shiboken.ObjectType & ABCmeta metaclasses.
    Allows use of collections.abc interfaces with QObjects.
    """


class DataWidgetContainer(QScrollArea, MutableSequence, metaclass=MetaMeta):
    """
    Scroll area containing data widgets.

    ToDo:
        - edit menu

    note:
        - pythonic Sequence interface
        - has data property for getting / setting data_object
    """
    def __init__(self, parent=None):
        QScrollArea.__init__(self, parent=parent)
        self.setObjectName("data_widget_container")
        self.create_ui()


    def create_ui(self):
        # self.setFrameShape(QFrame.NoFrame)
        self.setBackgroundRole(QPalette.Window)
        self.setWidgetResizable(True)
        self._content = QWidget()
        self._content.setAutoFillBackground(True)
        self._content.setBackgroundRole(QPalette.Base)
        self.setWidget(self._content)
        self._content_layout = QVBoxLayout()
        self._content_layout.setSpacing(3)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self._content_layout.setAlignment(Qt.AlignTop)
        self._content.setLayout(self._content_layout)
        self._content.setContentsMargins(10, 10, 4, 10)

    def __len__(self):
        layout = self._content_layout
        return layout.count()


    def __getitem__(self, index):
        if isinstance(index, slice):
            raise NotImplementedError("No slice support.")
        layout = self._content_layout
        data_widget_item = layout.itemAt(index)
        if data_widget_item is not None:
            return data_widget_item.widget()
        else:
            raise IndexError("{index!r}".format(**locals()))


    def __setitem__(self, index, data_widget):
        if isinstance(index, slice):
            raise NotImplementedError("No slice support.")
        del self[index]
        layout = self._content_layout
        layout.insertWidget(index, data_widget)


    def __delitem__(self, index):
        if isinstance(index, slice):
            raise NotImplementedError("No slice support.")
        layout = self._content_layout
        removed_item = layout.takeAt(index)
        if removed_item is not None:
            removed_item.widget().setParent(None)
        else:
            raise IndexError("{index!r}".format(**locals()))


    def insert(self, index, data_widget):
        layout = self._content_layout
        layout.insertWidget(index, data_widget)


    def get_data(self):
        """
        dict like list items [(key, value), ...]
        """
        return [(data_widget.objectName(), data_widget.data) for data_widget in self]


    @QSlot(list)
    def set_data(self, new_data):
        """
        dict like list items [(key, value), ...]
        """
        self.clear()
        self.extend(data_widget_mapper.create_widget(value, name=key) for key, value in new_data)
        self.data_changed.emit(self.get_data())


    data_changed = QSignal(list)
    data = QProperty(list, fget=get_data, fset=set_data, notify=data_changed)


    def minimumSizeHint(self):
        return QSize(200, 200)


class DictWidget(Section, MutableMapping, metaclass=MetaMeta):
    def __init__(self, parent=None):
        Section.__init__(self, parent=parent)
        self._label_width = 110


    def create_ui(self):  # super calls this create_ui
        Section.create_ui(self)  # this calls super create_ui
        edit_menu = self.menu_bar().addMenu(i18n("Edit"))
        content = QWidget()
        content.setObjectName("dict_content")
        content.setStyleSheet("""
                .QWidget#dict_content {
                    background-color: palette(window);
                    border: 1px outset rgba(0, 0, 0, 10%);
                    border-radius: 3px;
                }""")
        self._content_layout = QFormLayout()
        self._content_layout.setContentsMargins(40, 10, 4, 10)
        content.setLayout(self._content_layout)
        self.set_content(content)


    def __len__(self):
        return self._content_layout.rowCount()


    def __iter__(self):
        layout = self._content_layout
        for row in range(layout.rowCount()):
            span_item = layout.itemAt(row, QFormLayout.SpanningRole)
            if span_item is not None:
                yield span_item.widget().objectName()
            else:
                field_item = layout.itemAt(row, QFormLayout.FieldRole)
                yield field_item.widget().objectName()


    def __getitem__(self, key):
        layout = self._content_layout
        for row in range(layout.rowCount()):
            widget = None
            span_item = layout.itemAt(row, QFormLayout.SpanningRole)
            if span_item is not None:
                widget = span_item.widget()
            else:
                field_item = layout.itemAt(row, QFormLayout.FieldRole)
                widget = field_item.widget()
            if (widget is not None) and (widget.objectName() == key):
                return widget
        raise KeyError("{key!r}".format(**locals()))


    def __setitem__(self, key, widget):
        layout = self._content_layout
        for row in range(layout.rowCount()):
            found = False
            span_item = layout.itemAt(row, QFormLayout.SpanningRole)
            if span_item is not None:
                if span_item.widget().objectName() == key:
                    found = True
            else:
                field_item = layout.itemAt(row, QFormLayout.FieldRole)
                if field_item.widget().objectName() == key:
                    found = True
            if found:
                layout.removeRow(row)
                if isinstance(widget, Section):
                    widget.title = key
                    widget.setObjectName(key)
                    layout.insertRow(row, widget)
                else:
                    widget.setObjectName(key)
                    layout.insertRow(row, key, widget)
                    label_item = layout.itemAt(row, QFormLayout.LabelRole)
                    label_widget = label_item.widget()
                    label_widget.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    label_widget.setFixedWidth(self._label_width)  # elide right missing...
                break
        else:
            if isinstance(widget, Section):
                widget.title = key
                widget.setObjectName(key)
                layout.addRow(widget)
            else:
                widget.setObjectName(key)
                key_label = QLabel(key)
                key_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                key_label.setFixedWidth(self._label_width)  # elide right missing...
                layout.addRow(key_label, widget)


    def __delitem__(self, key):
        layout = self._content_layout
        for row in range(layout.rowCount()):
            span_item = layout.itemAt(row, QFormLayout.SpanningRole)
            if span_item is not None:
                if span_item.widget().objectName() == key:
                    layout.removeRow(row)
                    break
            else:
                field_item = layout.itemAt(row, QFormLayout.FieldRole)
                if field_item.widget().objectName() == key:
                    layout.removeRow(row)
                    break
        else:
            raise KeyError("{key!r}".format(**locals()))


    def _refresh_rows(self):
        layout = self._content_layout
        for row in range(layout.rowCount()):
            label_item = layout.itemAt(row, QFormLayout.LabelRole)
            if label_item is not None:
                label_widget = label_item.widget()
                label_widget.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                label_widget.setFixedWidth(self._label_width)  # elide right missing...


    def get_label_width(self):
        return self._label_width


    @QSlot(int)
    def set_label_width(self, new_label_width):
        new_label_width = int(new_label_width)
        old_label_width = self.get_label_width()
        if new_label_width != old_label_width:
            self._label_width = new_label_width
            self._refresh_rows()
            self.label_width_changed.emit(self.get_label_width())


    label_width_changed = QSignal(int)
    label_width = QProperty(int, fget=get_label_width, fset=set_label_width, notify=label_width_changed)


    def get_data(self):
        return oDict((name, data_widget.data) for name, data_widget in self.items())


    QSlot(dict)
    def set_data(self, new_data):
        self.clear()
        MutableMapping.update(self, ((key, data_widget_mapper.create_widget(value, name=key)) for key, value in new_data.items()))
        self.data_changed.emit(self.get_data())


    data_changed = QSignal(dict)
    data = QProperty(dict, fget=get_data, fset=set_data, notify=data_changed, user=True)


class ListWidget(Section, MutableSequence, metaclass=MetaMeta):
    def __init__(self, parent=None):
        Section.__init__(self, parent=parent)
        self._label_width = 110


    def create_ui(self):  # super calls this create_ui
        Section.create_ui(self)  # this calls super create_ui
        edit_menu = self.menu_bar().addMenu(i18n("Edit"))
        content = QWidget()
        content.setObjectName("list_content")
        content.setStyleSheet("""
                .QWidget#list_content {
                    background-color: palette(window);
                    border: 1px outset rgba(0, 0, 0, 10%);
                    border-radius: 3px;
                }""")
        self._content_layout = QFormLayout()
        self._content_layout.setContentsMargins(40, 10, 4, 10)
        content.setLayout(self._content_layout)
        self.set_content(content)


    def format_index(self, index):
        return "[ {index} ]".format(index=index)


    def __len__(self):
        return self._content_layout.rowCount()


    def __getitem__(self, index):
        if isinstance(index, slice):
            NotImplementedError("No slice support!")
        layout = self._content_layout
        index = (layout.rowCount() - index) if index < 0 else index
        if 0 <= index < layout.rowCount():
            widget = None
            span_item = layout.itemAt(index, QFormLayout.SpanningRole)
            if span_item is not None:
                return span_item.widget()
            else:
                field_item = layout.itemAt(index, QFormLayout.FieldRole)
                return field_item.widget()
        else:
            raise IndexError("{index!r}".format(**locals()))


    def __setitem__(self, index, widget):
        if isinstance(index, slice):
            NotImplementedError("No slice support!")
        layout = self._content_layout
        index = (layout.rowCount() - index) if index < 0 else index
        if 0 <= index < layout.rowCount():
            del self[index]
            nice_text = self.format_index(index)
            if isinstance(widget, Section):
                widget.title = nice_text
                layout.insertRow(index, widget)
            else:
                index_label = QLabel(nice_text)
                index_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                index_label.setFixedWidth(self._label_width)  # elide right missing...
                layout.insertRow(index, index_label, widget)
            self._refresh_rows()
        else:
            raise IndexError("{index!r}".format(**locals()))


    def __delitem__(self, index):
        if isinstance(index, slice):
            NotImplementedError("No slice support!")
        layout = self._content_layout
        index = (layout.rowCount() - index) if index < 0 else index
        if 0 <= index < layout.rowCount():
            layout.removeRow(index)
            self._refresh_rows()
        else:
            raise IndexError("{index!r}".format(**locals()))


    def insert(self, index, widget):
        layout = self._content_layout
        nice_text = self.format_index(index)
        if isinstance(widget, Section):
            widget.title = nice_text
            layout.insertRow(index, widget)
        else:
            index_label = QLabel(nice_text)
            index_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            index_label.setFixedWidth(self._label_width)  # elide right missing...
            layout.insertRow(index, index_label, widget)
        self._refresh_rows()


    def _refresh_rows(self):
        layout = self._content_layout
        for index in range(layout.rowCount()):
            label_widget = None
            span_item = layout.itemAt(index, QFormLayout.SpanningRole)
            if span_item is not None:
                label_widget = span_item.widget()
            else:
                label_item = layout.itemAt(index, QFormLayout.LabelRole)
                label_widget = label_item.widget()
            nice_text = self.format_index(index)
            if isinstance(label_widget, Section):
                label_widget.title = nice_text
            else:
                label_widget.setText(nice_text)
                label_widget.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                label_widget.setFixedWidth(self._label_width)  # elide right missing...


    def get_label_width(self):
        return self._label_width


    @QSlot(int)
    def set_label_width(self, new_label_width):
        new_label_width = int(new_label_width)
        old_label_width = self.get_label_width()
        if new_label_width != old_label_width:
            self._label_width = new_label_width
            self._refresh_rows()
            self.label_width_changed.emit(self.get_label_width())


    label_width_changed = QSignal(int)
    label_width = QProperty(int, fget=get_label_width, fset=set_label_width, notify=label_width_changed)


    def get_data(self):
        return [data_widget.data for data_widget in self]


    QSlot(list)
    def set_data(self, new_data):
        self.clear()
        self.extend(data_widget_mapper.create_widget(value, name=self.format_index(index)) for index, value in enumerate(new_data))
        self.data_changed.emit(self.get_data())


    data_changed = QSignal(list)
    data = QProperty(list, fget=get_data, fset=set_data, notify=data_changed, user=True)


class NoneWidget(QLabel):
    def __init__(self, parent=None):
        super(NoneWidget, self).__init__("None", parent=parent)


    def get_data(self):
        return None


    QSlot(type(None))
    def set_data(self, new_data):
        if new_data is not None:
            raise RuntimeError("Not None. (did get: {new_data})".format(**locals()))


    data_changed = QSignal(type(None))
    data = QProperty(type(None), fget=get_data, fset=set_data, notify=data_changed, user=True)

data_widget_mapper.register(type(None), NoneWidget)


class BoolWidget(QCheckBox):
    def __init__(self, parent=None):
        super(BoolWidget, self).__init__(parent=parent)
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

data_widget_mapper.register(bool, BoolWidget)


class IntWidget(QSpinBox):
    def __init__(self, parent=None):
        super(IntWidget, self).__init__(parent=parent)
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

data_widget_mapper.register(int, IntWidget)


class FloatWidget(QDoubleSpinBox):
    def __init__(self, parent=None):
        super(FloatWidget, self).__init__(parent=parent)
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

data_widget_mapper.register(float, FloatWidget)


class StringWidget(QLineEdit):
    def __init__(self, parent=None):
        super(StringWidget, self).__init__(parent=parent)
        self.setStyleSheet(".StringWidget {padding-left: 3px;}")
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

data_widget_mapper.register(UnicodeType, StringWidget)


class BytesWidget(QPlainTextEdit):
    def __init__(self, parent=None):
        super(BytesEditor, self).__init__(parent=parent)
        self._data = b''
        self.setReadOnly(True)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setForegroundRole(QPalette.BrightText)  # or green text?
        self.setBackgroundRole(QPalette.Dark)  # dark background
        self.setFont(QFont("Courier"))


    def _chunks(self, text, chunk_length):
        for chunk in (text[i:i + chunk_length] for i in range(0, len(text), chunk_length)):
            yield chunk


    def get_data(self):
        # hex_text = self.toPlainText()
        # hex_str = re.sub(r"\s", "", hex_text)
        # data = bytes.fromhex(hex_str)
        # return data
        return self._data


    def set_data(self, new_data):
        self._data = new_data
        new_data = bytes(new_data)
        hex_str = new_data.hex()
        sc = self._chunks
        hex_text = "\n".join(" ".join(sc(line, 2)) for line in sc(hex_str, 32))
        self.setPlainText(hex_text)


data_widget_mapper.register(BytesType, BytesWidget)
