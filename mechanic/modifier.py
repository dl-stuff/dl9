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
from collections import defaultdict
from functools import reduce
from itertools import chain
import itertools
from typing import Callable, Dict, Hashable, List, Sequence, Tuple, Optional, TYPE_CHECKING, Set
import operator

if TYPE_CHECKING:
    from action import Action


class Modifier:
    __slots__ = ["_value", "bracket", "status", "_active_fn"]

    def __init__(self, value: float, bracket: Tuple[Hashable, ...], active_fn: Optional[Callable] = None, status: bool = True) -> None:
        self._value = value
        self.bracket = bracket
        self.status = status
        self._active_fn = active_fn

    def get(self, *args, **kwargs) -> float:
        if not self.status:
            return 0.0
        if self._active_fn is None:
            return self._value
        if args or kwargs:
            try:
                return self._active_fn(*args, **kwargs) * self._value
            except KeyError:
                pass
        return self._active_fn() * self._value

    def __float__(self) -> float:
        return self.get()

    def __repr__(self) -> str:
        return f"{self.bracket}: {self._value} ({self._active_fn})"


class ModifierDict:
    __slots__ = ["_mods", "_tags", "action"]

    def __init__(self) -> None:
        self._mods: Dict[Tuple[Hashable, ...], List[Modifier]] = defaultdict(list)
        self._tags: Dict[Tuple[Hashable, ...], Set[Tuple[Hashable, ...]]] = defaultdict(set)

    def add(self, mod: Modifier) -> None:
        self._mods[mod.bracket].append(mod)
        for i in range(1, len(mod.bracket) + 1):
            self._tags[mod.bracket[0:i]].add(mod.bracket)

    def get(self, bracket: Tuple[Hashable, ...], specific: bool = False, *args, **kwargs) -> Sequence[Modifier]:
        if specific:
            return self._mods.get(bracket, [])
        return chain(*(self._mods.get(tag, []) for tag in self._tags.get(bracket)))

    def mod(self, bracket: Tuple[Hashable, ...], op: Callable = operator.add, initial: float = 0, specific: bool = False, *args, **kwargs) -> float:
        try:
            return initial + reduce(op, [mod.get(*args, **kwargs), self.get(bracket, specific=specific)])
        except TypeError:
            return initial


# class MDMultiLevel(ModifierDict):
#     def __init__(self) -> None:
#         self._subdict = {}
#         self._mods = []

#     def add(self, mod: Modifier, seq: int = 0):
#         if seq >= len(mod.bracket):
#             self._mods.append(mod)
#         else:
#             tag = mod.bracket[seq]
#             try:
#                 sub_md = self._subdict[tag]
#             except KeyError:
#                 sub_md = MDMultiLevel()
#                 self._subdict[tag] = sub_md
#             sub_md.add(mod, seq=seq + 1)

#     def get(self, bracket: Tuple[Hashable, ...], seq: int = 0):
#         if seq >= len(bracket):
#             all_mods = []
#             all_mods.extend(self._mods)
#             for sub_md in self._subdict.values():
#                 all_mods.extend(sub_md.get(bracket, seq=seq + 1))
#             return all_mods
#         else:
#             tag = bracket[seq]
#             try:
#                 return self._subdict[tag].get(bracket, seq=seq + 1)
#             except KeyError:
#                 return []


# class MDTagged(ModifierDict):
#     def __init__(self) -> None:
#         self._mods = defaultdict(list)
#         self._tags = defaultdict(set)

#     def add(self, mod: Modifier):
#         self._mods[mod.bracket].append(mod)
#         for i in range(1, len(mod.bracket) + 1):
#             self._tags[mod.bracket[0:i]].add(mod.bracket)

#     def get(self, bracket: Tuple[Hashable, ...]):
#         all_mods = []
#         try:
#             for tag in self._tags.get(bracket):
#                 all_mods.extend(self._mods[tag])
#         except TypeError:
#             pass
#         return all_mods


if __name__ == "__main__":
    from core.constants import Stat
    import random
    from pprint import pprint

    stat_lst = list(Stat)
    randomized_mods = []
    spr_mods = []
    modcount = 100
    counts = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
    }
    for i in range(modcount):
        bracket_len = random.choice((1, 2, 3, 4))
        counts[bracket_len] += 1
        stat = random.choice(stat_lst)
        if bracket_len == 1:
            bracket = (stat,)
        elif bracket_len == 2:
            bracket = (stat, random.choice(("Passive", "Buff")))
        elif bracket_len == 3:
            bracket = (stat, random.choice(("Passive", "Buff")), "EX")
        elif bracket_len == 4:
            bracket = (stat, random.choice(("Passive", "Buff")), "test", "speshul")
        mod = Modifier(random.random(), bracket)
        if stat == Stat.Spr:
            spr_mods.append(mod)
        randomized_mods.append(mod)

    # accuracy
    spr = reduce(operator.add, map(float, spr_mods))
    print(f"Real {spr}")
    md = ModifierDict()
    for mod in randomized_mods:
        md.add(mod)
    res = md.mod((Stat.Spr,))
    print(f"Check {ModifierDict.__name__}: {res}")
    print(flush=True)

    # for MD in (MDMultiLevel, MDTagged):
    #     md = MD()
    #     for mod in randomized_mods:
    #         md.add(mod)
    #     res = md.mod((Stat.Spr,))
    #     print(f"Check {MD.__name__}: {res}")
    #     # pprint(md.get((Stat.Spr,)))
    #     if res != spr:
    #         for mod in md.get((Stat.Spr,)):
    #             if mod not in spr_mods:
    #                 print(f"ERROR - wrong mod value {res} != {spr}")
    #                 print("Reason", mod)
    #     print(flush=True)

#     from time import monotonic

#     trials = 100000
#     print(f"{trials} trials with {modcount} mods")
#     print(counts)
#     for MD in (MDMultiLevel, MDTagged):
#         print(f"Testing {MD.__name__}")
#         start_t = monotonic()
#         for i in range(1000):
#             md = MD()
#             for mod in randomized_mods:
#                 md.add(mod)
#         print(f"Adding: {monotonic() - start_t}s")
#         start_t = monotonic()
#         for i in range(trials):
#             md.mod((random.choice(stat_lst),))
#         print(f"Getting 1: {monotonic() - start_t}s")
#         start_t = monotonic()
#         for i in range(trials):
#             md.mod((random.choice(stat_lst), random.choice(("Passive", "Buff"))))
#         print(f"Getting 2: {monotonic() - start_t}s")
#         start_t = monotonic()
#         for i in range(trials):
#             md.mod((random.choice(stat_lst), random.choice(("Passive", "Buff")), "EX"))
#         print(f"Getting 3: {monotonic() - start_t}s")
#         start_t = monotonic()
#         for i in range(trials):
#             md.mod((random.choice(stat_lst), random.choice(("Passive", "Buff")), "test", "speshul"))
#         print(f"Getting 4: {monotonic() - start_t}s")
#         print(flush=True)
