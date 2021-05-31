"""General action parts class"""
from __future__ import annotations
import operator
from enum import Enum
from typing import Callable, Mapping, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from action import Action

from core.constants import PlayerForm
from core.database import DBM
from core.log import LogKind
from mechanic.hit import HitLabel


class PartCmd(Enum):
    NONE = 0
    POSSIBE_NEXT_ACTION = 1
    PLAY_MOTION = 2
    BLEND_MOTION = 3
    STOP_MOTION = 4
    MOVE = 5
    MOVE_TO_TARGET = 6
    ROTATE = 7
    GEN_MARKER = 8
    GEN_BULLET = 9
    HIT_ATTRIBUTE = 10
    EFFECT = 11
    SOUND = 12
    CAMERA = 13
    SEND_SIGNAL = 14
    ACTIVE_CANCEL = 15
    LOITERING = 16
    ROTATE_TO_TARGET = 17
    MOVE_TO_TELEPORT = 18
    EFFECT_TO_TARGET = 19
    EVENT_ACTION = 20
    FALL = 21
    BREAK_FINISH = 22
    FREEZE_POSITION = 23
    MULTI_BULLET = 24
    VISIBLE_OBJECT = 25
    BULLET_CANE_COMBO_005 = 26
    BREAK_CHANCE = 27
    APPEAR_ENEMY = 28
    DROP_BULLET = 29
    CHARACTER_COMMAND = 30
    B00250 = 31
    B00252 = 32
    B00254 = 33
    B00255 = 34
    EFFECT_STRETCH = 35
    EXTRA_CAMERA = 36
    ARRANGE_BULLET = 37
    E02660 = 38
    D00562 = 39
    COLOR = 40
    PARABOLA_BULLET = 41
    ENEMY_GUARD = 42
    E02950 = 43
    EMOTION = 44
    NAVIGATENPC = 45
    DESTROY_MOTION = 46
    BULLET_WITH_MARKER = 47
    HIT_STOP = 48
    MOVE_TIME_CURVE = 49
    MOVE_ORBIT = 50
    WINDY_STREAM = 51
    VOLCANO = 52
    PIVOT_BULLET = 53
    MOVE_INPUT = 54
    ROTATE_INPUT = 55
    THUNDER = 56
    LIGHTNING_PILLAR = 57
    STOCK_BULLET_ROUND = 58
    STOCK_BULLET_FIRE = 59
    OPERATE_PARAMETER = 60
    UPTHRUST = 61
    MULTI_EFFECT = 62
    HEAD_TEXT = 63
    CALL_MINION = 64
    AI_TARGET = 65
    SETTING_HIT = 66
    DARK_TORRENT = 67
    BODY_SCALE = 68
    DESTROY_LOCK = 69
    RECLOSE_BOX = 70
    SALVATION_BUBBLE = 71
    BIND = 72
    SWITCHING_TEXTURE = 73
    FLAME_ARM = 74
    ENEMY_ABILITY = 75
    TANATOS_HIT = 76
    TANATOS_HOURGLASS_SETACTION = 77
    TANATOS_HOURGLASS_DROP = 78
    TANATOS_PLAYER_EFFECT = 79
    INITIALIZE_WEAK = 80
    APPEAR_WEAK = 81
    SEITENTAISEI_HEAL = 82
    EA_MIRAGE = 83
    TANATOS_HIT_PIVOT_BULLET = 84
    MULTI_MARKER_NEED_REGISTER_POS = 85
    TANATOS_GENERAL_PURPOSE = 86
    GM_EVENT = 87
    MULTI_DROP_BULLET_REGISTERED_POS = 88
    LEVEL_HIT = 89
    SERVANT = 90
    ORDER_TO_SUB = 91
    THUNDERBALL = 92
    WATCH_WIND = 93
    BIND_BULLET = 94
    SYNC_CHARA_POSITION = 95
    TIME_STOP = 96
    ORDER_FROM_SUB = 97
    SHAPE_SHIFT = 98
    DEATH_TIMER = 99
    FORMATION_BULLET = 100
    SHADER_PARAM = 101
    FISHING_POWER = 102
    FISHING_DANCE_D = 103
    FISHING_DANCE_C = 104
    REMOVE_BUFF_TRIGGER_BOMB = 105
    FISHING_DANCE_AB = 106
    ORDER_TO_MINION = 107
    RESIST_CLEAR = 108
    HUNTER_HORN = 109
    HUMAN_CANNON = 110
    BUFF_CAPTION = 111
    REACTIVE_LIGHTNING = 112
    LIGHT_SATELLITE = 113
    OPERATE_BG = 114
    ICE_RAY = 115
    OPERATE_SHADER = 116
    APPEAR_MULTIWEAK = 117
    COMMAND_MULTIWEAK = 118
    UNISON = 119
    ROTATE_TIME_CURVE = 120
    SCALE_BLAST = 121
    EA_CHILDPLAY = 122
    DOLL = 123
    PUPPET = 124
    BUFFFIELD_ATTACHMENT = 125
    OPERATE_GMK = 126
    BUTTERFLY_BULLET = 127
    SEIUNHA = 128
    TERMINATE_OTHER = 129
    SETUP_LASTGASP = 130
    SETUP_MIASMA = 131
    MIASMA_POINTUP = 132
    HOLYLIGHT_LEVELUP = 133
    PLAYER_STOP = 134
    DESTORY_ALL_PRAY_OBJECT = 135
    GOZ_TACKLE = 136
    TARGET_EFFECT = 137
    STOCK_BULLET_SHIKIGAMI = 138
    SETUP_2ND_ELEMENTS = 139
    SETUP_ALLOUT_ASSAULT = 140
    IGNORE_ENEMY_PUSH = 141
    ACT_UI = 142
    ENEMY_BOOST = 143
    PARTY_SWITCH = 144
    ROTATE_NODE = 145
    AUTOMATIC_FIRE = 146
    SWITCH_ELEMENT = 147
    ODCOUNTERED_HIT = 148
    EA_GENESIS = 149
    SCAPEGOAT_RITES = 150
    ROSE_TOKEN = 151
    RESERVE_71 = 152
    RESERVE_72 = 153
    RESERVE_73 = 154
    RESERVE_74 = 155
    RESERVE_75 = 156
    RESERVE_76 = 157
    RESERVE_77 = 158
    RESERVE_78 = 159
    RESERVE_79 = 160
    RESERVE_80 = 161
    RESERVE_81 = 162
    RESERVE_82 = 163
    RESERVE_83 = 164
    RESERVE_84 = 165
    RESERVE_85 = 166
    RESERVE_86 = 167
    RESERVE_87 = 168
    RESERVE_88 = 169
    RESERVE_89 = 170
    RESERVE_90 = 171
    RESERVE_91 = 172
    RESERVE_92 = 173
    RESERVE_93 = 174
    RESERVE_94 = 175
    RESERVE_95 = 176
    RESERVE_96 = 177
    RESERVE_97 = 178
    RESERVE_98 = 179
    RESERVE_99 = 180
    RESERVE_100 = 181


class PartCond(Enum):
    NONE = 0
    OwnerBuffCount = 1
    CPValue = 2
    Random = 3
    NearestEnemyDistance = 4
    SingleOrMultiPlay = 5
    SpecificTaggedBulletValid = 6
    ShikigamiLevel = 7
    SettingHitObjTagContains = 8
    ActionContainerHitCount = 9
    ActionCriticalStatus = 10
    HumanOrDragon = 11
    BulletTagContains = 12
    InitialOwner = 13
    RenderPartVisibility = 14
    RESERVE_01 = 15
    RESERVE_02 = 16
    RESERVE_03 = 17
    RESERVE_04 = 18
    RESERVE_05 = 19
    RESERVE_06 = 20
    RESERVE_07 = 21
    RESERVE_08 = 22


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


COND_COMARE = {
    0: operator.eq,
    1: operator.ne,
    2: operator.gt,
    3: operator.ge,
    4: operator.lt,
    5: operator.le,
}


class DisregardPart(Exception):
    pass


class PartCondition:
    """Condition for whether this part will be used"""

    def __init__(self, data: Mapping) -> None:
        self.cond = PartCond(data["_conditionType"])
        self._values = data["_conditionValue"]
        self.until = data["_checkConditionTill"]
        self.sync = bool(data["_syncWithStartParam"])

    def __bool__(self):
        return False


class PartLoop:
    def __init__(self, data: Mapping) -> None:
        self.loopNum = data["loopNum"]
        self.restartFrame = data["restartFrame"]
        self.restartSec = data["restartSec"]


class Part:
    """A command under an action"""

    __slots__ = ["_act", "_seq", "_data", "_timer", "cmd", "seconds", "duration", "_cond", "_loop", "_timer"]

    def __init__(self, act: Action, seq: int, data: Mapping) -> None:
        self._act = act
        self._seq = seq
        self._data = data
        self._timer = None

        self.cmd = PartCmd(data["commandType"])
        self.seconds = data["_seconds"]
        self.duration = data["_duration"]
        try:
            self._cond = PartCondition(data["_conditionData"])
        except KeyError:
            self._cond = False
        if data["_loopData"]["flag"]:
            self._loop = PartLoop(data["_loopData"])
        else:
            self._loop = None
        self._timer = self.schedule(self.seconds, self.proc)

    def log(self, fmt: str, kind: LogKind = LogKind.DEBUG, *args, **kwargs):
        self._act.player.quest.logger(fmt, kind, *args, **kwargs)

    def schedule(self, timeout: float, callback: Optional[Callable] = None, repeat: bool = False):
        return self._act.player.quest.timeline.schedule(timeout, callback=callback, repeat=repeat, name=self.cmd.name)

    def start(self):
        """Start the part timer"""
        self._timer.start()
        # self.log("start {} ({}s)", self.cmd.name, self.seconds)

    def cancel(self) -> None:
        """Turn off the part timer"""
        self._timer.end()
        # self.log("cancel {} ({}s)", self.cmd.name, self.seconds)

    def proc(self) -> bool:
        raise NotImplementedError(self)


class Part_PLAY_MOTION(Part):
    __slots__ = ["motion_state", "_anim_timer"]

    def __init__(self, act: Action, seq: int, data: Mapping) -> None:
        if data["_motionState"]:
            super().__init__(act, seq, data)
            self.motion_state = data["_motionState"]
            if self._act.form == PlayerForm.ADV:
                anim_ref = self._act.player.adventurer.anim_ref
            else:
                anim_ref = self._act.player.dragon.anim_ref
            motion_data = DBM.query_one(
                "SELECT duration FROM MotionData WHERE MotionData.name=? OR (MotionData.state=? AND MotionData.ref=?)",
                (
                    self.motion_state,
                    self.motion_state,
                    anim_ref,
                ),
            )
            if motion_data:
                self.duration += motion_data["duration"] or 1.0
            self._anim_timer = self.schedule(self.duration, self.anim_end)
        else:
            raise DisregardPart()

    def proc(self) -> bool:
        self._anim_timer.start()
        self.log("play anim {} ({:.2f}s)", self.motion_state, self.duration)

    def anim_end(self):
        self._act.end()


class Part_HIT_ATTRIBUTE(Part):
    __slots__ = ["label"]

    def __init__(self, act: Action, seq: int, data: Mapping) -> None:
        if data["_hitLabel"]:
            super().__init__(act, seq, data)
            self.label = HitLabel(data["_hitLabel"], self._act)
        else:
            raise DisregardPart()

    def proc(self) -> bool:
        hitattr = self.label.get(lv=self._act.lv, chlv=self._act.chlv, has=self._act.has)
        self.log("hitattr {}", hitattr.name)


class Part_ACTIVE_CANCEL(Part):
    __slots__ = ["by_action", "by_type", "is_end"]

    def __init__(self, act: Action, seq: int, data: Mapping) -> None:
        super().__init__(act, seq, data)
        self.by_action = data["_actionId"]
        self.by_type = InputType(data["_actionType"])
        self.is_end = bool(data["_motionEnd"])

    def proc(self) -> bool:
        if self.is_end:
            self._act.end()
            self.log("action end")
        else:
            self._act.add_cancel(self.by_type, self.by_action)
            self.log("allow cancel {} by {}", self.by_type, self.by_action)


class Part_SEND_SIGNAL(Part):
    __slots__ = ["signal", "to_action", "input", "until_end", "_signal_timer"]

    def __init__(self, act: Action, seq: int, data: Mapping) -> None:
        super().__init__(act, seq, data)
        self.signal = SignalType(data["_signalType"])
        if data["_actionId"]:
            self.to_action = data["_actionId"]
            self.input = InputType(data["_actionType"])
        self.until_end = bool(data["_motionEnd"])
        self._signal_timer = self.schedule(self.duration, self.end_signal)

    def cancel(self) -> None:
        super().cancel()
        if self._signal_timer is not None:
            self._signal_timer.end()

    def proc(self) -> bool:
        self._act.signals[self.signal].append(self)
        if not self.until_end:
            self._signal_timer.start()
        self.log("signal {}", self.signal)

    def end_signal(self):
        try:
            self._act.signals[self.signal].remove(self)
        except ValueError:
            pass
