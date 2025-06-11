from enum import Enum


class RotationType(Enum):
    # All rotation are assumed to along the world coordinate.
    # There are 6 permutation A(3,3) totally.
    RT_WHD = "WHD"  # No rotation.
    RT_HWD = "HWD"  # Rotate 90° along with z-axis.
    RT_HDW = "HDW"  # First rotate 90° along with x-axis, then rotate 90° along with y-axis.
    RT_DHW = "DHW"  # Rotate 90° along with y-axis.
    RT_DWH = "DWH"  # First rotate 90° along with x-axis, then rotate 90° along with z-axis.
    RT_WDH = "WDH"  # Rotate 90° along with x-axis.


# Allow the item to rotate in all directions.
RT_ALL = [RotationType.RT_WHD, RotationType.RT_HWD, RotationType.RT_HDW, RotationType.RT_DHW, RotationType.RT_DWH, RotationType.RT_WDH]
# Only allow for un upright or un updown.
RT_NotUpdown = [RotationType.RT_WHD, RotationType.RT_HWD]


class Axis(Enum):
    WIDTH = 0
    HEIGHT = 1
    DEPTH = 2


Axis_All = [Axis.WIDTH, Axis.HEIGHT, Axis.DEPTH]


class BinType(Enum):
    openTop = "openTop"
    openSide = "openSide"


START_POSITION = [0.0, 0.0, 0.0]

DELTA = 1e-3
