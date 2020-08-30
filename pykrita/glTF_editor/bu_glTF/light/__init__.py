from enum import Enum

from .ambientInfo import AmbientInfo
from .directionalInfo import DirectionalInfo
from .pointInfo import PointInfo
from .spotInfo import SpotInfo


class LightType(Enum):
    AMBIENT = "AMBIENT"
    DIRECTIONAL = "DIRECTIONAL"
    POINT = "POINT"
    SPOT = "SPOT"


class Light(object):
    """
    name: str = "light_01"

    type: LightType = LightType.DIRECTIONAL
    ambientInfo: Optional[AmbientInfo] = None
    directionalInfo: Optional[DirectionalInfo] = None
    pointInfo: Optional[PointInfo] = None
    spotInfo: Optional[SpotInfo] = None

    intensity: float = 1.0
    color: Color = Color(1.0, 1.0, 1.0)
    """
