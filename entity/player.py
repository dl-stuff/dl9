"""A player character"""
from __future__ import annotations
from enum import Enum
from functools import total_ordering  # default once 3.10
from typing import Mapping, Optional, Sequence, NamedTuple, Tuple, Union

from core.database import FromDB
from core.quest import Quest
from core.timeline import EventManager
from core.log import LogKind
from core.constants import PlayerForm
from core.utility import cfloat_mult, Array
from action import Action, Neutral
from entity.modifier import ModifierDict
from entity.ability import Stat


class PlayerConf(NamedTuple):
    adventurer: int
    dragon: int
    weapon: int
    wyrmprints: Sequence[int]


class Adventurer(FromDB, table="CharaData"):
    def __init__(self, id: int, player: Optional[Player] = None) -> None:
        super().__init__(id)
        self.anim_ref = None
        if self._data:
            self.anim_ref = f'{self._data["_BaseId"]:06}{self._data["_VariationId"]:02}'

    def edit_skill(self):
        pass

    def ex_abiility(self):
        pass


class Dragon(FromDB, table="DragonData"):
    def __init__(self, id: int, player: Optional[Player] = None) -> None:
        super().__init__(id)
        self.anim_ref = None
        if self._data:
            if self._data["_AnimFileName"]:
                self.anim_ref = self._data["_AnimFileName"].replace("_", "")
            else:
                self.anim_ref = f'd{self._data["_BaseId"]}{self._data["_VariationId"]:02}'


class Weapon(FromDB, table="WeaponBody"):
    def __init__(self, id: int, player: Optional[Player] = None) -> None:
        super().__init__(id)


class Wyrmprint(FromDB, table="AbilityCrest"):
    def __init__(self, id: int) -> None:
        super().__init__(id)


class Wyrmprints:
    def __init__(self, id_list: Sequence[int]) -> None:
        self.wps = tuple((Wyrmprint(id) for id in id_list))


class PlayerTeam:
    MAX_PLAYER = 4

    def __init__(self, quest: Quest) -> None:
        self.quest = quest
        self.events = EventManager()
        self.players = []

    def add(self, player: Player):
        if len(self.players) > PlayerTeam.MAX_PLAYER:
            return
        self.players.append(player)


class Gauge:
    __slots__ = ["current_value", "required_value", "maximum_value"]

    def __init__(self) -> None:
        self.current_value: int = 0
        self.required_value: int = 0
        self.maximum_value: int = 0

    def charge(self, value: int):
        self.current_value = max(min(self.current_value + value, self.maximum_value), 0)

    def charge_percent(self, percent: float):
        self.charge(cfloat_mult(self.required_value, percent))

    @property
    def count(self) -> int:
        return self.current_value // self.required_value

    @property
    def percent(self) -> float:
        return self.current_value / self.required_value

    def __repr__(self) -> str:
        if self.required_value == self.maximum_value:
            return "{}/{}".format(self.current_value, self.required_value)
        return "{}/{} [{}]".format(self.current_value, self.maximum_value, self.count)

    def set_req(self, value: int):
        self.required_value = value
        self.maximum_value = max(self.maximum_value, self.required_value)

    def set_max(self, value: int):
        self.maximum_value = value
        self.required_value = min(self.maximum_value, self.required_value)


class SPManager:
    __slots__ = ["player", "a", "d", "_mapping"]

    def __init__(self, player: Player) -> None:
        self.player = player

        # force 1-index
        self.a = Array(Gauge(), Gauge(), Gauge(), Gauge())
        self.d = Array(Gauge(), Gauge())
        self._mapping: Mapping[PlayerForm, Sequence[Gauge]] = {PlayerForm.ADV: self.a, PlayerForm.DRG: self.d}

    def targets(self, form=None):
        if (form or self.player.form) == PlayerForm.ADV:
            return ((PlayerForm.ADV, i) for i in range(1, 5))
        else:
            return ((PlayerForm.DRG, i) for i in range(1, 3))

    def charge(self, value: int, key: Union[None, PlayerForm, Tuple[PlayerForm, int]] = None, percent: bool = False):
        if key is None:
            targets = self.targets()
        elif type(key) is PlayerForm:
            targets = self.targets(form=key)
            key = None
        else:
            targets = (key,)

        if percent:
            for form, idx in targets:
                self._mapping[form][idx].charge_percent(percent)
        else:
            spr_mod = 1 + self.player.modifiers.submod((Stat.Spr,))
            for form, idx in targets:
                self._mapping[form][idx].charge(cfloat_mult(value, spr_mod + self.player.modifiers.submod((Stat.Spr, idx))))

        if key is None:
            self.player.log("{} +{} {}", self.player.form.name, value, self)
        else:
            self.player.log("{} +{} s{} {}", key[0].name, key[1], value, self)

    def __repr__(self) -> str:
        return "[ " + " | ".join((repr(self._mapping[form][idx]) for form, idx in self.targets())) + " ]"

    def __getitem__(self, key: Tuple[PlayerForm, int]) -> Gauge:
        form, idx = key
        return self._mapping[form][idx]


class Player:
    def __init__(self, quest: Quest, team: PlayerTeam, conf: PlayerConf) -> None:
        self.quest = quest
        self.team = team
        self.team.add(self)
        self.events = EventManager()
        self.modifiers = ModifierDict()

        self.sp = SPManager(self)

        self.adventurer = Adventurer(conf.adventurer)
        self.dragon = Dragon(conf.dragon)
        self.weapon = Weapon(conf.weapon)
        self.wyrmprints = Wyrmprints(conf.wyrmprints)

        self.form = PlayerForm.ADV
        self._neutral = Neutral()
        self.current: Action = self._neutral

    def log(self, fmt: str, *args, **kwargs):
        self.quest.logger(LogKind.SIM, fmt, *args, **kwargs)

    def to_neutral(self) -> None:
        self.current = self._neutral

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
