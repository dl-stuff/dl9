"""Set and run simulation"""


if __name__ == "__main__":
    from core.quest import Quest
    from entity.player import Player
    from core.constants import SimActKind
    from action import Action
    from core.timeline import Timer

    quest = Quest()
    player = Player(quest, None, None, None, None)
    action = Action(player, 711102, kind=SimActKind.SKILL, index=1)
    action.lv = 4
    action.start()
    timer = Timer(quest.timeline, 1.4, lambda: action.start())
    quest.timeline.run(10)