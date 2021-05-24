from core.quest import Quest


class Enemy:
    def __init__(self, quest: Quest) -> None:
        self.quest = quest
