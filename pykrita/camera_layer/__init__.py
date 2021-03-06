"""

Register & Unregister plugin for Krita.

ToDo:
    - can loaded modules be tracked before / after load?

"""

__version__ = "0.0.14"

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


def register():
    """
    Register Krita plugin.
    Add extensions & dockers to Krita.
    """
    # add_PYTHONPATH()
    try:
        # how to do this correctly ?
        import layer_extra_properties
    except:
        raise RuntimeError("Plugin dependency, layer_extra_properties plugin is needed!")

    from .extension import \
            CameraLayerExtension

    app = Krita.instance()
    extensions = (type(e) for e in app.extensions())
    if CameraLayerExtension not in extensions:
        extension = CameraLayerExtension(app)
        app.addExtension(extension)


def unregister():
    """
    Not supported by Krita :.(

    Remove extensions & dockers from Krita.
    Unload plugin modules from python ???
    """
    from .extension import \
            CameraLayerExtension

    app = Krita.instance()
    extensions = {type(e): e for e in app.extensions()}
    extension = extensions.get(CameraLayerExtension)
    if extension:
        app.removeExtension(extension)

    del sys.modules["Extension modules..."]


register()
