"""Hit label and attribute"""
from __future__ import annotations
from entity import Entity
from entity.player import Player
from core.constants import Bracket, ElementalType, PlayerForm
from enum import Enum
import functools
import re
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from action import Action


from core.database import DBData, DBM, FromDB
from mechanic.modifier import Modifier, ModifierDict


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


class KillerState(Enum):
    NONE = 0
    AbsPoison = 1
    AbsBurn = 2
    AbsFreeze = 3
    AbsParalysis = 4
    AbsDarkness = 5
    AbsSwoon = 6
    AbsCurse = 7
    AbsRebirth = 8
    AbsSlowMove = 9
    AbsSleep = 10
    AbsFrostbite = 11
    AbsFlashheat = 12
    AbsCrashwind = 13
    AbsDarkabs = 14
    AbsDestroyfire = 15
    AbsAll = 99
    DbfHp = 101
    DbfAttack = 102
    DbfDefense = 103
    DbfCritical = 104
    DbfSkillPower = 105
    DbfBurstPower = 106
    DbfRecovery = 107
    DbfGash = 108
    BfDbfAll = 197
    BfAll = 198
    DbfAll = 199
    Break = 201


class KnockBackType(Enum):
    NONE = 0
    NORMAL = 1
    RANDOM = 2
    SLIDE = 3
    ABSORPT = 4
    EVICTION = 5
    REPULSION = 6
    ABSORPT_EA = 7
    REPULSION_EA = 8
    RESERVE_04 = 9
    RESERVE_05 = 10


class DamageTo(Enum):
    HP = 1
    OD = 2


class PHitCond(Enum):
    NONE = 0
    HIT_TARGET_NUM_IN_P1P2 = 1
    HIT_NUM_IN_P1P2 = 2


DAMAGE_CONST = 5 / 3


def check_crisis(caster: Entity):
    return (1 - caster.hp.percent) ** 2


def check_killerstates(caster: Entity, states: Sequence[KillerState]):
    return 1


def check_buffcount(caster: Entity):
    return 0


class BuffCountData(FromDB, table="BuffCountData"):
    def __init__(self, id: int, hitattr: HitAttribute) -> None:
        super().__init__(id)
        self.hitattr = hitattr

    def mod_buffcountdata(self):
        return 1


class HitAttribute:
    """A hit attribute"""

    def __init__(self, data: DBData, action: Action) -> None:
        self._data = data
        self.action = action
        self.name = self._data["_Id"]
        self.hitexec = HitExec(self._data["_HitExecType"])
        self.target_group = HitTarget(self._data["_TargetGroup"])
        self.target_ele = None if not self._data["_TargetElemental"] else ElementalType(self._data["_TargetElemental"])
        if self._data["_Elemental01"]:
            self.hit_ele = ElementalType(self._data["_Elemental01"])
        else:
            if self.action.form == PlayerForm.ADV:
                self.hit_ele = self.action.player.adventurer.element
            elif self.action.form == PlayerForm.DRG:
                self.hit_ele = self.action.player.dragon.element

        self.attr_dragon = bool(self._data["_AttrDragon"])
        self.overdamage = bool(self._data["_IsAdditionalAttackToEnemy"])

        self.hit_modifiers = ModifierDict()
        # self.od_fill = self._data["_ToOdDmgRate"]
        # if self._data["_ToBreakDmgRate"] > 1:
        #     self.hit_modifiers.add(Modifier(self._data["_ToBreakDmgRate"] - 1, (DamageTo.OD,)))
        if self._data["_AdditionCritical"]:
            self.hit_modifiers.add(Modifier(self._data["_AdditionCritical"], (Bracket.CritRate,)))
        if self._data["_CrisisLimitRate"]:
            self.hit_modifiers.add(Modifier(self._data["_CrisisLimitRate"] - 1, (Bracket.Killer, "HIT_CRISIS"), self.mod_crisis_fn))
        if self._data["_KillerStateDamageRate"]:
            self.killer_states = tuple((KillerState(ks) for ks in (self._data["_KillerState1"], self._data["_KillerState2"], self._data["_KillerState3"]) if ks))
            self.hit_modifiers.add(Modifier(self._data["_KillerStateDamageRate"] - 1, (Bracket.Killer, "HIT_KS"), self.mod_killerstates_fn))
        if self._data["_DamageUpRateByBuffCount"]:
            self.hit_modifiers.add(Modifier(self._data["_DamageUpRateByBuffCount"], (Bracket.Misc, "BUFFCOUNT"), self.mod_buffcount_fn))
        if self._data["_DamageUpDataByBuffCount"]:
            self.bcd = BuffCountData(self._data["_DamageUpDataByBuffCount"])
            self.hit_modifiers.add(Modifier(1, (Bracket.Misc, "BUFFCOUNTDATA"), self.bcd.mod_buffcountdata))

    def mod_crisis_fn(self):
        return check_crisis(self.action.player)

    def mod_killerstates_fn(self):
        return check_killerstates(self.action.player, self.action.player)

    def mod_buffcount_fn(self):
        return check_buffcount(self.action.player)

    def proc(self):
        # get the targets
        # depending on self.hitexec, call diff sub functions
        # respect self.action.once_per_action
        pass

    def hitattr_damage_formula(self, source: Entity, target: Entity, damage_to: DamageTo = DamageTo.HP):
        # strength modifier
        # act damage
        # killer
        # punisher
        # target
        pass


HAS_PATTERN = re.compile(r"HAS")
LV_PATTERN = re.compile(r"LV(\d{2})")
CHLV_PATTERN = re.compile(r"CHLV(\d{2})")


class HitLabel:
    __slots__ = ["action", "_fragments", "_has", "_lv", "_chlv"]
    # ALL_LABELS = DBM.query_all_as_dict("SELECT * FROM PlayerActionHitAttribute")

    def _find_fragment(self, pattern):
        idx = 0
        while idx < len(self._fragments) and not pattern.match(self._fragments[idx]):
            idx += 1
        if idx == len(self._fragments):
            return None
        return idx

    def __init__(self, name: str, action: Action):
        self.action = action
        self._fragments = tuple(name.split("_"))
        self._has = self._find_fragment(HAS_PATTERN)
        self._lv = self._find_fragment(LV_PATTERN)
        self._chlv = self._find_fragment(CHLV_PATTERN)

    @functools.lru_cache()
    def get(self, lv: int = None, chlv: int = None, has: bool = False):
        # we will use arguments despite having action to trigger caching.
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
            return HitAttribute(hitattr, self.action)
        return None
