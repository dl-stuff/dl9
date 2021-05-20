"""Action parts that deal with triggering other actions"""
from enum import Enum
from typing import Mapping
from action.parts import Part, PartCmd
from core.database import DBData


class InputType(Enum):
    NONE = 0
    BurstAttack = 1
    Avoid = 2
    AvoidFront = 3
    AvoidBack = 4


class SignalType(Enum):
    Input = 0
    SuperArmor = 1
    Invincible = 2
    AttachWeaponLeft = 3
    AttachWeaponRight = 4
    NonUse01 = 5
    NonUse02 = 6
    PutUpEffect = 7
    Show = 8
    Hide = 9
    NoReaction = 10
    SuperArmorLv1 = 11
    SuperArmorLv2 = 12
    SuperArmorLv3 = 13
    Omit01 = 14
    AdditionalInput = 15
    InvincibleLv1 = 16
    InvincibleLv2 = 17
    InvincibleLv3 = 18
    SpecialDead = 19
    NoTarget = 20
    SuperArmorLv4 = 21
    DisableCheckOutside = 22
    DisableExternalVelocity = 23
    ShowWeapon = 24
    HideWeapon = 25
    DamageCounter = 26
    CancelInvincible = 27
    ChangePartsMesh = 28
    EnableAction = 29
    RecordHitTarget = 30
    GuardCounter = 31
    GuardReactionInCharge = 32
    HideStockBullet = 33
    Stop1 = 34
    HitCount = 35
    ActionCriticalStatus = 36
    RESERVE_03 = 37
    RESERVE_04 = 38
    RESERVE_05 = 39
    RESERVE_06 = 40
    RESERVE_07 = 41
    RESERVE_08 = 42
    RESERVE_09 = 43
    RESERVE_10 = 44


class Part_ACTIVE_CANCEL(Part):
    def __init__(self, data: DBData) -> None:
        super().__init__(data)
        self.by_action = data["_actionId"]
        self.cancel = InputType(data["_actionType"])
        self.end = bool(data["_motionEnd"])


class Part_SEND_SIGNAL(Part):
    def __init__(self, data: DBData) -> None:
        super().__init__(data)
        self.signal = SignalType(data["_signalType"])
        if data["_actionId"]:
            self.to_action = data["_actionId"]
            self.input = InputType(data["_actionType"])
        self.until_end = bool(data["_motionEnd"])
