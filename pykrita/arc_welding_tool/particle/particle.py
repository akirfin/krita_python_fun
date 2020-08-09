import math
from random import random
from contextlib import contextmanager

class Particle(object):
    """
    Holds info of one particle.
    """
    __slots__ = ("position", "velocity", "color", "lifespan")
    def __init__(self):
        self.position = QVector2D()
        self.velocity = QVector2D()
        self.color = QColor()
        self.lifespan = 0.0
