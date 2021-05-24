"""Math and other util functions"""
from ctypes import c_float


def cfloat_mult(a: float, b: float) -> int:
    c_float_value = c_float(c_float(a).value * c_float(b).value).value
    int_value = int(c_float_value)
    return int_value if int_value == c_float_value else int_value + 1
