"""A player character"""
from __future__ import annotations
from functools import total_ordering  # default once 3.10
from typing import Optional, Sequence, NamedTuple, Tuple

from core.database import FromDB
from core.quest import Quest
from core.modifier import ModifierDict, Stat
from core.timeline import EventManager
from core.log import LogKind
from core.utility import cfloat_mult
from action import Action


class PlayerConf(NamedTuple):
    adventurer: int
    dragon: int
    weapon: int
    wyrmprints: Sequence[int]


class Adventurer(FromDB, table="CharaData"):
    def __init__(self, id: str, player: Optional[Player] = None) -> None:
        super().__init__(id)

    def edit_skill(self):
        pass

    def ex_abiility(self):
        pass


class Dragon(FromDB, table="DragonData"):
    def __init__(self, id: str, player: Optional[Player] = None) -> None:
        super().__init__(id)


class Weapon(FromDB, table="WeaponBody"):
    def __init__(self, id: str, player: Optional[Player] = None) -> None:
        super().__init__(id)


class Wyrmprint(FromDB, table="AbilityCrest"):
    def __init__(self, id: str, player: Optional[Player] = None) -> None:
        super().__init__(id)


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


class PlayerForm:
    ADV = "c"
    DRG = "d"


class SP:
    __slots__ = ["current_value", "required_value", "maximum_value"]

    def __init__(self) -> None:
        self.current_value: int = 0
        self.required_value: int = 0
        self.maximum_value: int = 0

    def charge(self, value: int):
        self.current_value = max(min(self.current_value + value, self.maximum_value), 0)

    @property
    def count(self):
        return self.current_value // self.required_value

    def __repr__(self) -> str:
        if self.required_value == self.maximum_value:
            return "{}/{}".format(self.current_value, self.required_value)
        return "{}/{} [{}]".format(self.current_value, self.maximum_value, self.count)

    def __bool__(self) -> bool:
        return self.current_value >= self.required_value

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

        self.a = (SP(), SP(), SP(), SP())
        self.d = (SP(), SP())
        self._mapping = {PlayerForm.ADV: self.a, PlayerForm.DRG: self.d}

    def targets(self):
        if self.player.form == PlayerForm.ADV:
            return ((PlayerForm.ADV, i) for i in range(0, 4))
        else:
            return ((PlayerForm.DRG, i) for i in range(0, 2))

    def charge(self, value: int, key: Optional[Tuple[PlayerForm, int]] = None):
        if key is None:
            targets = self.targets()
        else:
            targets = (key,)

        spr_mod = 1 + self.player.modifiers.mod(Stat.Spr)

        for form, idx in targets:
            self._mapping[form][idx].charge(cfloat_mult(value, spr_mod + self.player.modifiers.mod((Stat.Spr, idx))))

    def __repr__(self) -> str:
        return "[ " + " | ".join((repr(self._mapping[form][idx]) for form, idx in self.targets())) + " ]"

    def __getitem__(self, key: Tuple[PlayerForm, int]) -> SP:
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
        self.wyrmprints = tuple((Wyrmprint(wp) for wp in conf.wyrmprints))

        self.form = PlayerForm.ADV
        self.current: Action = None

    def log(self, *args, **kwargs):
        self.quest.logger(LogKind.SIM, *args, **kwargs)

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
