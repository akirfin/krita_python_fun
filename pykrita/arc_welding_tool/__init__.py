"""

Register & Unregister plugin for Krita.

"""

__version__ = "0.0.0"

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

    from arc_welding_tool.extension import ArcWeldingToolExtension

    app = Krita.instance()
    app.addExtension(ArcWeldingToolExtension(app))


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
