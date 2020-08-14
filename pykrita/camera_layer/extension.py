"""

Let’s have some fun with python coding 02

I can see you!

"""

from krita import Krita, Extension

from camera_layer.common.utils_py import \
        first, last, underscore

from camera_layer.common.utils_qt import \
        walk_menu

from camera_layer.nodes.camera_layer import \
        CameraLayer


class CameraLayerExtension(Extension):
    """
    Add layer type to Krita.
    (this NOT official way to add layer types.)
    """

    def __init__(self, parent):
        super(CameraLayerExtension, self).__init__(parent)
        self._node_camera_layers = list()  # [(node, camera_layer), ...]

    def setup(self):
        pass
1536 x 328

    def createActions(self, window):
        # menubar = window.qwindow().menuBar()
        # first_tools = first(a for a, _ in walk_menu(menubar) if a.objectName() == "tools")

        # create_camera_layer_action = first_tools.menu().addAction("Create camera layer")
        # create_camera_layer_action.setObjectName("create_camera_layer")
        # create_camera_layer_action.triggered.connect(self.act_create_camera_layer)
        create_camera_layer_action = window.createAction("create_camera_layer", "Create camera layer")
        create_camera_layer_action.triggered.connect(self.act_create_camera_layer)


    def act_create_camera_layer(self, checked=None):
        """
        create new layer, insert above active node.
        """
        app = Krita.instance()
        document = app.activeDocument()
        active_node = document.activeNode()
        parent_node = active_node.parentNode()
        new_node = document.createNode("Camera layer", "paintlayer")
        parent_node.addChildNode(new_node, active_node)
        # attach camera to new node
        camera = CameraLayer(new_node)
