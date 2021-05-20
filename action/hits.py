"""Action parts that deal with hits and bullets"""
import re

from action.parts import Part, PartCmd
from typing import Mapping

LV_PATTERN = re.compile(r"_LV\d{2}")


class Part_HIT_ATTRIBUTE(Part):
    def __init__(self, data: Mapping) -> None:
        super().__init__(data)
        self.label = data["_hitLabel"]
        self.generic = LV_PATTERN.sub("_LV{lv:02}", self.label)
