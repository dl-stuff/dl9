from core.utility import HP
from core.timeline import EventManager

from core.quest import Quest
from mechanic.modifier import ModifierDict


class Entity:
    def __init__(self, quest: Quest) -> None:
        self.quest = quest
        self.events = EventManager()
        self.modifiers = ModifierDict()
        self.hp = HP(entity=self)