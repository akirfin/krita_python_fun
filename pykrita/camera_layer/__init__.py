"""

Register & Unregister plugin for Krita.

"""

import sys
import os

from krita import \
        Krita, DockWidgetFactory, DockWidgetFactoryBase


def add_PYTHONPATH():
    """
    If you wish to import external python modules, enable this in register.
    Adds PYTHONPATH to sys.path (enable packages from enviroment.)
    Note:
        - paths are inserted before existing paths. (workaround: PyQt5 clash with Qt.py)
        - no duplicate paths are added.
    """
    _memo = set(sys.path)
    for path in reversed(os.environ.get("PYTHONPATH", "").split(os.pathsep)):
        path = path.strip()
        if path and path not in _memo:
            sys.path.insert(1, path)
            _memo.add(path)


def load_plugins():
    """
    Make sure that depending plugins are registered.
    """
    try:
        import layer_meta_data
        layer_meta_data.register()
    except:
        raise RuntimeError("Plugin dependency, layer_meta_data plugin is needed!")


def register():
    """
    Register Krita plugin.
    Add extensions & dockers to Krita.
    """
    # add_PYTHONPATH()
    load_plugins()

    from camera_layer.extension import \
            CameraLayerExtension
    from camera_layer.data_types.camera_layer_data import \
            CameraLayerData
    from camera_layer.ui.camera_layer_widget import \
            CameraLayerWidget
    from layer_meta_data.ui.widget_mapper import \
            widget_mapper

    app = Krita.instance()
    extension = CameraLayerExtension(app)
    app.addExtension(extension)

    widget_mapper.register(
            CameraLayerData,
            CameraLayerWidget)


def unregister():
    """
    Not supported by Krita :.(

    Remove extensions & dockers from Krita.
    Unload plugin modules from python ???
    """
    app = Krita.instance()

    app.removeExtension('extension_id???')
    app.removeDockWidgetFactory('docker_id???')

    del sys.modules["Extension modules..."]


register()
