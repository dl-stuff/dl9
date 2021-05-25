"""Skills that can be used to do stuff"""
from __future__ import annotations
from enum import Enum  # default once 3.10
from typing import Optional, Sequence, TYPE_CHECKING

import core.random
from core.database import FromDB
from core.constants import SimActKind
from core.constants import PlayerForm
from action import Action

if TYPE_CHECKING:
    from entity.player import Player


class SkillCtx(Enum):
    OWN = ""
    EDIT = "Edit"
    DRAGON = "Dragon"


class Skill(FromDB, table="SkillData"):
    def __init__(self, id: str, player: Optional[Player] = None, level: int = 1, form: PlayerForm = PlayerForm.ADV, index: int = 1, context: SkillCtx = SkillCtx.OWN) -> None:
        super().__init__(id)
        self.level = level
        self.form = form
        self.index = index
        self.context = context
        self.player = player

        self.sp_key = (form, index)
        msp_key = "_Sp" if self.level == 1 else f"_SpLv{self.level}"
        msp_key += self.context.value
        self.req_sp = self._data[msp_key]
        self.player.sp[self.sp_key].set_req(self.req_sp)
        self.can_tension = bool(self._data[f"_IsAffectedByTensionLv{self.level}"] or self._data["_IsAffectedByTension"])

        self._actions: Sequence[Action] = []
        if (advanced_level := self._data["_AdvancedSkillLv1"]) and level >= advanced_level:
            self._actions.append(Action(self._data["_AdvancedActionId1"], self.player, SimActKind.SKILL, form=self.form, index=self.index))
        else:
            self._actions.append(Action(self._data["_ActionId1"], self.player, SimActKind.SKILL, form=self.form, index=self.index))
        for i in range(2, 5):
            if act_id := self._data[f"_ActionId{i}"]:
                self._actions.append(Action(self._data[act_id], self.player, SimActKind.SKILL, form=self.form, index=self.index))

    def check(self) -> bool:
        if self.player.sp[self.sp_key].count >= 1 and self.player.current.can_cancel(self.action()):
            return True
        return False

    def action(self) -> Action:
        if len(self._actions) > 1:
            return core.random.choice(self._actions)
        return self._actions[0]

    def cast(self) -> None:
        if not self.check():
            return
        self.player.sp[self.sp_key].charge(-self.req_sp)
        self.action().start()