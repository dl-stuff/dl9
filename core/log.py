"""Simulation logs"""
from __future__ import annotations  # default once 3.10
import sys
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from core.timeline import Timeline


class Logger:
    PRINT_ASAP = True

    def __init__(self, timeline: Timeline):
        self._timeline = timeline
        self.reset()

    def reset(self):
        self._entries = []
        self._damage_by_bracket = {}
        self._damage_by_time = {}

    def __call__(self, *args, **kwargs) -> None:
        entry = LogEntry(self._timeline.now, *args, **kwargs)
        if self.PRINT_ASAP:
            print(entry.fmt(), flush=True)
        entry.process(self)
        self._entries.append(entry)

    def write(self, output=sys.stdout):
        for entry in self:
            output.write(entry.fmt())
            output.write("\n")


class LogEntry:
    """1 row in the log"""

    def __init__(self, timestamp: float, format: str, *args, **kwargs) -> None:
        self._timestamp = timestamp
        self._format = "{ts:>8.3f}| " + format
        self._args = args
        self._kwargs = kwargs

    def fmt(self) -> str:
        """Format this line of log"""
        return self._format.format(ts=self._timestamp, *self._args, **self._kwargs)

    def process(self, logger: Logger) -> None:
        """Does any kind of updates to logger"""
        pass
