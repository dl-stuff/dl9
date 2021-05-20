import os
import json

from action.parts import *
from action.hits import *
from action.signal import *

PLAYER_ACTION_FMT = os.path.join(os.path.dirname(__file__), "data", "PlayerAction_{:08}.json")


class Action:
    def __init__(self, action_id: int) -> None:
        self._parts = []
        with open(PLAYER_ACTION_FMT.format(action_id), "r") as fn:
            for prt in json.load(fn):
                cmd = PartCmd(prt["commandType"])
                try:
                    self._parts.append(globals()[f"Part_{cmd.name}"](self, prt))
                except KeyError:
                    continue
