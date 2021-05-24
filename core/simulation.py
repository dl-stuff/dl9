"""Set and run simulation"""


from entity.player import PlayerForm
from action.skill import SkillCtx


if __name__ == "__main__":
    from core.quest import Quest
    from entity.player import Player, PlayerTeam, PlayerConf
    from action.skill import Skill

    quest = Quest()
    team = PlayerTeam(quest)
    conf = PlayerConf(
        adventurer=0,
        dragon=0,
        weapon=0,
        wyrmprints=(0, 0, 0, 0, 0, 0, 0),
    )
    player = Player(quest, team, conf)
    skill = Skill(107301011, player, level=4, form=PlayerForm.ADV, index=1, context=SkillCtx.OWN)
    player.sp.charge(6000)
    print(player.sp)
    skill.cast()
    quest.timeline.run(10)
