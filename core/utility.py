"""Math and other util functions"""
from entity.enemy import Enemy
from entity.player import Player
from action.parts import HitAttribute
from ctypes import c_float
import sqlite3
from core.modifier import ModifierDict
from core.constants import SimActKind


def float_ceil(a: float, b: float) -> int:
    c_float_value = c_float(c_float(a).value * c_float(b).value).value
    int_value = int(c_float_value)
    return int_value if int_value == c_float_value else int_value + 1


def damage_formula(hitattr: HitAttribute, player: Player, enemy: Enemy):
    pass
