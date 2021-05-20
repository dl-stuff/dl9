from action.parts import *
from action.hits import *
from action.signal import *
from core.database import DBM
import json


class Action:
    def __init__(self, action_id: int) -> None:
        # self._parts = []
        # for pidx in DBM.query_all("SELECT pk, act, seq, part FROM PartsIndex WHERE act=?", (action_id,)):
        #     try:
        #         part_class = globals()[pidx["part"]]
        #         part_data = DBM.query_one(f"SELECT * FROM {pidx['part']} WHERE pk=?", (pidx["pk"],))
        #         self._parts.append(part_class(part_data))
        #     except KeyError:
        #         continue
        with open("./action/PlayerAction_00711102.json", "r") as fn:
            for prt in json.load(fn):
                Part(prt)
        # print(self._parts)


if __name__ == "__main__":
    for _ in range(10000):
        Action(711102)
