"""Handles RNG"""
import random
from typing import Sequence


RNG = True


def choice(sequence: Sequence):
    if RNG:
        return random.choice(sequence)
    return sequence[0]
