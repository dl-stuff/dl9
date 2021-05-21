"""an action that can be called (acted) to trigger various effects"""
import os
import json
from typing import Optional

from action.parts import *
from core.constants import SimActKind

PLAYER_ACTION_FMT = os.path.join(os.path.dirname(__file__), "data", "PlayerAction_{:08}.json")


def _part_sort(part):
    return (part.seconds, part._seq)


class Action:
    def __init__(self, action_id: int, kind: SimActKind, index: int = 0) -> None:
        self._parts = []
        with open(PLAYER_ACTION_FMT.format(action_id), "r") as fn:
            for seq, data in enumerate(json.load(fn)):
                cmd = PartCmd(data["commandType"])
                try:
                    self._parts.append(globals()[f"Part_{cmd.name}"](self, seq, data))
                except KeyError:
                    continue
        self._parts = tuple(sorted(self._parts, key=_part_sort))

        self.kind = kind
        self.index = index

        self.has = None
        self.lv = None
        self.chlv = None

    def act(self, player: Player):
        for part in self._parts:
            part.act(self, player)