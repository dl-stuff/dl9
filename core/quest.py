"""A quest with a timeline and some event managers"""

from core.timeline import Timeline, EventManager


class Quest:
    def __init__(self) -> None:
        self.timeline = Timeline()
        self.events = EventManager()
