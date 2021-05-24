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


class ElementalType(Enum):
    NONE = 0
    FIRE = 1
    WATER = 2
    WIND = 3
    LIGHT = 4
    DARK = 5
    ANY = 99


class WeaponType(Enum):
    NONE = 0
    SWD = 1
    KAT = 2
    DAG = 3
    AXE = 4
    LAN = 5
    BOW = 6
    ROD = 7
    CAN = 8
    GUN = 9
