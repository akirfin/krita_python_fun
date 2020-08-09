"""

let's have some fun with python coding 03

Arc Welding! (now we're cooking with GAS)

"""

from krita import Krita, Extension

from .common.utils_py import\
        first

from .common.utils_qt import\
        walk_menu

from . import particle


class ArcWeldingToolExtension(Extension):
    """
    Add tool to Krita.
    (this NOT official way to add new tools.)
    """

    def __init__(self, parent):
        super(ArcWeldingToolExtension, self).__init__(parent)


    def setup(self):
        pass


    def createActions(self, window):
        self._arc_welding_tool_context = particle.System()

        menubar = window.qwindow().menuBar()
        first_tools = first(a for a, _ in walk_menu(menubar) if a.objectName() == "tools")
        
        activate_arc_welding_action = first_tools.menu().addAction("Activate Arc Welding")
        activate_arc_welding_action.setObjectName("activate_arc_welding")
        activate_arc_welding_action.triggered.connect(self.act_activate_arc_welding)


    def act_activate_arc_welding(self, checked=None):
        """
        activate arc welding tool.
        """
        self._arc_welding_tool_context.show()
