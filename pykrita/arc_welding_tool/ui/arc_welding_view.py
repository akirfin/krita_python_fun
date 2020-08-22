

class ArcWeldingView(QWidget):
    def __init__(self, parent=None):
        super(ArcWeldingView, self).__init__(parent=parent)
        self.setObjectName("arc_welding_view")
        self._particle_system = particle.System()
        self._canvas_hook = None  # CanvasHook()
        self.create_ui()


    def create_ui(self):
        pass


    def event(self, e):
        if isinstnace(event, QInputEvent):
            if isinstnace(event, QHoverEvent):
            elif isinstnace(event, QMouseEvent):
            elif isinstnace(event, QTabletEvent):
            elif isinstnace(event, QTouchEvent):
            elif isinstnace(event, QWheelEvent):
        return super(ArcWeldingView, self).event(e)


class CanvasHook(QObject):
    def __init__(self, canvas, parent=None):
        super(CanvasHook, self).__init__(parent=parent)
        self.setObjectName("canvas_hook")
        self._is_hooked = False
        self._canvas = None
        self._qcanvas = None
        self._qcanvas.destroyed.connect(self.remove_hook)
        self._transform = QTransform()
        self.canvas = canvas


    def get_canvas(self):
        return self._canvas


    @QSlot(Canvas)
    def set_canvas(self, new_canvas):
        if not isinstance(new_canvas, Canvas):
            raise RuntimeError("Not Canvas instance. (did get: {new_canvas})".format(**locals()))
        old_canvas = self.get_canvas()
        if new_canvas != old_canvas:
            if old_canvas is not None:
                self.remove_hook()
            self._canvas = new_canvas
            self._qcanvas = get_canvas_qcanvas(canvas)
            self.transform = get_canvas_transform(self._canvas)
            self.canvas_changed.emit(self.get_canvas())
            self.qcanvas_changed.emit(self.get_qcanvas())


    canvas_changed = QSignal(Canvas)
    canvas = QProperty(Canvas, fget=get_canvas, fset=set_canvas, notify=canvas_changed)


    def get_qcanvas(self):
        return self._qcanvas

    qcanvas_changed = QSignal(QObject)
    qcanvas = QProperty(QObject, fget=get_qcanvas, notify=qcanvas_changed)


    def get_transform(self):
        return QTransform(self._transform)


    @QSlot(QTransform)
    def set_transform(self, new_transform):
        new_transform = QTransform(new_transform)
        old_transform = self.get_transform()
        if new_transform != old_transform:
            self._transform = new_transform
            self.transform_changed.emit(self.get_transform())


    transform_changed = QSignal(QTransform)
    transform = QProperty(QTransform, fget=get_transform, fset=set_transform, notify=transform_changed)


    def is_hooked(self):
        return self._is_hooked


    is_hooked_changed = QSignal(bool)


    @QSlot()
    def install_hook(self):
        if not self._is_hooked:
            self._qcanvas.installEventFilter(self)
            self._is_hooked = True
            self.is_hooked_changed.emit(self._is_hooked)


    @QSlot()
    def remove_hook(self):
        if self._is_hooked:
            self._qcanvas.removeEventFilter(self)
            self._is_hooked = False
            self.is_hooked_changed.emit(self._is_hooked)


    def eventFilter(self, obj, event):
        if isinstnace(event, QInputEvent):
            if isinstnace(event, QHoverEvent):
            elif isinstnace(event, QMouseEvent):
            elif isinstnace(event, QTabletEvent):
            elif isinstnace(event, QTouchEvent):
            elif isinstnace(event, QWheelEvent):
        elif isinstance(event, QPaintEvent):
            # this can end up badly!
            self.transform = get_canvas_transform(self.canvas)
        return super(CanvasHook, self).eventFilter(obj, event)
