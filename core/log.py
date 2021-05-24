"""Simulation logs"""
from __future__ import annotations  # default once 3.10
import sys
from enum import Enum
from typing import Type, TYPE_CHECKING

if TYPE_CHECKING:
    from core.timeline import Timeline


class LogKind(Enum):
    DEBUG = 0
    SIM = 1


class LogData:
    pass


class Logger:
    __slots__ = ["_timeline", "_entries", "_data"]
    PRINT_ASAP = True

    def __init__(self, timeline: Timeline):
        self._timeline = timeline
        self.reset()

    def reset(self):
        self._entries = []
        self._data = LogData()

    def __call__(self, kind: LogKind, format: str, *args, **kwargs) -> None:
        entry = LogEntry(self._timeline.now, kind, format, *args, **kwargs)
        if self.PRINT_ASAP:
            print(entry.fmt(), flush=True)
        entry.process(self._data)
        self._entries.append(entry)

    def write(self, output=sys.stdout):
        for entry in self:
            output.write(entry.fmt())
            output.write("\n")


class LogEntry:
    """1 row in the log"""

    __slots__ = ["_timestamp", "_kind", "_fmt", "_args", "_kwargs"]

    def __init__(self, timestamp: float, kind: LogKind, fmt: str, *args, **kwargs) -> None:
        self._timestamp = timestamp
        self._kind = kind
        self._fmt = "{ts:>8.3f}{kind:>6}| " + fmt
        self._args = args
        self._kwargs = kwargs

    def fmt(self) -> str:
        """Format this line of log"""
        return self._fmt.format(ts=self._timestamp, kind=self._kind.name, *self._args, **self._kwargs)

    def process(self, data: LogData) -> None:
        """Does any kind of updates to log data"""
        pass
