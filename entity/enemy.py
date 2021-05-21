from core.database import DBData
from core.quest import Quest


class Enemy:
    def __init__(self, quest: Quest, data: DBData) -> None:
        self.quest = quest
        self._data = data
