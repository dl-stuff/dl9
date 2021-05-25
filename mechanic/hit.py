"""Hit label and attribute"""
from enum import Enum
import functools
import re

from core.database import DBData, DBM
from mechanic.modifier import Modifier


class HitExec(Enum):
    NONE = 0
    DAMAGE = 1
    HEAL = 2
    CUSTOM = 3
    TRANS = 4
    DAMAGE_OBJ = 5
    NODAMAGE = 6
    HEAL_SP = 7
    MYSELF = 8
    HEAL_SP_HUMANONLY = 9
    DUMMY_DAMAGE = 10
    RESERVE_05 = 11


class HitTarget(Enum):
    NONE = 0
    MYSELF = 1
    ALLY = 2
    HOSTILE = 3
    BOTH = 4
    DUNOBJ = 5
    MYPARTY = 6
    ALLY_HP_LOWEST = 7
    HIT_OR_GUARDED_RECORD = 8
    HIT_RECORD = 9
    HOSTILE_AND_DUNOBJ = 10
    BIND = 11
    MYPARTY_EXCEPT_MYSELF = 12
    MYPARTY_EXCEPT_SAME_CHARID = 13
    HIT_OR_GUARDED_RECORD_ALLY = 14
    HIT_OR_GUARDED_RECORD_MYSELF = 15
    FIXED_OBJECT = 16
    MYSELF_CHECK_COLLISION = 17
    RESERVE_11 = 18
    RESERVE_12 = 19
    RESERVE_13 = 20


class HitAttribute:
    """A hit attribute"""

    def __init__(self, data: DBData) -> None:
        self._data = data
        self.name = data["_Id"]
        # self.hitexec = HitExec(data["_HitExecType"])
        # self.target = HitTarget(data["_TargetGroup"])
        # self.as_dragon = bool(data["_AttrDragon"])

        # CREATE TABLE PlayerActionHitAttribute (_Id TEXT,
        # _FontEffect TEXT,
        # _HitExecType INTEGER,
        # _TargetGroup INTEGER,
        # _TargetElemental INTEGER,
        # _Elemental01 INTEGER,
        # _Elemental02 INTEGER,
        # _Attributes02 INTEGER,
        # _Attributes03 INTEGER,
        # _LookToDamageType INTEGER,
        # _Attributes04 INTEGER,
        # _Attributes05 INTEGER,
        # _Attributes07 INTEGER,
        # _Attributes08 INTEGER,
        # _AttrIgnoreBarrier INTEGER,
        # _AttrNoReaction INTEGER,
        # _AttrShare INTEGER,
        # _AttrCancelBind INTEGER,
        # _AttrDragon INTEGER,
        # _DamageAdjustment REAL,
        # _ToOdDmgRate REAL,
        # _ToBreakDmgRate REAL,
        # _ToEightDownRate REAL,
        # _AdditionCritical REAL,
        # _IsAdditionalAttackToEnemy INTEGER,
        # _IsDamageMyself INTEGER,
        # _SetCurrentHpRate REAL,
        # _ConsumeHpRate REAL,
        # _DamageSelfUpFromBuffCountBuffId INTEGER,
        # _RecoveryValue INTEGER,
        # _AdditionRecoverySp INTEGER,
        # _RecoverySpRatio REAL,
        # _RecoverySpSkillIndex INTEGER,
        # _RecoverySpSkillIndex2 INTEGER,
        # _AdditionRecoveryDpPercentage REAL,
        # _RecoveryDragonTime REAL,
        # _AdditionRecoveryDpLv1 INTEGER,
        # _AdditionRecoveryDpAbility INTEGER,
        # _RecoveryEp INTEGER,
        # _RecoveryCP INTEGER,
        # _RecoveryCPIndex INTEGER,
        # _RecoveryCPEveryHit INTEGER,
        # _AdditionActiveGaugeValue INTEGER,
        # _AdditionRecoveryUtp INTEGER,
        # _AddUtp INTEGER,
        # _IgnoreHitCountAddition INTEGER,
        # _IgnoreFirstHitCheck INTEGER,
        # _FixedDamage INTEGER,
        # _CurrentHpRateDamage INTEGER,
        # _HpDrainRate REAL,
        # _HpDrainRate2 REAL,
        # _HpDrainLimitRate REAL,
        # _HpDrainAttribute TEXT,
        # _DamageCounterCoef REAL,
        # _CrisisLimitRate REAL,
        # _DamageDispDelaySec REAL,
        # _IsDisableHealSpOnCurse INTEGER,
        # _ActionCondition1 INTEGER,
        # _HeadText TEXT,
        # _BattleLogText TEXT,
        # _ActionGrant INTEGER,
        # _AuraId INTEGER,
        # _AuraMaxLimitLevel INTEGER,
        # _KillerState1 INTEGER,
        # _KillerState2 INTEGER,
        # _KillerState3 INTEGER,
        # _KillerStateDamageRate REAL,
        # _KillerStateRelease INTEGER,
        # _DamageUpRateByBuffCount REAL,
        # _DamageUpDataByBuffCount INTEGER,
        # _SplitDamageCount INTEGER,
        # _SplitDamageCount2 INTEGER,
        # _ArmorBreakLv INTEGER,
        # _InvincibleBreakLv INTEGER,
        # _KnockBackType INTEGER,
        # _KnockBackDistance REAL,
        # _KnockBackDependsOnMass INTEGER,
        # _KnockBackDurationSec REAL,
        # _UseDamageMotionTimeScale INTEGER,
        # _DamageMotionTimeScale REAL,
        # _HitConditionType INTEGER,
        # _HitConditionP1 INTEGER,
        # _HitConditionP2 INTEGER,
        # _IsAddCombo INTEGER,
        # _BlastHeight REAL,
        # _BlastAngle REAL,
        # _BlastGravity REAL)


HAS_PATTERN = re.compile(r"HAS")
LV_PATTERN = re.compile(r"LV(\d{2})")
CHLV_PATTERN = re.compile(r"CHLV(\d{2})")


class HitLabel:
    __slots__ = ["_fragments", "_has", "_lv", "_chlv"]
    # ALL_LABELS = DBM.query_all_as_dict("SELECT * FROM PlayerActionHitAttribute")

    def _find_fragment(self, pattern):
        idx = 0
        while idx < len(self._fragments) and not pattern.match(self._fragments[idx]):
            idx += 1
        if idx == len(self._fragments):
            return None
        return idx

    def __init__(self, name: str):
        self._fragments = tuple(name.split("_"))
        self._has = self._find_fragment(HAS_PATTERN)
        self._lv = self._find_fragment(LV_PATTERN)
        self._chlv = self._find_fragment(CHLV_PATTERN)

    @functools.lru_cache()
    def get(self, lv: int = None, chlv: int = None, has: bool = False):
        fragments = list(self._fragments)
        if has and self._has is None:
            fragments.append("HAS")
        elif not has and self._has is not None:
            fragments.pop(self._has)
        if lv is not None:
            if self._lv is None:
                fragments.append(f"LV{lv:02}")
            else:
                fragments[self._lv] = f"LV{lv:02}"
        if chlv is not None:
            if self._chlv is None:
                fragments.append(f"CHLV{chlv:02}")
            else:
                fragments[self._chlv] = f"CHLV{chlv:02}"
        hitattr = DBM.query_one("SELECT * FROM PlayerActionHitAttribute WHERE _Id=?", ("_".join(fragments),))
        if hitattr:
            return HitAttribute(hitattr)
        return None
