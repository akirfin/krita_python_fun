"""

Arc Welding! (now we're cooking with GAS)

ToDo:
    - view/canvas trapping
    - using canvas_transform to solve transform.

"""

from krita import Krita, Extension

from PyQt5.QtCore import \
        QSettings, QTimer, QRect

from arc_welding_tool.common.utils_py import \
        first, last, underscore

from arc_welding_tool.common.utils_qt import \
        find_menu, create_menu, create_action

from layer_extra_properties.common.utils_kis import \
        write_extension_action_file, read_setting, write_setting

from arc_welding_tool.canvas_transform import \
        get_canvas_transform, get_canvas_qcanvas

from arc_welding_tool import \
        particle


class ArcWeldingToolExtension(Extension):
    """
    Add tool to Krita.
    (this NOT official way to add new tools.)
    """

    def __init__(self, parent):
        super(ArcWeldingToolExtension, self).__init__(parent)
        self.objectName("arc_welding_tool_extension")


    def setup(self):
        """
        Called once in Krita startup.
        """
        # hook app closing
        notifier = Krita.instance().notifier()
        notifier.applicationClosing.connect(self.shuttingDown)

        extension_name = self.objectName()
        # value = read_setting(extension_name, "setting_name", default=None)

        # create actions here and share "instance" to other places.
        self._activate_arc_welding_action = create_action(
                name="activate_arc_welding",
                text=i18n("Activate Arc Welding"),
                triggered=self.activate_arc_welding,
                parent=self)  # I own the action!

        # when is .action file applied?
        # write_extension_action_file(self)


    def shuttingDown(self):
        """
        Called once in Krita shutting down.
        """
        extension_name = self.objectName()
        # write_setting(extension_name, "setting_name", value)


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
        # copy active layer to QImage
        # show particle system + QImage in new window resize to QImage
        # hook canvas transform change signals
        # hook canvas mouse / tablet events (transform to new window)

        canvas = app.activeWindow().activeView().canvas()
        for welding_view in self._welding_views:
            if welding_view.canvas == canvas
                welding_view.install_hook()
                welding_view.show()
                welding_view.raise_()
                break # already exist!
        else:
            welding_view = WeldingView(canvas)
            welding_view.install_hook()
            welding_view.show()
            welding_view.raise_()
            self._welding_views.append(welding_view)


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
