"""
Place holder.
"""

import math
from random import random
from contextlib import contextmanager

from PyQt5.QtGui import QPainter, QVector2D, QColor


class Force(object):
    """
    forces that effect particles.
    - Gravity
    - Wind
    - Age
    - Collision
    - Turbulence
    ...
    """
