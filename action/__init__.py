from action.parts import *
from action.hits import *
from action.signal import *

PART_CLS = {
    PartCmd.HIT_ATTRIBUTE: HitAttribute,
    PartCmd.ACTIVE_CANCEL: ActiveCancel,
    PartCmd.SEND_SIGNAL: SendSignal,
}


class Action:
    def __init__(self, action_id) -> None:
        self._parts = []
        with open(PLAYER_ACTION_FMT.format(action_id), "r") as fn:
            for data in json.load(fn, parse_float=float, parse_int=int):
                try:
                    self._parts.append(PART_CLS[PartCmd(data["commandType"])](data))
                except KeyError:
                    pass
        self._parts = sorted(self._parts, key=lambda p: p.seconds)
        for pt in self._parts:
            print(pt)
