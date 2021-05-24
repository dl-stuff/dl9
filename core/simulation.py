"""Set and run simulation"""


if __name__ == "__main__":
    from core.quest import Quest
    from entity.player import Player, PlayerTeam
    from core.constants import SimActKind
    from action import Action

    quest = Quest()
    team = PlayerTeam(quest)
    player = Player(quest, team, None, None, None, None)
    action = Action(player, 711102, kind=SimActKind.SKILL, index=1)
    action.lv = 4
    action.start()
    timer = quest.timeline.schedule(1.4, lambda: action.start())
    quest.timeline.run(10)