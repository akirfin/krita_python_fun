"""

How to use:

from camera_layer.layer_properties.layer_properties_hook import \
        LayerPropertiesHook

LayerPropertiesHook.register()

"""
from collections import OrderedDict as oDict

from krita import Krita

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtCore import \
        QObject, QEvent, QSize, QTimer

from PyQt5.QtGui import \
        QPalette

from PyQt5.QtWidgets import \
        QWidget, QDialog, QStackedLayout, QScrollArea, \
        QApplication, QTextEdit

from camera_layer.common.utils_py import \
        print_console, first, last, UnicodeType, BytesType

from camera_layer.common.utils_kis import \
        get_active_node

from .widget_mapper import \
        widget_mapper

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
        self._scroll_area.setBackgroundRole(QPalette.Base)
        self._scroll_area.setWidgetResizable(True)
        layout.addWidget(self._scroll_area)


    def pull_data(self):
        def get_meta_data(_result):
            qapp = QApplication.instance()
            for w in qapp.topLevelWidgets():
                if isinstance(w, QDialog):
                    if w.metaObject().className() == "KisMetaDataEditor":
                        dialog = w
                        edit_description = dialog.findChild(QTextEdit, "editDescription")
                        _result.append(edit_description.toPlainText())
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
                        edit_description = dialog.findChild(QTextEdit, "editDescription")
                        edit_description.setPlainText(_new_text)
                        dialog.accept()

        # target node must be activeNode!
        QTimer.singleShot(0, lambda text=data: set_text(text))
        Krita.instance().action("EditLayerMetaData").trigger()


    def minimumSizeHint(self):
        return QSize(200, 200)


class LayerPropertiesHook(QObject):
    _alive = list()
    _hook = None

    @classmethod
    def register(cls):
        cls.unregister()
        cls._hook = cls()
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
        return super(LayerPropertiesHook, self).eventFilter(obj, event)
