"""

Register & Unregister plugin for Krita.

ToDo:
    - can loaded modules be tracked before / after load?

"""

__version__ = "0.0.12"

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

    try:
        import layer_extra_properties
        layer_extra_properties.register()
    except:
        raise RuntimeError("Plugin dependency, layer_extra_properties plugin is needed!")
    """


def register():
    """
    Register Krita plugin.
    Add extensions & dockers to Krita.
    """
    # add_PYTHONPATH()
    # load_plugins()  how to do this correctly ?

    from camera_layer.extension import \
            CameraLayerExtension

    app = Krita.instance()
    extension = CameraLayerExtension(app)
    app.addExtension(extension)


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
