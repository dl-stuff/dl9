"""an action that can be called (acted) to trigger various effects"""
from __future__ import annotations
from collections import defaultdict  # default once 3.10
import os
import json
from typing import List, Sequence, Dict, TYPE_CHECKING

from action.parts import *
from core.constants import SimActKind

if TYPE_CHECKING:
    from entity.player import Player

PLAYER_ACTION_FMT = os.path.join(os.path.dirname(__file__), "data", "PlayerAction_{:08}.json")


def _part_sort(part):
    return (part.seconds, part._seq)


class Action:
    def __init__(self, player: Player, action_id: int, kind: SimActKind, index: int = 0) -> None:
        self.player = player
        self.status = False
        self.id = action_id
        self._parts: Sequence[Part] = []
        with open(PLAYER_ACTION_FMT.format(action_id), "r") as fn:
            for seq, data in enumerate(json.load(fn)):
                cmd = PartCmd(data["commandType"])
                try:
                    self._parts.append(globals()[f"Part_{cmd.name}"](self, seq, data))
                except (KeyError, DisregardPart):
                    continue
        self._parts = tuple(sorted(self._parts, key=_part_sort))

        self.kind = kind
        self.index = index

        self.has = None
        self.lv = None
        self.chlv = None

        self.signals: Dict[SignalType, List[Part_SEND_SIGNAL]] = defaultdict(list)
        self.cancel_by: List[int] = []

    def start(self) -> None:
        self.player.current = self
        self.status = True
        for part in self._parts:
            part.start()

    def can_cancel(self, by_action: Action) -> bool:
        return not self.status or by_action.id in self.cancel_by

    def cancel(self, by_action: Action) -> bool:
        if not self.can_cancel(by_action):
            return False
        for part in self._parts:
            part.cancel()
        self.end()

    def end(self) -> None:
        self.status = False
        self.signals.clear()
        self.cancel_by.clear()
