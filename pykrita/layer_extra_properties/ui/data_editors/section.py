from enum import IntEnum
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
        QWidget, QFrame, QLabel, QMenuBar, QHBoxLayout, QVBoxLayout, \
        QToolButton, QGraphicsDropShadowEffect

from layer_extra_properties.common.utils_py import \
        first, last, UnicodeType, BytesType


class Folding(IntEnum):
    COLLAPSED = 0
    EXPANDED = 1


class TitleBar(QFrame):
    def __init__(self, foldable=None, folding=None,  parent=None):
        super(TitleBar, self).__init__(parent=parent)
        self.setObjectName("title_bar")
        self.create_ui()
        self.set_foldable(True if foldable is None else foldable)
        self.set_folding(Folding.COLLAPSED if folding is None else folding)


    def create_ui(self):
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.Window)
        bg_role = self.backgroundRole()
        palette = self.palette()
        old_color = palette.color(bg_role)
        bar_color = old_color.lighter(120)
        palette.setColor(bg_role, bar_color)
        self.setPalette(palette)
        # layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        # folding button
        self._folding = QToolButton()
        self._folding.setCheckable(True)
        self._folding.setChecked(True)
        self._folding.setStyleSheet(
                        ('.QToolButton {border: none;}'
                         '.QToolButton:hover {border: 1px;}'
                         '.QToolButton:pressed {border: 1px;}'))
        layout.addWidget(self._folding)
        # title label
        self._title = QLabel()
        self._title.setContentsMargins(8, 0, 8, 0)
        layout.addWidget(self._title)
        # stretch
        layout.addStretch(stretch=100)
        # menu bar
        self._menu_bar = QMenuBar()
        self._menu_bar.setBackgroundRole(QPalette.Window)
        bg_role = self._menu_bar.backgroundRole()
        palette = self._menu_bar.palette()
        palette.setColor(bg_role, bar_color)
        self._menu_bar.setPalette(palette)
        layout.addWidget(self._menu_bar)
        # connect signals
        self._folding.toggled.connect(self.on_folding_toggled)
        self._folding.toggled.connect(lambda c: self.folding_changed.emit(Folding.EXPANDED if c else Folding.COLLAPSED))


    def on_folding_toggled(self, checked):
        self._folding.setArrowType(Qt.DownArrow if checked else Qt.RightArrow)


    def get_foldable(self):
        return self._folding.isVisibleTo(self)


    @QSlot(bool)
    def set_foldable(self, new_foldable):
        if not new_foldable:
            # about to remove ability to fold, do expanding!
            self.folding = Folding.EXPANDED
        self._folding.setVisible(new_foldable)


    foldable = QProperty(bool, fget=get_foldable, fset=set_foldable)


    def get_folding(self):
        return self._folding.isChecked()


    @QSlot(Folding)
    def set_folding(self, new_folding):
        if not self.foldable:
            return  # no folding!
        if new_folding == Folding.COLLAPSED:
            self._folding.setChecked(False)
        else:
            self._folding.setChecked(True)
        # toggled signal is chained folding_changed


    folding_changed = QSignal(Folding)
    folding = QProperty(Folding, fget=get_folding, fset=set_folding, notify=folding_changed, user=True)


    def get_title(self):
        return self._title.text()


    @QSlot(UnicodeType)
    def set_title(self, new_title):
        self._title.setText(new_title)


    title = QProperty(UnicodeType, fget=get_title, fset=set_title)


    def menu_bar(self):
        return self._menu_bar


    def mouseReleaseEvent(self, e):
        def hit_test(pos):
            return self.rect().contains(pos)

        if e.button() != Qt.LeftButton:
            e.ignore()
            return
        if hit_test(e.pos()):
            new_state = Folding.COLLAPSED if self.get_folding() == Folding.EXPANDED else Folding.EXPANDED
            self.set_folding(new_state)
            e.accept()
        else:
            e.ignore()


class Section(QWidget):
    def __init__(self, foldable=None, folding=None, parent=None):
        super(Section, self).__init__(parent=parent)
        self.setObjectName("section")
        self.create_ui()
        self.set_foldable(True if foldable is None else foldable)
        self.set_folding(Folding.COLLAPSED if folding is None else folding)


    def create_ui(self):
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(10)
        self._shadow.setColor(QColor(0, 0, 0, 80))
        self._shadow.setOffset(2, 2)
        self.setGraphicsEffect(self._shadow)
        # layout
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)
        # title bar
        self._title_bar = TitleBar()
        layout.addWidget(self._title_bar)
        # content
        self._content = None
        # connect signals
        self._title_bar.folding_changed.connect(self.on_title_bar_folding_changed)
        self._title_bar.folding_changed.connect(self.folding_changed)


    def on_title_bar_folding_changed(self, folding):
        if self._content is not None:
            if folding == Folding.EXPANDED:
                self._content.setVisible(True)
            else:
                self._content.setVisible(False)


    def get_title(self):
        return self._title_bar.title


    @QSlot(UnicodeType)
    def set_title(self, new_title):
        self._title_bar.title = new_title


    title = QProperty(UnicodeType, fget=get_title, fset=set_title)


    def get_foldable(self):
        return self._title_bar.foldable


    @QSlot(bool)
    def set_foldable(self, new_foldable):
        self._title_bar.foldable = new_foldable


    foldable = QProperty(bool, fget=get_foldable, fset=set_foldable)


    def get_folding(self):
        return self._title_bar.folding


    @QSlot(Folding)
    def set_folding(self, new_folding):
        self._title_bar.folding = new_folding


    folding_changed = QSignal(Folding)
    folding = QProperty(Folding, fget=get_folding, fset=set_folding, notify=folding_changed)


    def title_bar(self):
        return self._title_bar


    def menu_bar(self):
        return self._title_bar.menu_bar()


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
            new_content.setVisible(self.folding == Folding.EXPANDED)