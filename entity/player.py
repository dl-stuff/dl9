"""A player character"""
from typing import Mapping, Optional, Sequence
from core.database import DBData
from core.quest import Quest
from core.modifier import ModifierDict
from core.timeline import EventManager
from __future__ import annotations  # default once 3.10


class Adventurer:
    def __init__(self, data: DBData) -> None:
        self._data = data

    def setup(self, settings: Optional[Mapping] = None):
        self.skills

    def edit_skill(self):
        pass

    def ex_abiility(self):
        pass


class Dragon:
    def __init__(self, data: DBData) -> None:
        self._data = data


class Weapon:
    def __init__(self, data: DBData) -> None:
        self._data = data


class Wyrmprints:
    def __init__(self, data: DBData) -> None:
        self._data = data


class PlayerTeam:
    def __init__(self, quest: Quest, players: Sequence[Player]) -> None:
        self.quest = quest
        self.events = EventManager()
        self.players = (None, None, None, None)
        for i in range(4):
            try:
                self.players[i] = players[i]
            except IndexError:
                break


class Player:
    def __init__(self, quest: Quest, team: PlayerTeam, adventurer: Adventurer, dragon: Dragon, weapon: Weapon, wyrmprints: Sequence[Wyrmprints]) -> None:
        self.quest = quest
        self.team = team
        self.events = EventManager()
        self.modifiers = ModifierDict()

        self.adventurer = adventurer
        self.dragon = dragon
        self.weapon = weapon
        self.wyrmprints = wyrmprints

        self.act = None

    # inputs
    def tap(self) -> bool:
        pass

    def skill(self, n: int = 1) -> bool:
        pass

    def shapeshift(self) -> bool:
        pass

    def mode(self, n: int = 1) -> bool:
        pass

    def hold(self) -> bool:
        pass

    def release(self) -> bool:
        pass

    def roll(self) -> bool:
        pass

    def swipe(self) -> bool:
        pass
