"""

Arc Welding! (now we're cooking with GAS)

ToDo:
    - view/canvas trapping
    - using canvas_transform to solve transform.
    - solve settings
    - solve parent menu / sub menu

"""

from krita import Krita, Extension

from PyQt5.QtCore import \
        QSettings, QTimer, QRect

from arc_welding_tool.common.utils_py import \
        first, last, underscore

from arc_welding_tool.common.utils_qt import \
        find_menu, create_menu, create_action

from arc_welding_tool.canvas_transform import \
        get_canvas_transform, get_canvas_qcanvas

from arc_welding_tool import \
        particle


class ArcWeldingToolExtension(Extension):
    """
    Add tool to Krita.
    (this NOT official way to add new tools.)
    """
    settings_path = "plugin_settings/arc_welding_tool"
    # some_setting = settings_path +"/some"

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
        # config_path = QStandardPaths.writableLocation(QStandardPaths.GenericConfigLocation)
        # self.settings = QSettings(config_path + "/krita/arc_welding_tool", QSettings.IniFormat)
        # self._some_value = settings.value(self.some_setting, defaultValue=, type=)

        # create actions here and share "instance" to other places.
        self._activate_arc_welding_action = create_action(
                name="activate_arc_welding",
                text=i18n("Activate Arc Welding"),
                triggered=self.activate_arc_welding,
                parent=self)  # I own the action!


    def shuttingDown(self):
        """
        Called once in Krita shutting down.
        """
        settings = QSettings()
        # settings.setValue(self.some_setting, self._some_value)


    def createActions(self, window):
        """
        Called once for each new window opened in Krita.
        """
        menu_bar = window.qwindow().menuBar()

        tools_menu = find_menu(menu_bar, "tools")
        experimental_menu = find_menu(tools_menu, "experimental")
        if experimental_menu is None:
            experimental_menu = create_menu("experimental", i18n("Experimental"), parent=tools_menu)
            tools_menu.addAction(experimental_menu.menuAction())

        # add action "instance"
        experimental_menu.addAction(self._activate_arc_welding_action)


    def activate_arc_welding(self, checked=None):
        """
        activate arc welding tool.
        """
        app = Krita.instance()
        p_system = self._arc_welding_tool_context
        active_canvas = None
        active_view = app.activeWindow().activeView()
        if active_view:
            active_canvas = active_view.canvas()
        if active_canvas:
            qcanvas = get_canvas_qcanvas(active_canvas)

        doc = app.activeDocument()
        p_system.resize(doc.width(), doc.height())
        p_system.transform = get_canvas_transform(active_canvas)
        p_system.show()
