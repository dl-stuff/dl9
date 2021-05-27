from enum import Enum
from entity import Entity
from core.database import FromDB, DBData
from core.constants import AfflictType
from typing import Optional


class AffGroup(Enum):
    DOT = 1
    CC = 2


class Affliction(FromDB, table="AbnormalStatusType"):
    def __init__(self, aff_type: AfflictType, entity: Entity) -> None:
        super().__init__(aff_type.value)
        self.entity = entity
        self.resist = 0
        self.gain = self._data["_ResistGain"]
        self.group = AffGroup(self._data["_Group"])

    @staticmethod
    def _get_name(data: Optional[DBData]):
        if not data:
            return None
        return data.get("_AbnormalName")