"""A quest with a timeline and some event managers"""
from __future__ import annotations
from typing import MutableSequence, TYPE_CHECKING
from core.timeline import Timeline, EventManager
from core.log import Logger

if TYPE_CHECKING:
    from entity.player import Player, Team
    from entity.enemy import Enemy


class Quest:
    MAX_PLAYER = 16
    MAX_TEAM = 4
    # MAX_ENEMY = 1
    __slots__ = ["timeline", "events", "logger", "players", "teams", "enemies"]

    def __init__(self) -> None:
        self.timeline = Timeline()
        self.events = EventManager()
        self.logger = Logger(self.timeline)

        self.players: MutableSequence[Player] = []
        self.teams: MutableSequence[Team] = []
        self.enemies: Enemy = None

    def add_player(self, player: Player):
        if len(self.players) < Quest.MAX_PLAYER:
            self.players.append(player)

    def add_team(self, team: Team):
        if len(self.players) < Quest.MAX_TEAM:
            self.teams.append(team)
            self.events.add_child(team.events)

    def set_enemy(self, enemy: Enemy):
        self.enemy = enemy
        self.events.add_child(enemy.events)
