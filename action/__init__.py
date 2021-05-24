"""an action that can be called (acted) to trigger various effects"""
from __future__ import annotations
from collections import defaultdict  # default once 3.10
import os
import json
from typing import List, Sequence, Dict, TYPE_CHECKING, Tuple

from action.parts import *
from core.constants import SimActKind, PlayerForm
from core.database import FromDB

if TYPE_CHECKING:
    from entity.player import Player

PLAYER_ACTION_FMT = os.path.join(os.path.dirname(__file__), "data", "PlayerAction_{:08}.json")


def _part_sort(part):
    return (part.seconds, part._seq)


class Action(FromDB, table="PlayerAction"):
    def __init__(self, id: int, player: Player, kind: SimActKind, form: PlayerForm = PlayerForm.ADV, index: int = 0) -> None:
        super().__init__(id)
        self.player = player
        self.status = False
        self.kind = kind
        self.form = form
        self.index = index

        self._parts: Sequence[Part] = []
        with open(PLAYER_ACTION_FMT.format(self.id), "r") as fn:
            for seq, data in enumerate(json.load(fn)):
                cmd = PartCmd(data["commandType"])
                try:
                    self._parts.append(globals()[f"Part_{cmd.name}"](self, seq, data))
                except (KeyError, DisregardPart):
                    continue
        self._parts = tuple(sorted(self._parts, key=_part_sort))

        self.has = None
        self.lv = None
        self.chlv = None

        self.signals: Dict[SignalType, List[Part_SEND_SIGNAL]] = defaultdict(list)
        self.cancel_by: List[int] = []
        self.cancel_by_any: bool = False

    def start(self) -> None:
        self.player.current = self
        self.status = True
        for part in self._parts:
            part.start()

    def add_cancel(self, by_type: InputType, by_action: int):
        if by_type is InputType.NONE:
            self.cancel_by_any = True
        else:
            self.cancel_by.append(by_action)

    def can_cancel(self, by_action: Action) -> bool:
        return not self.status or self.cancel_by_any or by_action.id in self.cancel_by

    def cancel(self, by_action: Action) -> None:
        if not self.can_cancel(by_action):
            return False
        self.end()

    def end(self) -> None:
        if self.status:
            for part in self._parts:
                part.cancel()
            self.status = False
            self.signals.clear()
            self.cancel_by.clear()
            self.cancel_by_any = False
            self.player.to_neutral()


class Neutral(Action):
    def __init__(self) -> None:
        pass

    def start(self) -> None:
        pass

    def can_cancel(self, by_action: Action) -> bool:
        return True

    def cancel(self, by_action: Action) -> None:
        pass

    def end(self) -> None:
        pass
