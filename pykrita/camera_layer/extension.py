"""

Let’s have some fun with python coding 02

I can see you!

"""

from krita import Krita, Extension

from .camera_layer import CameraLayer


class CameraLayerExtension(Extension):
    """
    Add layer type to Krita.
    (this NOT official way to add layer types.)
    """

    def __init__(self, parent):
        super(CameraLayerExtension, self).__init__(parent)
        self._camera_layers = list()


    def setup(self):
        pass


    def createActions(self, window):
        menubar = window.qwindow().menuBar()
        first_tools = first(a for a, _ in walk_menu(menubar) if a.objectName() == "tools")

        create_camera_layer_action = first_tools.menu().addAction("Create camera layer")
        create_camera_layer_action.setObjectName("create_camera_layer")
        create_camera_layer_action.triggered.connect(self.act_create_camera_layer)


    def act_create_camera_layer(self, checked=None):
        """
        create new layer, insert above active node.
        """
        document = app.activeDocument()
        node = document.activeNode()
        new_node = document.createNode()
        # attach camera to new node
        camera_layer = CameraLayer(new_node)
        # now where to put this camera_layer ?
        self._camera_layers.append(camera_layer)
