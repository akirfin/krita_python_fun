"""

Small common scripts for Krita

"""
import os
import json
from contextlib import contextmanager

from krita import Krita, View

from PyQt5.QtCore import QStandardPaths
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QMdiArea

from .utils_py import \
    first, last, Undefined


def walk_nodes(nodes, depth_first=True):
    """
    Traverse all child nodes of given nodes.
    """
    stack = list((n, 0) for n in nodes)
    while stack:
        node, depth = stack.pop(0 if depth_first else -1)
        yield node, depth
        stack[0:0] = ((n, depth +1) for n in node.childNodes())


def walk_node_ancestors(node):
    """
    Traverse all ancestor nodes of given node.
    """
    cursor = node.parent()
    while cursor is not None:
        yield cursor
        cursor = cursor.parent()


def find_document_for(node):
    """
    Missing method:
        document = krita.Node.document(self)
    """
    app = Krita.instance()
    for document in app.documents():
        for n, _ in walk_nodes([document.rootNode()]):
            if n == node:
                return document


def get_active_node():
    """
    common shorthand.
    """
    app = Krita.instance()
    document = app.activeDocument()
    if document is not None:
        return document.activeNode()


def set_active_document(document):
    """
    Fixed Krita.setActiveDocument(document)
    """
    app = Krita.instance()
    for window in app.windows():
        for v_i, view in enumerate(window.views()):
            if view.document() == document:
                qwindow = window.qwindow()
                central = qwindow.centralWidget()
                area = central.findChild(QMdiArea)
                sub = area.subWindowList()[v_i]
                area.setActiveSubWindow(sub)
                return True


@contextmanager
def keep_batch_mode(new_batch_mode=None):
    app = Krita.instance()
    old_batch_mode = app.batchMode()
    try:
        if new_batch_mode is not None:
            app.setBatchMode(new_batch_mode)
        yield app.batchMode()
    finally:
        if old_batch_mode is not None:
            app.setBatchMode(old_batch_mode)


@contextmanager
def keep_active_document(new_document=None):
    app = Krita.instance()
    old_document = app.activeDocument()
    try:
        if new_document is not None:
            set_active_document(new_document)
        yield app.activeDocument()
    finally:
        if old_document is not None:
            set_active_document(old_document)


@contextmanager
def keep_active_node(new_node=None):
    app = Krita.instance()
    new_document = app.activeDocument() if new_node is None else find_document_for(new_node)
    with keep_active_document(new_document):
        old_node = get_active_node()
        try:
            if new_document is not None:
                new_document.setActiveNode(new_node)
            yield get_active_node()
        finally:
            document = find_document_for(old_node)
            if document is not None:
                document.setActiveNode(old_node)


def create_document_from_qimage(
                    qimage,
                    name=None,
                    add_view=None,
                    width=None,
                    height=None,
                    color_mode=None,
                    color_depth=None,
                    color_profile=None,
                    dpi=None):
    """
    Create new document from given QImage.

    Document properties are inherited from image, use arguments to override.
    Document name is taken from QImage.objectName()  # NOT great.
    """
    if qimage.isNull():
        return  # None document for Null image!
    if name is None:
        raise RuntimeError("Name must be given.")
    width = qimage.width() if width is None else width
    height = qimage.height() if height is None else height
    # ToDo: solve new documents colorMode & colorDepth from QImage.pixelFormat()
    color_mode = "RGBA"  # qimage.color_mode() if color_mode is None else color_mode
    color_depth = "U8"  # qimage.color_depth() if color_depth is None else color_depth
    color_profile = ""  # qimage.color_profile() if color_profile is None else color_profile
    dpi = 72.0  # qimage.dpiX() if dpi is None else dpi
    app = Krita.instance()

    document = app.createDocument(
            width,
            height,
            name,
            color_mode,
            color_depth,
            color_profile,
            dpi)

    first_node = first(document.topLevelNodes())
    push_qimage_data_to_node(qimage, first_node)
    first_node.setOpacity(255)
    document.refreshProjection()

    if isinstance(add_view, View):
        # use given view
        view.setDocument(document)
    elif add_view:
        # not a view, but True, create new view
        app.activeWindow().addView(document)
    return document


def create_node_from_qimage(document, qimage, name=None):
    """
    Add new node to document and pull its pixels from QImage.
    Node name is taken from QImage.objectName()  # NOT great.
    """
    if qimage.isNull():
        return  # None Node for Null image!
    if name is None:
        raise RuntimeError("Name must be given.")
    node = document.createNode(name, paintlayer)
    push_qimage_data_to_node(qimage, node)
    node.setOpacity(255)
    document.refreshProjection()
    return node


def push_qimage_data_to_node(qimage, node, x=None, y=None, width=None, height=None):
    """
    Try to convert QImage data to Node data.
    """
    node_name = node.name()
    node_type = node.type()
    if node.type() != "paintlayer":
        raise RuntimeError("Node type must be paintlayer. (did get: name={node_name}, type={node_type})".format(**locals()))
    x = 0 if x is None else x
    y = 0 if y is None else y
    width = qimage.width() if width is None else width
    height = qimage.height() if height is None else height
    # color_mode = qimage.color_mode()
    # color_depth = qimage.color_depth()
    # color_profile = qimage.color_profile()
    dpi = qimage.logicalDpiX()

    app = Krita.instance()
    if not qimage.isNull():
        # ToDo: convert qimage to match document.colorMode & colorDepth
        qimage.convertToFormat(QImage.Format_RGBA8888)
        ptr = qimage.constBits()
        ptr.setsize(qimage.byteCount())
        node.setPixelData(bytes(ptr.asarray()), x, y, width, height)


def read_setting(extension_name, name, default=Undefined, type_hint=None):
    undefined_str = "<--Undefined 445632456-->"
    app = Krita.instance()
    if (type_hint is None) and (default is not Undefined):
        type_hint = type(default)
    data_str = app.readSetting(extension_name, name, undefined_str)
    if data_str == undefined_str:
        if default is Undefined:
            raise ValueError((
                    "Setting not found, and no default given."
                    "(did get: extension_name={extension_name!r}, name={name!r})").format(**locals()))
        else:
            return default
    else:
        return data_str if type_hint is None else type_hint(data_str)


def read_setting(extension_name, name, default=Undefined):
    undefined_str = '"<--undefined 435235-->"'
    app = Krita.instance()
    json_str = app.readSetting(extension_name, name, undefined_str)
    if json_str == undefined_str:
        if default is Undefined:
            raise ValueError((
                    "Setting not found, and no default given."
                    "(did get: extension_name={extension_name!r}, name={name!r})").format(**locals()))
        else:
            return default
    else:
        return json.loads(json_str)


def write_setting(extension_name, name, value):
    app = Krita.instance()
    app.writeSetting(extension_name, name, json.dumps(value))


def krita_resource_dir():
    return QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)


def write_extension_action_file(extension, overwrite=False):
    actions_collection_template = """
            <?xml version="1.0" encoding="UTF-8"?>
            <ActionCollection version="2" name="Scripts">
                <Actions category="{extension_name}">
                    {actions}
                </Actions>
            </ActionCollection>"""

    action_template = """
            <text>{action_text}</text>
            <Action name="{action_name}">
                <icon>{action_icon}</icon>
                <text>{action_text}</text>
                <whatsThis>{action_whats_this}</whatsThis>
                <toolTip>{action_tool_tip}</toolTip>
                <iconText>{action_icon_text}</iconText>
                <activationFlags>10000</activationFlags>
                <activationConditions>0</activationConditions>
                <shortcut>{action_shortcut}</shortcut>
                <isCheckable>{action_is_checkable}</isCheckable>
                <statusTip>{action_status_tip}</statusTip>
            </Action>"""

    extension_name = extension.objectName()

    action_file_name = "{extension_name}.action".format(**locals())
    action_file_path = os.path.join(krita_resource_dir(), "actions", action_file_name)

    file_missing = not os.path.isfile(action_file_path)
    if file_missing or overwrite:
        # write file
        actions = list()
        for action in extension.findChildren(QAction):
            # iterate MY actions.
            action_name = action.objectName()
            action_icon = action.icon().name()  # ToDo: check this?
            action_text = action.text()
            action_icon_text = action.iconText()
            action_whats_this = action.whatsThis()
            action_tool_tip = action.toolTip()
            action_status_tip = action.statusTip()
            action_is_checkable = action.isCheckable()
            action_shortcut = action.shortcut().toString()
            actions.append(action_template.format(**locals()))

        actions = ''.join(actions)
        xml_data = actions_collection_template.format(**locals())
        with open(action_file_path, "w") as f:
            f.write(xml_data)
    else:
        pass # nothing to do
