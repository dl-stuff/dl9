"""Series of actions that form a combo chain"""
from __future__ import annotations
from typing import Optional, Sequence, TYPE_CHECKING

from action import Action
from core.utility import Array
from core.constants import PlayerForm, SimActKind, MomentType
from core.database import FromDB

if TYPE_CHECKING:
    from entity.player import Player


class Combos:
    def __init__(self, player: Player, form: PlayerForm, act_ids: Sequence[int], ex_act_ids: Optional[Sequence[int]] = None) -> None:
        self.player = player
        self.actions: Array[Action] = Array()
        for idx, act_id in enumerate(act_ids):
            self.actions.append(Action(act_id, player, kind=SimActKind.COMBO, form=form, index=idx + 1))
        self.ex_actions = None
        if ex_act_ids:
            self.ex_actions: Array[Action] = Array()
            for idx, act_id in enumerate(ex_act_ids):
                if not act_id:
                    self.ex_actions.append(None)
                    continue
                self.ex_actions.append(Action(act_id, player, kind=SimActKind.COMBO, form=form, index=idx + 1))

    def next(self):
        if self.player.current in self.actions:
            try:
                return self.actions[self.player.current.index + 1]
            except IndexError:
                pass
        return self.actions[1]

    def __repr__(self) -> str:
        if self.ex_actions:
            return "->".join(map(repr, self.actions)) + "\tEX[" + "->".join(map(repr, self.ex_actions)) + "]"
        return "->".join(map(repr, self.actions))


class UniqueCombos(Combos, FromDB, table="CharaUniqueCombo"):
    def __init__(self, id: int, player: Player) -> None:
        FromDB.__init__(self, id)
        act_ids = (self._data["_ActionId"] + i for i in range(self._data["_MaxComboNum"]))
        ex_act_ids = None if not self._data["_ExActionId"] else (self._data["_ExActionId"] + i for i in range(self._data["_MaxComboNum"]))
        Combos.__init__(self, player, PlayerForm.ADV, act_ids, ex_act_ids=ex_act_ids)
        if self._data["_ShiftConditionType"] == 1:
            self.player.events.listen(MomentType.HIT, self.enable)

    def enable(self, *args, **kwargs):
        pass


class DefaultCombos(Combos, FromDB, table="WeaponType"):
    def __init__(self, id: int, player: Player) -> None:
        FromDB.__init__(self, id)
        act_ids = (self._data[f"_DefaultSkill{i+1:02}"] for i in range(5) if self._data[f"_DefaultSkill{i+1:02}"])
        ex_act_ids = None if not self._data["_DefaultSkill05Ex"] else (0, 0, 0, 0, self._data["_DefaultSkill05Ex"])
        Combos.__init__(self, player, PlayerForm.ADV, act_ids, ex_act_ids=ex_act_ids)


class DragonCombos(Combos):
    def __init__(self, id: int, combo_max: int, player: Player) -> None:
        act_ids = (id + i for i in range(combo_max))
        Combos.__init__(self, player, PlayerForm.DRG, act_ids)
