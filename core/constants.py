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


GLOBAL = "GLOBAL"


class ForceTimelineEnd(Exception):
    pass


class EventOrder(Enum):
    BEFORE = 0
    DURING = 1
    AFTER = 2


class Stat(Enum):
    NONE = 0
    Hp = 1
    Atk = 2
    Def = 3
    Spr = 4
    Dpr = 5
    Dummy1 = 6
    ChargeTime = 7
    DragonTime = 8
    DamageCut = 9
    AttackSpeed = 10
    BurstSpeed = 11
    ChargeSpeed = 12
    ConsumeDpRate = 13
    FinalDragonTimeRate = 14
    Utpr = 15
    DamageCutB = 16


class Bracket(Enum):
    Misc = 0
    ActDmg = 1
    CritRate = 2
    CritDmg = 3
    Killer = 4
    Punisher = 5


class MomentType(Enum):
    NONE = 0
    QUEST_START = 1
    HP = 2
    SP = 3
    CP = 4
    DP = 5
    HIT = 6
    HEALED = 7
    DAMAGED = 8
    DODGED = 9
    CRITICAL = 10
    TENSION = 11
    SLAYER = 12
    REBORN = 13
    DISPEL = 14
    AFFLICTION_CAUSE = 101
    AFFLICTION_RECEIVED = 102
    BUFF_START = 201
    BUFF_END = 202
    DEBUFF_START = 211
    DEBUFF_END = 212
    DRAGONSHIFT_START = 301
    DRAGONSHIFT_END = 302
    BURST_START = 501
    BURST_END = 502


class AfflictType(Enum):
    NONE = 0
    POISON = 1
    BURN = 2
    FREEZE = 3
    PARALYSIS = 4
    DARKNESS = 5
    SWOON = 6
    CURSE = 7
    REBIRTH = 8
    SLOWMOVE = 9
    SLEEP = 10
    FROSTBITE = 11
    FLASHHEAT = 12
    CRASHWIND = 13
    DARKABS = 14
    DESTROYFIRE = 15
    ALL = 99
