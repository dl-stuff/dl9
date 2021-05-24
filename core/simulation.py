"""Set and run simulation"""


from entity.player import PlayerForm
from core.quest import Quest
from entity.player import Player, PlayerTeam, PlayerConf
from entity.skill import Skill, SkillCtx
from entity.ability import Ability


if __name__ == "__main__":

    quest = Quest()
    team = PlayerTeam(quest)
    conf = PlayerConf(
        adventurer=0,
        dragon=0,
        weapon=0,
        wyrmprints=(0, 0, 0, 0, 0, 0, 0),
    )
    player = Player(quest, team, conf)
    ab = Ability(676, player)
    ab.activate()
    print(ab)
    # s1 = Skill(107301011, player, level=4, form=PlayerForm.ADV, index=1, context=SkillCtx.OWN)
    # s2 = Skill(107301012, player, level=3, form=PlayerForm.ADV, index=2, context=SkillCtx.OWN)
    # player.sp.charge(6000, key=PlayerForm.ADV)
    # s1.cast()
    # quest.timeline.schedule(1.4, s2.cast).start()
    # quest.timeline.run(10)
