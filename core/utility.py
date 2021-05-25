"""Math and other util functions"""
from ctypes import c_float
from typing import Any


def cfloat_mult(a: float, b: float) -> int:
    c_float_value = c_float(c_float(a).value * c_float(b).value).value
    int_value = int(c_float_value)
    return int_value if int_value == c_float_value else int_value + 1


class Array(list):
    """1-indexed list"""

    def __init__(self, *init) -> None:
        super().__init__(init)

    def __getitem__(self, i: int) -> Any:
        return super().__getitem__(i - 1)

    def __setitem__(self, i: int, value: Any):
        return super().__setitem__(i - 1, value)

    def enumerate(self):
        for idx, value in enumerate(self):
            yield idx + 1, value