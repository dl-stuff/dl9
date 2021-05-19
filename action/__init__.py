from action.parts import *
from action.hits import *
from action.signal import *
from core.database import DBM


class Action:
    def __init__(self, action_id: int) -> None:
        self._parts = []
        for pidx in DBM.query_all("SELECT * FROM PartsIndex WHERE act=?", (action_id,)):
            try:
                print(pidx["part"], globals()[pidx["part"]])
            except KeyError:
                print(pidx["part"], "not found")
            print(tuple(pidx))


if __name__ == "__main__":
    Action(711102)