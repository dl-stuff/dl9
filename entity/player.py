"""A player character"""
from __future__ import annotations
from typing import Mapping, Optional, Sequence, NamedTuple, Tuple, Union

from core.database import FromDB
from core.quest import Quest
from core.timeline import EventManager
from core.log import LogKind
from core.constants import ElementalType, PlayerForm, Stat
from core.utility import cfloat_mult, Array, Gauge
from entity import Entity
from action import Action, Neutral


class PlayerConf(NamedTuple):
    adventurer: int
    dragon: int
    weapon: int
    wyrmprints: Sequence[int]


class Adventurer(FromDB, table="CharaData"):
    def __init__(self, id: int, player: Optional[Player] = None) -> None:
        super().__init__(id)
        if self._data:
            self.anim_ref = f'{self._data["_BaseId"]:06}{self._data["_VariationId"]:02}'
            self.element = ElementalType(self._data["_ElementalType"])
        else:
            self.anim_ref = None
            self.element = ElementalType.NONE


class Dragon(FromDB, table="DragonData"):
    def __init__(self, id: int, player: Optional[Player] = None) -> None:
        super().__init__(id)
        if self._data:
            if self._data["_AnimFileName"]:
                self.anim_ref = self._data["_AnimFileName"].replace("_", "")
            else:
                self.anim_ref = f'd{self._data["_BaseId"]}{self._data["_VariationId"]:02}'
            self.element = ElementalType(self._data["_ElementalType"])
        else:
            self.anim_ref = None
            self.element = ElementalType.NONE


class Weapon(FromDB, table="WeaponBody"):
    def __init__(self, id: int, player: Optional[Player] = None) -> None:
        super().__init__(id)


class Wyrmprint(FromDB, table="AbilityCrest"):
    def __init__(self, id: int) -> None:
        super().__init__(id)


class Wyrmprints:
    def __init__(self, id_list: Sequence[int]) -> None:
        self.wps = tuple((Wyrmprint(id) for id in id_list))


class Team:
    MAX_PLAYER = 4

    def __init__(self, quest: Quest) -> None:
        self.quest = quest
        self.events = EventManager()
        self.players = []
        self.quest.add_team(self)

    def add_player(self, player: Player):
        if len(self.players) < Team.MAX_PLAYER:
            self.players.append(player)
            self.events.add_child(player.events)


class SPManager:
    __slots__ = ["player", "name", "a", "d", "_mapping"]

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
                self._mapping[form][idx].charge_percent(value)
            valuestr = f"+{value:.0%}"
        else:
            spr_mod = 1 + self.player.modifiers.submod((Stat.Spr,))
            for form, idx in targets:
                self._mapping[form][idx].charge(cfloat_mult(value, spr_mod + self.player.modifiers.submod((Stat.Spr, idx))))
            valuestr = f"+{value}"

        if key is None:
            self.player.log("{}.SP {} {}", self.player.form.name, valuestr, self)
        else:
            self.player.log("{}.{}.SP s{} {}", key[0].name, key[1], valuestr, self)

    def __repr__(self) -> str:
        return "[ " + " | ".join((repr(self._mapping[form][idx]) for form, idx in self.targets())) + " ]"

    def __getitem__(self, key: Tuple[PlayerForm, int]) -> Gauge:
        form, idx = key
        return self._mapping[form][idx]


class Player(Entity):
    def __init__(self, quest: Quest, team: Team, conf: PlayerConf) -> None:
        super().__init__(quest)
        self.team = team

        self.sp = SPManager(self)

        self.adventurer = Adventurer(conf.adventurer)
        self.dragon = Dragon(conf.dragon)
        self.weapon = Weapon(conf.weapon)
        self.wyrmprints = Wyrmprints(conf.wyrmprints)

        # set hp here

        self.form = PlayerForm.ADV
        self._neutral = Neutral()
        self.current: Action = self._neutral

        self.quest.add_player(self)
        self.team.add_player(self)

    def log(self, fmt: str, *args, **kwargs):
        self.quest.logger(fmt, LogKind.SIM, *args, **kwargs)

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
