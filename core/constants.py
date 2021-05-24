from enum import Enum


class SimEvent(Enum):
    NONE = 0
    DAMAGE = 1
    HEAL = 2


class SimActKind(Enum):
    NONE = 0
    COMBO = 1
    BURST = 2
    SKILL = 3


class PlayerForm(Enum):
    ADV = "c"
    DRG = "d"
