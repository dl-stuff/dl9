"""A quest with a timeline and some event managers"""

from core.timeline import Timeline, EventManager
from core.log import Logger


class Quest:
    __slots__ = ["timeline", "events", "logger"]

    def __init__(self) -> None:
        self.timeline = Timeline()
        self.events = EventManager()
        self.logger = Logger(self.timeline)
