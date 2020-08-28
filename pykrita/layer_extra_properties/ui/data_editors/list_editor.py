from collections import OrderedDict as oDict
try:
    from collections.abc import MutableSequence
except:
    from collections import MutableSequence

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtWidgets import \
        QWidget, QFormLayout, QLabel

from .meta_meta import MetaMeta
from .section import Section

from .data_editor_mapper import data_editor_mapper


class ListEditor(Section, MutableSequence, metaclass=MetaMeta):
    def __init__(self, parent=None):
        Section.__init__(self, parent=parent)
        self._label_width = 110


    def create_ui(self):  # super calls this create_ui
        Section.create_ui(self)  # this calls super create_ui
        edit_menu = self.menu_bar().addMenu(i18n("Edit"))
        edit_menu.addAction("Add Field")
        edit_menu.addAction("Edit Field")
        edit_menu.addAction("Remove Field")
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
            span_item = layout.itemAt(index, QFormLayout.SpanningRole)
            if span_item is not None:
                return span_item.widget()
            else:
                field_item = layout.itemAt(index, QFormLayout.FieldRole)
                return field_item.widget()
        else:
            raise IndexError("{index!r}".format(**locals()))


    def __setitem__(self, index, editor):
        if isinstance(index, slice):
            NotImplementedError("No slice support!")
        layout = self._content_layout
        index = (layout.rowCount() - index) if index < 0 else index
        if 0 <= index < layout.rowCount():
            del self[index]
            nice_text = self.format_index(index)
            if isinstance(editor, Section):
                editor.title = nice_text
                layout.insertRow(index, editor)
            else:
                index_label = QLabel(nice_text)
                index_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                index_label.setFixedWidth(self._label_width)  # elide right missing...
                layout.insertRow(index, index_label, editor)
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


    def insert(self, index, editor):
        layout = self._content_layout
        nice_text = self.format_index(index)
        if isinstance(editor, Section):
            editor.title = nice_text
            layout.insertRow(index, editor)
        else:
            index_label = QLabel(nice_text)
            index_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            index_label.setFixedWidth(self._label_width)  # elide right missing...
            layout.insertRow(index, index_label, editor)
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
        return [data_editor.data for data_editor in self]


    QSlot(list)
    def set_data(self, new_data):
        self.clear()
        self.extend(data_editor_mapper.create_editor(value, title=self.format_index(index)) for index, value in enumerate(new_data))
        self.data_changed.emit(self.get_data())


    data_changed = QSignal(list)
    data = QProperty(list, fget=get_data, fset=set_data, notify=data_changed, user=True)


data_editor_mapper.register(list, ListEditor)
