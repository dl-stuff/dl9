"""
kinds of modifiers

1. Ability Passive
- stat mods
- act damage up/down
- punisher

2. Action condtion (and Aura)
- there's a lot of crap here but they r all additive if same field
- str aura is same as _RateAttack
- certain fields (crit, crit dmg, punisher) are same bracket for w/e reason

3. hitattr
- independent from everything else
"""
from enum import Enum
from collections import defaultdict
from typing import Callable, Hashable, Optional


class Stat(Enum):
    NONE = 0
    Hp = 1
    Atk = 2
    Def = 3
    Spr = 4
    Dpr = 5
    Dummy1 = 6
    ChargeTime = 7
    DragonTime = 8
    DamageCut = 9
    AttackSpeed = 10
    BurstSpeed = 11
    ChargeSpeed = 12
    ConsumeDpRate = 13
    FinalDragonTimeRate = 14
    Utpr = 15
    DamageCutB = 16


class Modifier:
    def __init__(self, value: float, bracket: Hashable, active: Optional[Callable] = None) -> None:
        self._value = value
        self.bracket = bracket
        self.active = active

    def __float__(self) -> float:
        if self.active is None:
            return self._value
        return self.active() * self._value

    def __repr__(self) -> str:
        return f"{self.bracket}: {self._value} ({self.active})"


class ModifierDict(defaultdict):
    def __init__(self) -> None:
        super().__init__(list)

    def add(self, mod: Modifier):
        self[mod.bracket].append(mod)

    def mod(self, bracket: Hashable) -> float:
        try:
            return sum(map(float, self.get(bracket)))
        except TypeError:
            return 0
