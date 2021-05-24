"""Hit label and attribute"""
from enum import Enum
import functools
import re

from core.database import DBData, DBM
from entity.modifier import Modifier


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
        self.hitexec = HitExec(data["_HitExecType"])
        self.target = HitTarget(data["_TargetGroup"])
        self.as_dragon = bool(data["_AttrDragon"])

    # def set_modifiers(self, player: Player) -> None:
    #     player.modifiers.add(Modifier(self._data["_DamageAdjustment"]))
    # "_DamageAdjustment": 0.0,
    # "_ToOdDmgRate": 0.0,
    # "_ToBreakDmgRate": 0.0,
    # "_ToEightDownRate": 0.0,
    # "_AdditionCritical": 0.0,
    # "_IsAdditionalAttackToEnemy": 0,
    # "_IsDamageMyself": 0,
    # "_SetCurrentHpRate": 0.0,
    # "_ConsumeHpRate": 0.0,
    # "_DamageSelfUpFromBuffCountBuffId": 0,
    # "_RecoveryValue": 0,
    # "_AdditionRecoverySp": 0,
    # "_RecoverySpRatio": 0.0,
    # "_RecoverySpSkillIndex": 0,
    # "_RecoverySpSkillIndex2": 0,
    # "_AdditionRecoveryDpPercentage": 0.0,
    # "_RecoveryDragonTime": 0.0,
    # "_AdditionRecoveryDpLv1": 0,
    # "_AdditionRecoveryDpAbility": 0,
    # "_RecoveryEp": 0,
    # "_RecoveryCP": 0,
    # "_RecoveryCPIndex": 0,
    # "_RecoveryCPEveryHit": 0,
    # "_AdditionActiveGaugeValue": 0,
    # "_AdditionRecoveryUtp": 0,
    # "_AddUtp": 0,
    # "_IgnoreHitCountAddition": 0,
    # "_IgnoreFirstHitCheck": 0,
    # "_FixedDamage": 0,
    # "_CurrentHpRateDamage": 0,
    # "_HpDrainRate": 0.0,
    # "_HpDrainRate2": 0.0,
    # "_HpDrainLimitRate": 0.0,
    # "_HpDrainAttribute": "",
    # "_DamageCounterCoef": 0.0,
    # "_CrisisLimitRate": 0.0,
    # "_DamageDispDelaySec": 0.0,
    # "_IsDisableHealSpOnCurse": 0,
    # "_ActionCondition1": 0,
    # "_HeadText": "ACTION_CONDITION_0",
    # "_BattleLogText": "",
    # "_ActionGrant": 0,
    # "_AuraId": 10000,
    # "_AuraMaxLimitLevel": 2,
    # "_KillerState1": 0,
    # "_KillerState2": 0,
    # "_KillerState3": 0,
    # "_KillerStateDamageRate": 0.0,
    # "_KillerStateRelease": 0,
    # "_DamageUpRateByBuffCount": 0.0,
    # "_DamageUpDataByBuffCount": 0,
    # "_SplitDamageCount": 0,
    # "_SplitDamageCount2": 0,
    # "_ArmorBreakLv": 4,
    # "_InvincibleBreakLv": 1,
    # "_KnockBackType": 1,
    # "_KnockBackDistance": 0.699999988079071,
    # "_KnockBackDependsOnMass": 0,
    # "_KnockBackDurationSec": 0.30000001192092896,
    # "_UseDamageMotionTimeScale": 1,
    # "_DamageMotionTimeScale": 1.2000000476837158,
    # "_HitConditionType": 0,
    # "_HitConditionP1": 0,
    # "_HitConditionP2": 0,
    # "_IsAddCombo": 0,
    # "_BlastHeight": 1.5,
    # "_BlastAngle": 60.0,
    # "_BlastGravity": 25.0


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
