from collections import OrderedDict as oDict
try:
    from collections.abc import Mapping, Iterable
except:
    from collections import Mapping, Iterable

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtCore import \
        QObject

from PyQt5.QtGui import \
        QPalette, QColor

from PyQt5.QtWidgets import \
        QWidget, QFrame, QLabel, QLineEdit, QSpinBox, QDoubleSpinBox, QCheckBox, \
        QMenuBar, QFormLayout, QHBoxLayout, QVBoxLayout, QToolButton, QGraphicsDropShadowEffect

from layer_extra_properties.common.utils_py import \
        first, last, UnicodeType, BytesType


class Section(QWidget):
    def __init__(self, folding=None, parent=None):
        super(Section, self).__init__(parent=parent)
        self.setObjectName("section")
        self.create_ui()
        if folding is not None:
            self.folding = folding


    def create_ui(self):
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(10)
        self._shadow.setColor(QColor(0, 0, 0, 80))
        self._shadow.setOffset(2, 2)
        self.setGraphicsEffect(self._shadow)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        self._title_bar = QFrame()
        self._title_bar.setAutoFillBackground(True)
        self._title_bar.setBackgroundRole(QPalette.Window)
        bg_role = self._title_bar.backgroundRole()
        palette = self._title_bar.palette()
        old_color = palette.color(bg_role)
        bar_color = old_color.lighter(120)
        palette.setColor(bg_role, bar_color)
        self._title_bar.setPalette(palette)
        layout.addWidget(self._title_bar)

        title_bar_layout = QHBoxLayout()
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        self._title_bar.setLayout(title_bar_layout)

        self._folding = QToolButton()
        self._folding.setCheckable(True)
        self._folding.setStyleSheet(
                        ('.QToolButton {border: none;}'
                         '.QToolButton:hover {border: 1px;}'
                         '.QToolButton:pressed {border: 1px;}'))
        title_bar_layout.addWidget(self._folding)

        self._title = QLabel("")
        self._title.setContentsMargins(8, 0, 8, 0)
        title_bar_layout.addWidget(self._title)

        title_bar_layout.addStretch(stretch=100)

        self._menu_bar = QMenuBar()
        self._menu_bar.setBackgroundRole(QPalette.Window)
        bg_role = self._menu_bar.backgroundRole()
        palette = self._menu_bar.palette()
        palette.setColor(bg_role, bar_color)
        self._menu_bar.setPalette(palette)

        title_bar_layout.addWidget(self._menu_bar)

        self._content = None

        # connect signals
        self._folding.clicked.connect(self.on_toggle_folding)
        self._folding.toggled.connect(self.folding_changed)
        self.on_toggle_folding(True)


    def on_toggle_folding(self, checked=None):
        self._folding.setChecked(checked)
        if self._folding.isChecked():
            self._folding.setArrowType(Qt.DownArrow)
            if self._content is not None:
                self._content.setVisible(True)
        else:
            self._folding.setArrowType(Qt.RightArrow)
            if self._content is not None:
                self._content.setVisible(False)


    def get_title(self):
        return self._title.text()


    @QSlot(UnicodeType)
    def set_title(self, new_title):
        self._title.setText(new_title)


    title = QProperty(UnicodeType, fget=get_title, fset=set_title)


    def get_folding(self):
        return self._folding.isChecked()


    @QSlot(bool)
    def set_folding(self, new_folding):
        new_folding = bool(new_folding)
        old_folding = self.get_folding()
        if new_folding != old_folding:
            self._folding.setChecked(new_folding)
            # toggled signal is chained folding_changed


    folding_changed = QSignal(bool)
    folding = QProperty(UnicodeType, fget=get_folding, fset=set_folding, notify=folding_changed, user=True)


    def menu_bar(self):
        return self._menu_bar


    def get_content(self):
        return self._content


    def set_content(self, new_content):
        old_content = self.get_content()
        if old_content is not None:
            # remove old content, and unparent
            layout.removeWidget(old_content)
            if old_content.parent() is self:
                old_content.setParent(None)
        self._content = new_content
        if new_content is not None:
            # add new content
            layout = self.layout()
            layout.addWidget(new_content)
