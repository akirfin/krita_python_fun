"""

let's have some fun with python coding 03

Arc Welding! (now we're cooking with GAS)

"""

from krita import Krita, Extension

from PyQt5.QtCore import \
        QSettings

from PyQt5.QtWidgets import \
        QMessageBox

from arc_welding_tool.common.utils_py import \
        first, last, underscore

from arc_welding_tool.common.utils_qt import \
        make_menus, create_action

from arc_welding_tool import particle


class ArcWeldingToolExtension(Extension):
    """
    Add tool to Krita.
    (this NOT official way to add new tools.)
    """
    settings_path = "plugin_settings/arc_welding_tool"

    def __init__(self, parent):
        super(ArcWeldingToolExtension, self).__init__(parent)


    def setup(self):
        """
        Called once in Krita startup.
        """
        # hook app closing
        notifier = Krita.instance().notifier()
        notifier.applicationClosing.connect(self.shuttingDown)

        settings = QSettings()
        # some_value = settings.value(self.settings_path +"/some_name", defaultValue=?, type=?)

        # create actions here and share "instance" to other places.
        self._activate_arc_welding_action = create_action(
                name="activate_arc_welding",
                text="Activate Arc Welding",
                triggered=self.act_activate_arc_welding,
                parent=self)  # I own the action!


    def shuttingDown(self):
        """
        Called once in Krita shutting down.
        """
        settings = QSettings()
        # settings.setValue(self.settings_path +"/some_name", some_value)


    def createActions(self, window):
        """
        Called once for each new window opened in Krita.
        """
        self._arc_welding_tool_context = particle.System()

        menu_bar = window.qwindow().menuBar()
        parent_menu = make_menus(
                menu_bar,
                [("tools", "&Tools"),
                    ("experimental_plugins", "&Experimental Plugins")],
                exist_ok=True)

        # add action "instance"
        parent_menu.addAction(
                self._activate_arc_welding_action)


    def act_activate_arc_welding(self, checked=None):
        """
        activate arc welding tool.
        """
        self._arc_welding_tool_context.show()
        # ok = QMessageBox.information(None, "Arc welding tool (sorry)", "Sorry, Welding tool is under construction :(")
