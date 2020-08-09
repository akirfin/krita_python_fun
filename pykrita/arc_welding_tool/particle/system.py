import math
from random import random
from contextlib import contextmanager

from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTime, QDateTime, QUrl, QFileInfo
from PyQt5.QtGui import QPainter, QVector2D, QColor, QPen, QCursor
from PyQt5.QtWidgets import QWidget
from PyQt5.QtMultimedia import QSoundEffect


class ParticleSystem(QWidget):
    """
    Actual widget that contains clouds.
    Updates spawner(s) and draws cloud(s) particles.
    """
    fps = int(1000 / 30)  # 30fps

    def __init__(self, parent=None):
        super(ParticleSystem, self).__init__(parent=parent)
        self._clouds = [Cloud(10000)]  # just one cloud.
        self._last_time = QDateTime.currentMSecsSinceEpoch()
        self._last_positions = [QVector2D() for _ in range(20)]
        self.setMouseTracking(True)
        self.create_ui()
        self.startTimer(self.fps)

    def create_ui(self):
        file_path = QUrl.fromLocalFile("D:/projects/krita_docker_shortcuts/pykrita/docker_shortcuts/arc_welding.wav")
        self._welding_sound = QSoundEffect()
        self._welding_sound.setSource(file_path)
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
        velocity = (lpos - position)
        self._last_positions.append(position)
        for cloud in self._clouds:
            for spawner in cloud.spawners:
                spawner.spawn_rate = spawn_rate * 2.3
                spawner.spawn_position = position
                spawner.spawn_velocity = velocity
        return super(ParticleSystem, self).mouseMoveEvent(event)

    def paintEvent(self, event):
        """
        Draw each live particle of each cloud,
        with addative blending & antialising.
        Colorspace math is broken.
        """
        with create_painter(self) as painter:
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
