import base64
from enum import IntEnum

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtGui import QPalette, QFont, QColor

from PyQt5.QtWidgets import QPlainTextEdit, QActionGroup

from layer_extra_properties.common.utils_py import \
        first, last, UnicodeType, BytesType

from .data_editor_mapper import data_editor_mapper


class ViewMode(IntEnum):
    HEX = 0
    BASE64 = 1


class BytesEditor(QPlainTextEdit):
    """
    Editing is not supported in BytesEditor. (not implemented!)
    view mode HEX / BASE64
    """
    def __init__(self, parent=None):
        super(BytesEditor, self).__init__(parent=parent)
        self._view_mode = ViewMode.HEX
        self._data = b''
        # self.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.setReadOnly(True)
        self.setBackgroundRole(QPalette.Dark)  # dark background
        palette = self.palette()
        palette.setColor(QPalette.Text, QColor(10, 200, 10))
        self.setPalette(palette)
        self.setFont(QFont("Courier"))
        # self.textChanged.connect(lambda : self.data_changed.emit(self.get_data()))


    def contextMenuEvent(self, e):
        menu = self.createStandardContextMenu()
        mode_group = QActionGroup(menu)

        view_hex = menu.addAction(i18n("View HEX"))
        view_hex.setCheckable(True)
        if self.get_view_mode() == ViewMode.HEX:
            view_hex.setChecked(True)
        view_hex.triggered.connect(lambda checked: self.set_view_mode(ViewMode.HEX))
        mode_group.addAction(view_hex)

        view_base64 = menu.addAction(i18n("View BASE64"))
        view_base64.setCheckable(True)
        if self.get_view_mode() == ViewMode.BASE64:
            view_base64.setChecked(True)
        view_base64.triggered.connect(lambda checked: self.set_view_mode(ViewMode.BASE64))
        mode_group.addAction(view_base64)

        menu.exec(e.globalPos())


    def _chunks(self, text, chunk_length):
        for chunk in (text[i:i + chunk_length] for i in range(0, len(text), chunk_length)):
            yield chunk


    def _update_text(self):
        if self._view_mode == ViewMode.HEX:
            hex_str = self._data.hex()
            sc = self._chunks
            hex_text = "\n".join(" ".join(sc(line, 2)) for line in sc(hex_str, 32))
            self.setPlainText(hex_text)
            self.setLineWrapMode(QPlainTextEdit.NoWrap)
        else:
            base64_text = base64.b64encode(self._data).decode('ascii')
            self.setPlainText(base64_text)
            self.setLineWrapMode(QPlainTextEdit.WidgetWidth)


    def get_view_mode(self):
        return self._view_mode


    @QSlot(ViewMode)
    def set_view_mode(self, new_view_mode):
        new_view_mode = ViewMode(new_view_mode)
        old_view_mode = self.get_view_mode()
        if new_view_mode != old_view_mode:
            self._view_mode = new_view_mode
            self._update_text()
            self.view_mode_changed.emit(self.get_view_mode())


    view_mode_changed = QSignal(ViewMode)
    view_mode = QProperty(ViewMode, fget=get_view_mode, fset=set_view_mode, notify=view_mode_changed)


    def get_data(self):
        # hex_text = self.toPlainText()
        # hex_str = re.sub(r"\s", "", hex_text)
        # data = bytes.fromhex(hex_str)
        # return data
        return self._data


    QSlot(BytesType)
    def set_data(self, new_data):
        self._data = BytesType(new_data)
        self._update_text()
        self.data_changed.emit(self.get_data())


    data_changed = QSignal(BytesType)  # note: never changes!
    data = QProperty(BytesType, fget=get_data, fset=set_data, notify=data_changed, user=True)


data_editor_mapper.register(BytesType, BytesEditor)
