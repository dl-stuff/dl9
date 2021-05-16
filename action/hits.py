"""Action parts that deal with hits and bullets"""
import re
from typing import Mapping

from action.parts import Part, PartCmd

LV_PATTERN = re.compile(r"_LV\d{2}")


class HitAttribute(Part, pcmd=PartCmd.HIT_ATTRIBUTE):
    def __init__(self, data: Mapping) -> None:
        super().__init__(data)
        self.label = data["_hitLabel"]
        self.generic = LV_PATTERN.sub("_LV{lv:02}", self.label)
