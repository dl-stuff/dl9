"""Hit label and attribute"""
from __future__ import annotations
from entity.player import Player
from core.constants import ElementalType, PlayerForm
from enum import Enum
import functools
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from action import Action


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


class PHitCond(Enum):
    NONE = 0
    HIT_TARGET_NUM_IN_P1P2 = 1
    HIT_NUM_IN_P1P2 = 2


class HitAttribute:
    """A hit attribute"""

    def __init__(self, data: DBData, action: Action) -> None:
        self._data = data
        self.action = action
        self.name = self._data["_Id"]
        self.hitexec = HitExec(self._data["_HitExecType"])
        try:
            self.hitexec_fn = getattr(self, f"hit_{self.hitexec.name}")
        except AttributeError:
            self.hitexec_fn = None
        self.target = HitTarget(self._data["_TargetGroup"])
        self.target_ele = None if not self._data["_TargetElemental"] else ElementalType(self._data["_TargetElemental"])
        if self._data["_Elemental01"]:
            self.hit_ele = ElementalType(self._data["_Elemental01"])
        else:
            if self.action.form == PlayerForm.ADV:
                self.hit_ele = self.action.player.adventurer.element
            elif self.action.form == PlayerForm.DRG:
                self.hit_ele = self.action.player.dragon.element

    def hit_DAMAGE(self):
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
