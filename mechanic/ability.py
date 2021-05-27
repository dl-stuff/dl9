"""player abilities"""
from __future__ import annotations
from core.constants import ElementalType, PlayerForm, SimActKind, MomentType
from mechanic.modifier import Modifier
from enum import Enum

from core.database import FromDB

from typing import Callable, NamedTuple, Optional, Sequence, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from entity.player import Player


class AbilityType(Enum):
    NONE = 0
    StatusUp = 1
    ResistAbs = 2
    ActAddAbs = 3
    ResistTribe = 4
    ActKillerTribe = 5
    ActDamageUp = 6
    ActCriticalUp = 7
    ActRecoveryUp = 8
    ActBreakUp = 9
    ResistTrap = 10
    AddRecoverySp = 11
    AddRecoveryDp = 12
    RecoveryHpOnHitCount = 13
    ChangeState = 14
    ResistInstantDeath = 15
    DebuffGrantUp = 16
    SpCharge = 17
    BuffExtension = 18
    DebuffExtension = 19
    AbnormalKiller = 20
    UserExpUp = 21
    CharaExpUp = 22
    CoinUp = 23
    ManaUp = 24
    ActionGrant = 25
    CriticalDamageUp = 26
    DpCharge = 27
    ResistElement = 28
    ResistUnique = 29
    UniqueKiller = 30
    Dummy01 = 31
    Dummy02 = 32
    Dummy03 = 33
    Dummy04 = 34
    ModeGaugeSuppression = 35
    DragonDamageUp = 36
    EnemyAbilityKiller = 37
    HitAttribute = 38
    PassiveGrant = 39
    ActiveGaugeStatusUp = 40
    Dummy05 = 41
    HitAttributeShift = 42
    ReferenceOther = 43
    EnhancedSkill = 44
    EnhancedBurstAttack = 45
    DragonTimeForParty = 46
    AbnoramlExtension = 47
    DragonTimeSpeedRate = 48
    DpChargeMyParty = 49
    DontAct = 50
    RandomBuff = 51
    CriticalUpDependsOnBuffTypeCount = 52
    InvalidDragonAbility = 53
    ActDamageUpDependsOnHitCount = 54
    ChainTimeExtension = 55
    UniqueTransform = 56
    EnhancedElementDamage = 57
    UtpCharge = 58
    DebuffTimeExtensionForSpecificDebuffs = 59
    RemoveAllStockBullets = 60
    ChangeMode = 61
    RandomBuffNoTDuplicate_Param1Times = 62
    ModifyBuffDebuffDurationTime = 63
    CpCoef = 64
    UniqueAvoid = 65
    RebornHpRateUp = 66
    AttackBaseOnHPUpRate = 67
    ChangeStateHostile = 68
    CpContinuationDown = 69
    AddCpRate = 70
    RunOptionAction = 71
    SecondElements = 72
    KickAuraEffectTritter = 73
    ConsumeSpToRecoverHp = 74
    CrestGroupScoreUp = 75
    ModifyBuffDebuffDurationTimeByRecoveryHp = 76
    CrisisRate = 77
    ActDamageDown = 78
    AutoAvoidProbability = 79
    LimitCriticalAddRate = 80
    AddReborn = 81


class AbilityCondition(Enum):
    NONE = 0
    HP_MORE = 1
    HP_LESS = 2
    BUFF_SKILL1 = 3
    BUFF_SKILL2 = 4
    DRAGON_MODE = 5
    BREAKDOWN = 6
    GET_BUFF_ATK = 7
    GET_BUFF_DEF = 8
    TOTAL_HITCOUNT_MORE = 9
    TOTAL_HITCOUNT_LESS = 10
    KILL_ENEMY = 11
    TRANSFORM_DRAGON = 12
    HP_MORE_MOMENT = 13
    HP_LESS_MOMENT = 14
    QUEST_START = 15
    OVERDRIVE = 16
    ABNORMAL_STATUS = 17
    TENSION_MAX = 18
    TENSION_MAX_MOMENT = 19
    DEBUFF_SLIP_HP = 20
    HITCOUNT_MOMENT = 21
    GET_HEAL_SKILL = 22
    SP1_OVER = 23
    SP1_UNDER = 24
    SP1_LESS = 25
    SP2_OVER = 26
    SP2_UNDER = 27
    SP2_LESS = 28
    CAUSE_ABNORMAL_STATUS = 29
    DAMAGED_ABNORMAL_STATUS = 30
    DRAGONSHIFT_MOMENT = 31
    PARTY_ALIVE_NUM_OVER = 32
    PARTY_ALIVE_NUM_UNDER = 33
    TENSION_LV = 34
    TENSION_LV_MOMENT = 35
    GET_BUFF_TENSION = 36
    HP_NOREACH = 37
    HP_NOREACH_MOMENT = 38
    SKILLCONNECT_SKILL1_MOMENT = 39
    SKILLCONNECT_SKILL2_MOMENT = 40
    DRAGON_MODE2 = 41
    CAUSE_DEBUFF_ATK = 42
    CAUSE_DEBUFF_DEF = 43
    CHANGE_BUFF_TYPE_COUNT = 44
    CAUSE_CRITICAL = 45
    TAKE_DAMAGE_REACTION = 46
    NO_DAMAGE_REACTION_TIME = 47
    BUFFED_SPECIFIC_ID = 48
    DAMAGED = 49
    DEBUFF = 50
    RELEASE_DRAGONSHIFT = 51
    UNIQUE_TRANS_MODE = 52
    DAMAGED_MYSELF = 53
    SP1_MORE_MOMENT = 54
    SP1_UNDER_MOMENT = 55
    SP2_MORE_MOMENT = 56
    SP2_UNDER_MOMENT = 57
    HP_MORE_NOT_EQ_MOMENT = 58
    HP_LESS_NOT_EQ_MOMENT = 59
    HP_MORE_NO_SUPPORT_CHARA = 60
    HP_NOREACH_NO_SUPPORT_CHARA = 61
    CP1_CONDITION = 62
    CP2_CONDITION = 63
    REQUIRED_BUFF_AND_SP1_MORE = 64
    REQUIRED_BUFF_AND_SP2_MORE = 65
    ENEMY_HP_MORE = 66
    ENEMY_HP_LESS = 67
    ALWAYS_REACTION_TIME = 68
    ON_ABNORMAL_STATUS_RESISTED = 69
    BUFF_DISAPPEARED = 70
    BUFFED_SPECIFIC_ID_COUNT = 71
    CHARGE_LOOP_REACTION_TIME = 72
    BUTTERFLYBULLET_NUM_OVER = 73
    AVOID = 74
    CAUSE_DEBUFF_SLIP_HP = 75
    CP1_OVER = 76
    CP2_OVER = 77
    CP1_UNDER = 78
    CP2_UNDER = 79
    BUFF_COUNT_MORE_THAN = 80
    BUFF_CONSUMED = 81
    HP_BETWEEN = 82
    DAMAGED_WITHOUT_MYSELF = 83
    BURST_ATTACK_REGULAR_INTERVAL = 84
    BURST_ATTACK_FINISHED = 85
    REBORN_COUNT_LESS_MOMENT = 86
    DISPEL_SUCCEEDED = 87
    ON_BUFF_FIELD = 88
    ENTER_EXIT_BUFF_FIELD = 89
    GET_DP = 90
    GET_BUFF_FOR_PD_LINK = 91
    GET_HEAL = 92
    CHARGE_TIME_MORE_MOMENT = 93
    EVERY_TIME_HIT_OCCURS = 94
    HITCOUNT_MOMENT_TIMESRATE = 95
    JUST_AVOID = 96
    GET_BRITEM = 97
    DUP_BUFF_ALWAYS_TIMESRATE = 98
    BUFFED_SPECIFIC_ID_COUNT_MORE_ALWAYS_CHECK = 99
    GET_BUFF_FROM_SKILL = 100
    HP_RECOVERED_BETWEEN = 101
    RELEASE_DIVINEDRAGONSHIFT = 102
    HAS_AURA_TYPE = 103
    SELF_AURA_LEVEL_MORE = 104
    PARTY_AURA_LEVEL_MORE = 105
    DRAGONSHIFT = 106
    DRAGON_MODE_STRICTLY = 107


CONDITON_TO_MOMENT = {
    AbilityCondition.GET_BUFF_DEF: MomentType.BUFF_START,
    AbilityCondition.KILL_ENEMY: MomentType.SLAYER,
    AbilityCondition.TRANSFORM_DRAGON: MomentType.DRAGONSHIFT_START,
    AbilityCondition.HP_MORE_MOMENT: MomentType.HP,
    AbilityCondition.HP_LESS_MOMENT: MomentType.HP,
    AbilityCondition.QUEST_START: MomentType.QUEST_START,
    AbilityCondition.TENSION_MAX_MOMENT: MomentType.TENSION,
    AbilityCondition.HITCOUNT_MOMENT: MomentType.HIT,
    AbilityCondition.TENSION_LV_MOMENT: MomentType.TENSION,
    AbilityCondition.CAUSE_ABNORMAL_STATUS: MomentType.AFFLICTION_CAUSE,
    AbilityCondition.DAMAGED_ABNORMAL_STATUS: MomentType.AFFLICTION_RECEIVED,
    AbilityCondition.DRAGONSHIFT_MOMENT: MomentType.DRAGONSHIFT_START,
    AbilityCondition.GET_BUFF_TENSION: MomentType.TENSION,
    AbilityCondition.HP_NOREACH_MOMENT: MomentType.HP,
    AbilityCondition.SKILLCONNECT_SKILL1_MOMENT: MomentType.SP,
    AbilityCondition.SKILLCONNECT_SKILL2_MOMENT: MomentType.SP,
    AbilityCondition.CAUSE_DEBUFF_ATK: MomentType.DEBUFF_START,
    AbilityCondition.CAUSE_DEBUFF_DEF: MomentType.DEBUFF_START,
    AbilityCondition.CAUSE_CRITICAL: MomentType.CRITICAL,
    AbilityCondition.TAKE_DAMAGE_REACTION: MomentType.DAMAGED,
    AbilityCondition.DAMAGED: MomentType.DAMAGED,
    AbilityCondition.RELEASE_DRAGONSHIFT: MomentType.DRAGONSHIFT_END,
    AbilityCondition.DAMAGED_MYSELF: MomentType.DAMAGED,
    AbilityCondition.SP1_MORE_MOMENT: MomentType.SP,
    AbilityCondition.SP1_UNDER_MOMENT: MomentType.SP,
    AbilityCondition.SP2_MORE_MOMENT: MomentType.SP,
    AbilityCondition.SP2_UNDER_MOMENT: MomentType.SP,
    AbilityCondition.HP_MORE_NOT_EQ_MOMENT: MomentType.HP,
    AbilityCondition.HP_LESS_NOT_EQ_MOMENT: MomentType.HP,
    AbilityCondition.HP_MORE_NO_SUPPORT_CHARA: MomentType.HP,
    AbilityCondition.HP_NOREACH_NO_SUPPORT_CHARA: MomentType.HP,
    AbilityCondition.BUFF_DISAPPEARED: MomentType.BUFF_END,
    AbilityCondition.AVOID: MomentType.DODGED,
    AbilityCondition.BUFF_CONSUMED: MomentType.BUFF_END,
    AbilityCondition.DAMAGED_WITHOUT_MYSELF: MomentType.DAMAGED,
    AbilityCondition.BURST_ATTACK_REGULAR_INTERVAL: MomentType.BURST_START,
    AbilityCondition.BURST_ATTACK_FINISHED: MomentType.BURST_END,
    AbilityCondition.REBORN_COUNT_LESS_MOMENT: MomentType.REBORN,
    AbilityCondition.DISPEL_SUCCEEDED: MomentType.DISPEL,
    AbilityCondition.GET_DP: MomentType.DP,
    AbilityCondition.GET_HEAL: MomentType.HEALED,
    AbilityCondition.CHARGE_TIME_MORE_MOMENT: MomentType.BURST_START,
    AbilityCondition.HITCOUNT_MOMENT_TIMESRATE: MomentType.HIT,
    AbilityCondition.JUST_AVOID: MomentType.DODGED,
    AbilityCondition.GET_BUFF_FROM_SKILL: MomentType.BURST_START,
    AbilityCondition.DRAGONSHIFT: MomentType.DRAGONSHIFT_START,
}


class AbilityTarget(Enum):
    NONE = 0
    COMBO = 1
    BURST_ATTACK = 2
    SKILL_1 = 3
    SKILL_2 = 4
    SKILL_3 = 5
    SKILL_ALL = 6
    HUMAN_SKILL_1 = 7
    HUMAN_SKILL_2 = 8
    DRAGON_SKILL_1 = 9
    SKILL_4 = 10
    HUMAN_SKILL_3 = 11
    HUMAN_SKILL_4 = 12


TARGET_TO_ACTKIND = {
    AbilityTarget.COMBO: SimActKind.COMBO,
    AbilityTarget.BURST_ATTACK: SimActKind.BURST,
    AbilityTarget.SKILL_ALL: SimActKind.SKILL,
    AbilityTarget.SKILL_1: SimActKind.SKILL,
    AbilityTarget.SKILL_2: SimActKind.SKILL,
    AbilityTarget.SKILL_3: SimActKind.SKILL,
    AbilityTarget.SKILL_4: SimActKind.SKILL,
    AbilityTarget.HUMAN_SKILL_1: SimActKind.SKILL,
    AbilityTarget.HUMAN_SKILL_2: SimActKind.SKILL,
    AbilityTarget.HUMAN_SKILL_3: SimActKind.SKILL,
    AbilityTarget.HUMAN_SKILL_4: SimActKind.SKILL,
    AbilityTarget.DRAGON_SKILL_1: SimActKind.SKILL,
}

TARGET_TO_INDEX = {
    AbilityTarget.SKILL_1: 1,
    AbilityTarget.SKILL_2: 2,
    AbilityTarget.SKILL_3: 3,
    AbilityTarget.SKILL_4: 4,
    AbilityTarget.HUMAN_SKILL_1: 1,
    AbilityTarget.HUMAN_SKILL_2: 2,
    AbilityTarget.HUMAN_SKILL_3: 3,
    AbilityTarget.HUMAN_SKILL_4: 4,
    AbilityTarget.DRAGON_SKILL_1: 1,
}

TARGET_TO_FORM = {
    AbilityTarget.HUMAN_SKILL_1: PlayerForm.ADV,
    AbilityTarget.HUMAN_SKILL_2: PlayerForm.ADV,
    AbilityTarget.HUMAN_SKILL_3: PlayerForm.ADV,
    AbilityTarget.HUMAN_SKILL_4: PlayerForm.ADV,
    AbilityTarget.DRAGON_SKILL_1: PlayerForm.DRG,
}


class UnitType(Enum):
    NONE = 0
    Chara = 1
    Dragon = 2
    Amulet = 3
    Weapon = 4
    Skill = 5
    ExAbility2 = 6
    EventAbility = 7
    UnionBonus = 8


class AbCond:
    __slots__ = ["c_type", "values", "eval_fn", "moment"]
    eval_NONE = None

    def __init__(self, c_type: AbilityCondition, value: float, value_2: Optional[float] = None, value_str: Optional[str] = None) -> None:
        self.c_type = c_type
        self.values = (value, value_2, value_str)
        try:
            self.eval_fn: Optional[Callable] = getattr(self, f"eval_{self.c_type.name}")
        except AttributeError:
            self.eval_fn = None
        self.moment: Optional[MomentType] = CONDITON_TO_MOMENT.get(self.c_type)

    def eval(self, *args, **kwargs):
        if self.eval_fn is None:
            return True
        return self.eval_fn(*args, **kwargs)


class Vars(NamedTuple):
    a: Optional[int] = None
    b: Optional[int] = None
    c: Optional[int] = None
    s: Optional[str] = None


class AbSub:
    __slots__ = ["ab", "seq", "ab_type", "ex", "vars", "upval", "target", "activate_fn"]

    def __init__(self, ab: Union[Ability, ExAbility], seq: int):
        self.ab = ab
        self.seq = seq
        self.ab_type = AbilityType(self.ab._data[f"_AbilityType{self.seq}"])
        if self.ab_type is AbilityType.NONE:
            raise ValueError(self.ab_type)

        self.ex: bool = isinstance(ab, ExAbility)
        if self.ex:
            self.vars: Vars = Vars(a=self.ab._data[f"_VariousId{self.seq}"])
        else:
            self.vars: Vars = Vars(
                a=self.ab._data[f"_VariousId{self.seq}a"],
                b=self.ab._data[f"_VariousId{self.seq}b"],
                c=self.ab._data[f"_VariousId{self.seq}c"],
                s=self.ab._data[f"_VariousId{self.seq}str"],
            )

        self.upval: float = self.ab._data[f"_AbilityType{self.seq}UpValue"]
        self.target = AbilityTarget(self.ab._data[f"_TargetAction{self.seq}"])
        try:
            getattr(self, f"initialize_{self.ab_type.name}")()
        except AttributeError:
            pass
        try:
            self.activate_fn: Callable = getattr(self, f"activate_{self.ab_type.name}")
        except AttributeError:
            self.activate_fn = None

    def check_target_skill(self):
        if not self.ab.cond.eval():
            return False
        c_act = self.ab.player.current
        t_kind = TARGET_TO_ACTKIND[self.target]
        t_index = TARGET_TO_INDEX[self.target]
        if (t_form := TARGET_TO_FORM.get(self.target)) :
            return c_act.kind == t_kind and c_act.index == t_index and c_act.form == t_form
        return c_act.kind == t_kind and c_act.index == t_index

    def __repr__(self) -> str:
        if self.ab_type == AbilityType.ReferenceOther:
            return "Ref(\n:{}\n)".format("\n:".join(map(repr, self.vars)))
        return "{}{}({:.2f},{},{})".format("EX " if self.ex else "", self.ab_type.name, self.upval, self.target.name, self.vars)

    def initialize_ResistAbs(self) -> None:
        pass

    def initialize_ActDamageUp(self) -> None:
        if self.ex:
            bracket = (TARGET_TO_ACTKIND[self.target], "EX")
        else:
            bracket = (TARGET_TO_ACTKIND[self.target],)
        if self.target in TARGET_TO_INDEX:
            mod = Modifier(self.upval, bracket, active=self.check_target_skill)
        else:
            mod = Modifier(self.upval, bracket, active=self.ab.cond.eval_fn)
        self.ab.player.modifiers.add(mod)

    def initialize_ChangeState(self) -> None:
        pass

    def activate_ChangeState(self) -> None:
        pass

    def initialize_ReferenceOther(self) -> None:
        abilities: Sequence[Ability] = []
        for var in self.vars:
            try:
                abilities.append(Ability(var, self.ab.player))
            except ValueError:
                continue
        self.vars: Sequence[Ability] = abilities

    def activate_ReferenceOther(self) -> None:
        for ab in self.vars:
            ab.activate()

    def activate(self) -> None:
        if self.activate_fn is None:
            return
        self.activate_fn()


class Ability(FromDB, table="AbilityData"):
    __slots__ = ["player", "unit", "element", "weapon", "target", "cond", "cooltime", "sub"]

    def __init__(self, id: str, player: Player) -> None:
        super().__init__(id)
        if not self._data:
            raise ValueError(f'{id} not in AbilityData')
        self.player = player
        self.unit = UnitType(self._data["_UnitType"])
        self.element = ElementalType(self._data["_ElementalType"])
        self.weapon = ElementalType(self._data["_WeaponType"])
        self.target = AbilityTarget(self._data["_TargetAction"])
        self.cond = AbCond(AbilityCondition(self._data["_ConditionType"]), self._data["_ConditionValue"], self._data["_ConditionValue2"], self._data["_ConditionString"])
        if self._data["_CoolTime"]:
            self.cooltime = self.player.quest.timeline.schedule(self._data["_CoolTime"])
        else:
            self.cooltime = None
        self.sub: Sequence[AbSub] = []
        for i in range(1, 4):
            try:
                self.sub.append(AbSub(self, i))
            except ValueError:
                continue

        if self.cond.moment:
            self.player.events.listen(self.cond.moment, self.activate_by_moment)

    def activate_by_moment(self, *args, **kwargs):
        if not self.cond.eval(*args, **kwargs):
            return
        self._activate()

    def activate(self):
        if not self.cond.eval():
            return
        self._activate()

    def _activate(self):
        if self.cooltime is not None:
            if self.cooltime:
                return
            self.cooltime.start()

        for sub in self.sub:
            sub.activate()

    def __repr__(self) -> str:
        if not self.sub:
            return super().__repr__()
        return super().__repr__() + " [" + ",".join(map(repr, self.sub)) + "]"


class ExAbility(FromDB, table="ExAbilityData"):
    __slots__ = ["player", "cond", "category", "sub"]

    def __init__(self, id: str, player: Player) -> None:
        super().__init__(id)
        self.player = player
        self.cond = AbCond(AbilityCondition(self._data["_ConditionType"]), self._data["_ConditionValue"])
        self.category = self._data["_Category"]
        self.sub: Sequence[AbSub] = []
        for i in range(1, 4):
            try:
                self.sub.append(AbSub(self, i))
            except ValueError:
                continue

    def __repr__(self) -> str:
        if not self.sub:
            return super().__repr__()
        return super().__repr__() + "[" + ",".join(map(repr, self.sub)) + "]"
