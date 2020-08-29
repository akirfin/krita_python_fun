from collections import OrderedDict as oDict
try:
    from collections.abc import MutableMapping
except:
    from collections import MutableMapping

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtWidgets import \
        QWidget, QFormLayout, QLabel

from .abc_editor_container import AbcEditorContainer
from .data_editor_mapper import data_editor_mapper


class DictEditor(AbcEditorContainer, MutableMapping):
    def __init__(self, parent=None):
        AbcEditorContainer.__init__(self, parent=parent)
        self._label_width = 110


    def create_ui(self):  # super calls this create_ui
        AbcEditorContainer.create_ui(self)  # this calls super create_ui

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
            editor = None
            span_item = layout.itemAt(row, QFormLayout.SpanningRole)
            if span_item is not None:
                editor = span_item.widget()
            else:
                field_item = layout.itemAt(row, QFormLayout.FieldRole)
                editor = field_item.widget()
            if (editor is not None) and (editor.objectName() == key):
                return editor
        raise KeyError("{key!r}".format(**locals()))


    def __setitem__(self, key, editor):
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
                if isinstance(editor, AbcEditorContainer):
                    editor.title = key
                    editor.setObjectName(key)
                    layout.insertRow(row, editor)
                else:
                    editor.setObjectName(key)
                    layout.insertRow(row, key, editor)
                    label_item = layout.itemAt(row, QFormLayout.LabelRole)
                    label_widget = label_item.widget()
                    label_widget.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    label_widget.setFixedWidth(self._label_width)  # elide right missing...
                break
        else:
            if isinstance(editor, AbcEditorContainer):
                editor.title = key
                editor.setObjectName(key)
                layout.addRow(editor)
            else:
                editor.setObjectName(key)
                key_label = QLabel(key)
                key_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                key_label.setFixedWidth(self._label_width)  # elide right missing...
                layout.addRow(key_label, editor)


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
        return oDict((name, data_editor.data) for name, data_editor in self.items())


    QSlot(oDict)
    def set_data(self, new_data):
        self.clear()
        for key, value in new_data.items():
            self[key] = data_editor_mapper.create_editor(value, title=key)
        self.data_changed.emit(self.get_data())


    data_changed = QSignal(oDict)
    data = QProperty(oDict, fget=get_data, fset=set_data, notify=data_changed, user=True)


data_editor_mapper.register(oDict, DictEditor)
