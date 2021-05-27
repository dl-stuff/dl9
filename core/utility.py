"""Math and other util functions"""
from ctypes import c_float
from entity import Entity
from typing import Any, Optional


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


class Gauge:
    __slots__ = ["current_value", "required_value", "maximum_value"]

    def __init__(self, current_value: Optional[int] = None, required_value: Optional[int] = None, maximum_value: Optional[int] = None) -> None:
        self.current_value: int = current_value or 0
        self.required_value: int = required_value or 0
        self.maximum_value: int = maximum_value or self.required_value

    def charge(self, value: int):
        self.current_value = max(min(self.current_value + value, self.maximum_value), 0)

    def charge_percent(self, percent: float):
        self.charge(cfloat_mult(self.required_value, percent))

    @property
    def value(self) -> int:
        return self.current_value

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


class HP:
    def __init__(self, entity: Entity):
        self.base_max = None
        self.current_value: float = float("inf")
        self.entity = entity
        self._max_mod_fn = None

    @property
    def maximum_value(self) -> int:
        if self._max_mod_fn is None or self.base_max is None:
            return self.base_max
        return cfloat_mult(self.base_max, self._max_mod_fn())

    def set_base_max(self, base_max: Optional[int]):
        self.base_max = base_max
        if self.base_max is None:
            self.current_value = float("inf")

    @property
    def value(self) -> float:
        return self.current_value

    def add(self, value: float):
        if self.base_max is None:
            return
        self.current_value = max(min(self.current_value + value, self.maximum_value), 0)

    def add_percent(self, percent: float):
        if self.base_max is None:
            return
        self.add(cfloat_mult(self.maximum_value, percent))

    def __repr__(self) -> str:
        if self.base_max is None:
            return "infinite"
        return "{}/{}".format(int(self.current_value), self.maximum_value)
