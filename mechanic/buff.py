from collections import deque
from entity import Entity
from typing import MutableMapping, MutableSequence, Set, TYPE_CHECKING, Optional
from enum import Enum

if TYPE_CHECKING:
    from entity.player import Player

from core.database import FromDB, DBData


class BlockExhaust(Enum):
    NONE = 0
    InAnySkill = 1
    InTransform = 2


class BuffFlag(Enum):
    Normal = 0
    NoIcon = 1
    NoCount = 2


class BuffEff(Enum):
    Add = 0
    RemoveTypeAll = 1
    RemoveStack = 2
    RemoveBuffAll = 97
    RemoveDebuffAll = 98
    RemoveAll = 99
    Dispel = 100


class ActionCondition(FromDB, table="ActionCondition"):
    def __init__(self, id: int, entity: Entity) -> None:
        super().__init__(id)
        if not self._data:
            raise ValueError(f"{id} not in ActionCondition")
        self._timers = deque(maxlen=self._data["_MaxDuplicatedCount"] or None)
        self.entity = entity
        self.icon = self._data["_UniqueIcon"] or None

    @staticmethod
    def _get_name(data: Optional[DBData]):
        if not data:
            return None
        return data.get("_Text")

    @property
    def stack(self):
        return len(self._timers)


class ActionConditionManager:
    def __init__(self, entity: Entity) -> None:
        self.entity = entity
        self.all_actcond: MutableMapping[ActionCondition] = {}
        self.buffs: Set[int] = set()
        self.debuffs: Set[int] = set()

    def start_actcond(self, id: int):
        try:
            actcond = self.all_actcond[id]
        except KeyError:
            actcond = ActionCondition(id, self.entity)
            self.all_actcond[id] = actcond
        # figure out buff vs debuff
        # activate the actcond

    @property
    def buffcount(self):
        return sum((self.all_actcond[buff_id].stack for buff_id in self.buffs))

    @property
    def iconcount(self):
        return len(set(self.all_actcond[buff_id].icon for buff_id in self.buffs if self.all_actcond[buff_id].icon))