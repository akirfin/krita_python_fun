import math
from random import random
from contextlib import contextmanager

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot as QSlot
from PyQt5.QtCore import pyqtSignal as QSignal
from PyQt5.QtCore import pyqtProperty as QProperty

from PyQt5.QtCore import \
        QTime, QDateTime, QUrl, QFileInfo

from PyQt5.QtGui import \
        QPainter, QVector2D, QColor, QPen, QCursor, QTransform

from PyQt5.QtWidgets import \
        QWidget

from PyQt5.QtMultimedia import \
        QSoundEffect

from arc_welding_tool.common.utils_qt import \
        create_painter, keep_painter

from .cloud import Cloud


class System(QWidget):
    """
    Actual widget that contains clouds.
    Updates spawner(s) and draws cloud(s) particles.
    """

    fps = int(1000 / 30)  # 30fps
    sound_file = QUrl.fromLocalFile("audio:arc_welding.wav")

    def __init__(self, parent=None):
        super(System, self).__init__(parent=parent)
        self._clouds = [Cloud(10000)]  # just one cloud.
        self._last_time = QDateTime.currentMSecsSinceEpoch()
        self._last_positions = [QVector2D() for _ in range(20)]
        self._transform = QTransform()
        self.setMouseTracking(True)
        self.create_ui()
        self.startTimer(self.fps)


    def create_ui(self):
        self._welding_sound = QSoundEffect()
        self._welding_sound.setSource(self.sound_file)
        self._welding_sound.setLoopCount(QSoundEffect.Infinite)
        self._welding_sound.setVolume(0.0)
        self._welding_sound.play()


    def mouseMoveEvent(self, event):
        """
        Works better if TabletEvents are used instead.
        """
        left = event.buttons() & Qt.LeftButton
        mid = event.buttons() & Qt.MidButton
        right = event.buttons() & Qt.RightButton
        any_button = bool(left or mid or right)

        spawn_rate = any_button * 1.0

        self._welding_sound.setVolume(spawn_rate)
        position = QVector2D(event.windowPos())
        lpos = self._last_positions.pop(0)
        velocity = (lpos - position) * 0.2
        self._last_positions.append(position)
        for cloud in self._clouds:
            for spawner in cloud.spawners:
                spawner.spawn_rate = spawn_rate * 2.3
                spawner.spawn_position = position
                spawner.spawn_velocity = velocity
        return super(System, self).mouseMoveEvent(event)


    def paintEvent(self, event):
        """
        Draw each live particle of each cloud,
        with addative blending & antialising.
        Colorspace math is broken.
        """
        with create_painter(self) as painter:
            inv, success = self._transform.inverted()
            painter.setTransform(inv)  # setWorldTransform
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setCompositionMode(QPainter.CompositionMode_Plus)
            pen = QPen()
            pen.setWidth(1.75)
            for cloud in self._clouds:
                for p in cloud.particles[:cloud.alive_count]:
                    pen.setColor(p.color)
                    painter.setPen(pen)
                    p1 = p.position
                    p2 = p1 - p.velocity
                    painter.drawLine(p1.toPointF(), p2.toPointF())


    def timerEvent(self, event):
        """
        Calculate delta time.
        Run cloud simulations.
        Request redraw using QWidget.update()
        """
        now = QDateTime.currentMSecsSinceEpoch()
        delta_time = now - self._last_time
        self._last_time = now
        for cloud in self._clouds:
            cloud.simulate(delta_time)
        self.update()
        return super(System, self).timerEvent(event)


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
