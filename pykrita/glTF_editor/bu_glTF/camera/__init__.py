from enum import Enum
from .orthographic import Orthographic
from .perspective import Perspective


class CameraType(Enum):
    """
    issue: evil lowercase!
    """
    PERSPECTIVE = "perspective"
    ORTHOGRAPHIC = "orthographic"


class Camera(object):
    """
    """
