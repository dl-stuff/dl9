"""A player character"""
from __future__ import annotations  # default once 3.10
from typing import Mapping, Optional, Sequence

from core.database import DBData
from core.quest import Quest
from core.modifier import ModifierDict
from core.timeline import EventManager
from action import Action


class PlayerData:
    def __init__(self, data: DBData) -> None:
        self._data = data

    def setup(self, player: Player):
        return NotImplemented


class Skill(PlayerData):
    def __init__(self, data: DBData, level: int = 1) -> None:
        super().__init__(data)
        self.level = level

    def setup(self, player: Player):
        pass


class Adventurer(PlayerData):
    def edit_skill(self):
        pass

    def ex_abiility(self):
        pass


class Dragon(PlayerData):
    pass


class Weapon(PlayerData):
    pass


class Wyrmprints(PlayerData):
    pass


class PlayerTeam:
    def __init__(self, quest: Quest) -> None:
        self.quest = quest
        self.events = EventManager()
        self.players = [None, None, None, None]

    def add(self, player: Player):
        i = 0
        while self.players[i] is not None:
            i += 1
        if i > 4:
            return
        self.players[i] = player


class Player:
    def __init__(self, quest: Quest, team: PlayerTeam, adventurer: Adventurer, dragon: Dragon, weapon: Weapon, wyrmprints: Sequence[Wyrmprints]) -> None:
        self.quest = quest
        self.team = team
        self.team.add(self)
        self.events = EventManager()
        self.modifiers = ModifierDict()

        self.adventurer = adventurer
        self.dragon = dragon
        self.weapon = weapon
        self.wyrmprints = wyrmprints

        self.current: Action = None

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
