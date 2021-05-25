"""Set and run simulation"""


from core.quest import Quest
from entity.player import Player, PlayerTeam, PlayerConf


if __name__ == "__main__":

    quest = Quest()
    team = PlayerTeam(quest)
    conf = PlayerConf(
        adventurer=10350102,
        dragon=0,
        weapon=0,
        wyrmprints=(0, 0, 0, 0, 0, 0, 0),
    )
    player = Player(quest, team, conf)
