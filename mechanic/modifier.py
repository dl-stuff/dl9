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
from typing import Callable, Hashable, Tuple, Optional


class Modifier:
    def __init__(self, value: float, bracket: Tuple[Hashable, ...], active: Optional[Callable] = None) -> None:
        self._value = value
        self.bracket = bracket
        self.active = active

    def __float__(self) -> float:
        if self.active is None:
            return self._value
        return self.active() * self._value

    def __repr__(self) -> str:
        return f"{self.bracket}: {self._value} ({self.active})"


class ModifierDict:
    def __init__(self) -> None:
        self._mods = defaultdict(list)
        self._categorized = defaultdict(list)

    def add(self, mod: Modifier):
        self._mods[mod.bracket].append(mod)
        self._categorized[mod.bracket[0]].append(mod.bracket)

    def submod(self, bracket: Tuple[Hashable, ...]) -> float:
        try:
            return sum(map(float, self._mods.get(bracket)))
        except TypeError:
            return 0.0

    def mod(self, category: Hashable) -> float:
        try:
            return 1 + sum(map(self.submod, self._categorized.get(category)))
        except TypeError:
            return 0.0
