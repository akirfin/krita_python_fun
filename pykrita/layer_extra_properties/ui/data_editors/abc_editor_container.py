from uuid import uuid4, UUID
from enum import IntEnum
from abc import ABCMeta
from collections import OrderedDict as oDict
try:
    from collections.abc import Mapping, Iterable
except:
    from collections import Mapping, Iterable

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtCore import QObject

from PyQt5.QtGui import \
        QPalette, QColor

from PyQt5.QtWidgets import \
        QWidget, QFrame, QLabel, QMenuBar, QMenu, QHBoxLayout, QVBoxLayout, \
        QToolButton, QGraphicsDropShadowEffect, QListWidget, QListWidgetItem, \
        QDialog, QStyle

from layer_extra_properties.common.utils_py import \
        first, last, UnicodeType, BytesType


class MetaMeta(type(QObject), ABCMeta):
    """
    Too meta for me, so thats why the name!
    (Nothing to see, move along...)

    Union of Shiboken.ObjectType & ABCmeta metaclasses.
    Allows use of collections.abc interfaces with QObjects.
    """


class FieldEditor(QDialog):
    def __init__(self, target,  parent=None):
        super(FieldEditor, self).__init__(parent=parent)
        self.setObjectName("field_editor")
        self._target = target
        self.create_ui()
        self.build_view()


    def build_view(self):
        target = self._target
        view = self._view
        view.clear()
        if isinstance(target, Mapping):
            for name, data_editor in target.items():
                data_type = type(data_editor.data)
                item = QListWidgetItem()
                text = "{name} ({data_type.__name__})".format(**locals())
                item.setText(text)
                view.addItem(item)
        else:  # list
            for index, data_editor in enumerate(target):
                data_type = type(data_editor.data)
                item = QListWidgetItem()
                text = "[ {index} ] ({data_type.__name__})".format(**locals())
                item.setText(text)
                view.addItem(item)


    def create_ui(self):
        import layer_extra_properties.ui.data_editors.data_editor_mapper as data_editor_mapper

        layout = QVBoxLayout()
        self.setLayout(layout)

        self._view = QListWidget()
        # add items for existing fileds
        layout.addWidget(self._view)

        buttons = QWidget()
        layout.addWidget(buttons)

        buttons_layout = QHBoxLayout()
        buttons.setLayout(buttons_layout)

        self._add_field_menu = menu = QMenu()
        for data_type, editor_type in data_editor_mapper:
            add_action = menu.addAction(data_type.__name__)
            add_action.triggered.connect(lambda _, et=editor_type: self.add_field(et))

        self._add_field = QToolButton()
        self._add_field.setText("+")
        self._add_field.setPopupMode(QToolButton.InstantPopup)
        self._add_field.setMenu(menu)
        buttons_layout.addWidget(self._add_field, alignment=Qt.AlignLeft)

        # move field down

        # move field up

        buttons_layout.addStretch(100)

        add_icon = self.style().standardIcon(QStyle.SP_DialogDiscardButton)
        self._del_selected_fields = QToolButton()
        buttons_layout.addWidget(self._del_selected_fields, alignment=Qt.AlignRight)


    def add_field(self, editor_type):
        target = self._target
        if isinstance(target, Mapping):
            data_editor = editor_type()
            new_name = "field_{}".format(uuid4().hex)
            self._target[new_name] = data_editor
            self.build_view()
            # start name editor on new item
        else:
            data_editor = editor_type()
            self._target.append(data_editor)
            self.build_view()


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


class AbcEditorContainer(QWidget, metaclass=MetaMeta):
    def __init__(self, foldable=None, folding=None, parent=None):
        super(AbcEditorContainer, self).__init__(parent=parent)
        self.setObjectName("abc_editor_container")
        self.create_ui()
        self.set_foldable(True if foldable is None else foldable)
        self.set_folding(Folding.COLLAPSED if folding is None else folding)


    def create_ui(self):
        # layout
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

        self.create_shadow()

        self.create_title_bar()

        self.create_content()


    def create_shadow(self):
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(10)
        self._shadow.setColor(QColor(0, 0, 0, 80))
        self._shadow.setOffset(2, 2)
        self.setGraphicsEffect(self._shadow)


    def create_title_bar(self):
        # title bar
        self._title_bar = TitleBar()
        layout.addWidget(self._title_bar)

        edit_menu = self.menu_bar().addMenu(i18n("Edit Schema"))  # gear icon!
        edit_fields = edit_menu.addAction("Edit Schema")
        edit_fields.triggered.connect(self.on_edit_fields)

        # connect signals
        self._title_bar.folding_changed.connect(self.on_title_bar_folding_changed)
        self._title_bar.folding_changed.connect(self.folding_changed)


    def create_content(self):
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


    def on_title_bar_folding_changed(self, folding):
        if self._content is not None:
            if folding == Folding.EXPANDED:
                self._content.setVisible(True)
            else:
                self._content.setVisible(False)


    def on_edit_fields(self):
        dialog = self.create_standard_field_editor()
        dialog.exec_()


    def create_standard_field_editor(self):
        return FieldEditor(target=self)


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
