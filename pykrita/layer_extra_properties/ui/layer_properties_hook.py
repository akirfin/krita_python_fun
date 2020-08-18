"""

How to use:

from layer_extra_properties.ui.layer_properties_hook import \
        LayerPropertiesHook

LayerPropertiesHook.register()

"""

from collections import OrderedDict as oDict

from krita import Krita, Node

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtCore import \
        QObject, QEvent, QSize

from PyQt5.QtGui import \
        QPalette, QColor

from PyQt5.QtWidgets import \
        QWidget, QDialog, QStackedLayout, QScrollArea, \
        QApplication

from layer_extra_properties.common.utils_py import \
        print_console, first, last, UnicodeType, BytesType

from layer_extra_properties.common.utils_kis import \
        get_active_node

from layer_extra_properties.common.data_serializer import \
        serializer

from layer_extra_properties.layer_meta_data import \
        get_layer_meta_data, set_layer_meta_data

from .widget_mapper import \
        widget_mapper


class LayerExtraPropertiesWidget(QWidget):
    def __init__(self, node=None, parent=None):
        super(LayerExtraPropertiesWidget, self).__init__(parent=parent)
        self._node = None
        self.setObjectName("layer_extra_properties_widget")
        self.create_ui()
        if node is not None:
            self.node = node


    def create_ui(self):
        layout = QStackedLayout()
        self.setLayout(layout)

        self._scroll_area = QScrollArea()
        self._scroll_area.setBackgroundRole(QPalette.Base)
        self._scroll_area.setWidgetResizable(True)
        layout.addWidget(self._scroll_area)


    def pull_data(self):
        meta_data = get_layer_meta_data(self._node)
        try:
            data = serializer.loads(meta_data)
        except:
            data = oDict()
        content = widget_mapper.create_widget(data)
        content.setObjectName("layer_extra_properties")
        content.title = "Layer Extra Properties"
        old_widget = self._scroll_area.widget()
        self._scroll_area.setWidget(content)
        content.node = self._node
        if old_widget is not None:
            old_widget.deletelater()
            old_widget.setParent(None)


    @QSlot()
    def push_data(self):
        content = self._scroll_area.widget()
        meta_data = "{}" if content is None else serializer.dumps(content.data)
        set_layer_meta_data(self._node, meta_data)


    def get_node(self):
        return self._node


    @QSlot(object)
    def set_node(self, new_node):
        if not isinstance(new_node, (Node, type(None))):
            raise RuntimeError("Bad node, must be Node or None. (did get: {new_node})".format(**locals()))
        old_node = self.get_node()
        if new_node != old_node:
            self._node = new_node
            self.pull_data()
            self.node_changed.emit(self.get_node())


    node_changed = QSignal(object)
    node = QProperty(object, fget=get_node, fset=set_node, notify=node_changed)


    def minimumSizeHint(self):
        return QSize(200, 200)


class LayerPropertiesHook(QObject):
    _alive = list()
    _hook = None

    @classmethod
    def is_registered(cls):
        return cls._hook is not None


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
            return True
        return False


    @classmethod
    def drop_dead(cls, qobj):
        cls._alive[:] = (q for q in cls._alive if q != qobj)


    def eventFilter(self, obj, event):
        if isinstance(obj, QDialog):
            dialog = obj
            if dialog.metaObject().className() == "KisDlgLayerProperties":
                flags = dialog.windowFlags()
                if not (flags & Qt.WindowStaysOnTopHint):
                    dialog.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
                # if event.type() == 216:  # done only once in init.
                if event.type() == QEvent.WindowIconChange:  # done only once in init.
                    if self.keep_alive(dialog):
                        # was added to keep_alive (only first time)
                        dialog.destroyed.connect(lambda target=dialog: self.drop_dead(target))
                        layout = dialog.layout()  # QVBoxLayout
                        node = get_active_node()
                        widget = LayerExtraPropertiesWidget(node)
                        layout.insertWidget(1, widget, stretch=100)
                        dialog.accepted.connect(widget.push_data)
        return super(LayerPropertiesHook, self).eventFilter(obj, event)
