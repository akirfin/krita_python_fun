from contextlib import contextmanager

from krita import Krita, Canvas

from Qt.QtGui import \
        QTransform

from Qt.QtWidgets import \
        QWidget, QMdiArea, QMdiSubWindow, QAbstractScrollArea

from animaMattePainter.common.utils_py import \
        first, last

from animaMattePainter.ui.utils_qt import \
        meta_cls_name, dump_tree, dump_transform, walk_qobject_ancestors



##
#
# about 100 lines of code just get one 3x3 matrix... (I don't feel like a winner.)
#

def find_qviews_area(qwindow):
    """
    find QMdiArea that holds KisViews.
    """
    # first try to find any KisView, then backup to ancestor QMdiArea
    for qmdi_win in qwindow.findChildren(QMdiSubWindow):
        qview = qmdi_win.widget()
        if meta_cls_name(qview) == "KisView":
            for anc in walk_qobject_ancestors(qmdi_win):
                if isinstance(anc, QMdiArea):
                    return anc
    # fallback (area is there, but no views exists)
    qmdi_areas = list(qwindow.findChildren(QMdiArea))
    if len(qmdi_areas) == 1:
        return qmdi_areas[0]
    # what now? give up!
    raise RuntimeError("Can not identify QMdiArea used for views!")


def find_qcanvas(qview):
    for qview_child in qview.findChildren(QAbstractScrollArea):
        if meta_cls_name(qview_child) == "KisCanvasController":
            for viewport_child in qview_child.viewport().children():
                meta_name = meta_cls_name(viewport_child)
                if meta_name.startswith("Kis") and ("Canvas" in meta_name):
                    return viewport_child


@contextmanager
def keep_active_view(qwindow):
    """
    Protect current active QMdiSubWindow.
    (restore at context exit)
    """
    qviews_area = find_qviews_area(qwindow)
    old_active = qviews_area.activeSubWindow()
    try:
        yield
    finally:
        try:
            # will fail if is closed / destroyed
            qviews_area.setActiveSubWindow(old_active)
        except:
            pass


def _get_canvas_mapping_cache():
    """
    Update canvas mapping cache.
    To Find matching Krita Canvas -> Qt KisCanvasX,
    change activation at Qt side, then check
    witch View is active using Window.activeView().
    """
    result = list()
    app = Krita.instance()
    for window in app.windows():
        qwindow = window.qwindow()
        with keep_active_view(qwindow):
            qviews_area = find_qviews_area(qwindow)
            for qsub in qviews_area.subWindowList():
                qviews_area.setActiveSubWindow(qsub)
                qview = qsub.widget()
                if meta_cls_name(qview) == "KisView":
                    # this qview is now active, get matching active view.canvas
                    active_canvas = window.activeView().canvas()
                    active_qcanvas = find_qcanvas(qview)
                    result.append((active_canvas, active_qcanvas))
    return result


def get_canvas_qcanvas(canvas, _cache=list()):
    """
    Cached mapping Canvas <-> Qt Canvas
    Cache is updated everytime when matching is NOT found.
    (Asking about imaginary friends is frowned upon!)
    """
    qcanvas = first((qc for c, qc in _cache if c == canvas), None)
    if qcanvas is None:
        _cache[:] = _get_canvas_mapping_cache()
        # try once more, with fresh cache.
        qcanvas = first((qc for c, qc in _cache if c == canvas), None)
    return qcanvas


def get_canvas_translate(canvas):
    """
    Get canvas translate used in KisCanvas.
    """
    def bar_offset(bar):
        min_value, max_value = bar.minimum(), bar.maximum()
        mid_value = (min_value + max_value) / 2.0
        value = bar.value()
        # bar.pageStep() width of slider
        return value - mid_value

    qcanvas = get_canvas_qcanvas(canvas)
    for anc in walk_qobject_ancestors(qcanvas):
        if isinstance(anc, QAbstractScrollArea) and meta_cls_name(anc) == "KisCanvasController":
            x_offset = bar_offset(anc.horizontalScrollBar())
            y_offset = bar_offset(anc.verticalScrollBar())
            return (x_offset, y_offset)


def get_canvas_transform(canvas):
    """
    Why so hard?
    QTransform matrix for canvas.
    """
    view = canvas.view()
    document = view.document()
    res = document.resolution()
    x, y = get_canvas_translate(canvas)
    dpi_zoom = canvas.zoomLevel()
    zoom = (dpi_zoom * 72.0) / res
    rotation = canvas.rotation()
    # and finally...
    transform = QTransform()
    transform.translate(x, y)
    transform.rotate(rotation)
    transform.scale(zoom, zoom)
    return transform