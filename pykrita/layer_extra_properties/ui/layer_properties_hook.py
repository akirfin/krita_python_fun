
from collections import OrderedDict as oDict

from krita import Krita, Node

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtCore import \
        QObject, QEvent

from PyQt5.QtGui import \
        QPalette, QColor

from PyQt5.QtWidgets import \
        QWidget, QDialog, QStackedLayout, QScrollArea, \
        QApplication

from layer_extra_properties.common.utils_py import \
        print_console, first, last, UnicodeType, BytesType

from layer_extra_properties.common.utils_kis import \
        get_active_node

from layer_extra_properties.common.utils_qt import \
        dump_qobject_tree

from layer_extra_properties.common.data_serializer import \
        serializer

from layer_extra_properties.layer_meta_data import \
        get_layer_meta_data, set_layer_meta_data

from .layer_extra_properties_container import \
        LayerExtraPropertiesContainer


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


    def _collapse_extra_spacer(self, dialog):
        """
        collapse extra spacer at bottom of dialog.
        """
        WdgLayerProperties = dialog.findChild(QWidget, "WdgLayerProperties")
        layout = WdgLayerProperties.layout()
        for i in range(layout.count()):
            item = layout.itemAt(i)
            spacer = item.spacerItem()
            if spacer is not None:
                spacer.changeSize(0, 0)


    def pull_data(self, node):
        json_data = get_layer_meta_data(node)
        try:
            return serializer.loads(json_data)
        except:
            return oDict()


    @QSlot()
    def push_data(self, node, data):
        json_data = serializer.dumps(data)
        set_layer_meta_data(node, json_data)


    def eventFilter(self, obj, event):
        if event.type() == QEvent.WindowIconChange:
            if isinstance(obj, QDialog):
                dialog = obj
                if dialog.metaObject().className() == "KisDlgLayerProperties":
                    # dump_qobject_tree(dialog)
                    if self.keep_alive(dialog):
                        # was added to keep_alive
                        self._collapse_extra_spacer(dialog)
                        dialog.destroyed.connect(lambda target=dialog: self.drop_dead(target))
                        node = get_active_node()
                        container = LayerExtraPropertiesContainer()
                        container.data = self.pull_data(node)
                        dialog.layout().insertWidget(1, container, stretch=100)
                        dialog.accepted.connect(lambda n=node, c=container: self.push_data(node, container.data))
        return super(LayerPropertiesHook, self).eventFilter(obj, event)
