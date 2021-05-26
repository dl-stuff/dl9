"""Set and run simulation"""


from core.constants import PlayerForm
from core.quest import Quest
from entity.player import Player, PlayerTeam, PlayerConf
from action.skill import Skill, SkillCtx


if __name__ == "__main__":

    quest = Quest()
    team = PlayerTeam(quest)
    conf = PlayerConf(
        adventurer=10730101,
        dragon=0,
        weapon=0,
        wyrmprints=(0, 0, 0, 0, 0, 0, 0),
    )
    player = Player(quest, team, conf)
    s1 = Skill(107301011, player, level=4, form=PlayerForm.ADV, index=1, context=SkillCtx.OWN)
    player.sp.charge(1, key=PlayerForm.ADV, percent=True)
    s1.cast()
    quest.timeline.run(10)
