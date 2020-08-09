
def walk_nodes(nodes, depth_first=True):
    stack = list((n, 0) for n in nodes)
    while stack:
        node, depth = stack.pop(0 if depth_first else -1)
        yield node, depth
        stack[0:0] = ((n, depth +1) for n in node.childNodes())


def find_document_for(node):
    app = Krita.instance()
    for document in app.documents():
        for n, _ in walk_nodes([document.rootNode()]):
            if n == node:
                return document


def set_node_pixel_data(node, qimage, x=None, y=None, width=None, height=None):
    x = 0 if x is None else x
    y = 0 if y is None else y
    width = qimage.width() if width is None else width
    height = qimage.height() if height is None else height
    app = Krita.instance()
    if not qimage.isNull():
        qimage.convertToFormat(QImage.Format_RGBA8888)
        ptr = qimage.constBits()
        ptr.setsize(qimage.byteCount())
        node.setPixelData(bytes(ptr.asarray()), x, y, width, height)
