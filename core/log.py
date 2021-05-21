"""Simulation logs"""
from __future__ import annotations  # default once 3.10
import sys
from enum import Enum
from typing import Hashable, Type, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from core.timeline import Timeline


class LogKind(Enum):
    DEBUG = -1
    SIM = 0
    ACT = 1
    THINK = 2
    SIG = 3


class Logger:
    PRINT_ASAP = True

    def __init__(self, timeline: Timeline):
        self._timeline = timeline

    def reset(self):
        self._entries = []
        self._damage_by_bracket = {}
        self._damage_by_time = {}

    def __call__(self, entrycls: Type, *args, **kwargs) -> None:
        entry = entrycls(self._timeline.now, *args, **kwargs)
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

    def __init_subclass__(cls, kind: LogKind = LogKind.DEBUG, fmt: str = "") -> None:
        cls._kind = kind
        cls._fmt = "{ts:>8.3f}:{kind:>5}| " + fmt

    def __init__(self, timestamp: float) -> None:
        self._timestamp = timestamp

    def fmt(self, *args, **kwargs) -> str:
        """Format this line of log"""
        return self._fmt.format(kind=self._kind.name, ts=self._timestamp, *args, **kwargs)

    def process(self, logger: Logger) -> None:
        """Does any kind of updates to logger"""
        pass


class DebugLog(LogEntry, kind=LogKind.DEBUG, fmt="{debug}"):
    """Generic debug log"""

    def __init__(self, timestamp: float, *args) -> None:
        super().__init__(timestamp)
        self.debug = args

    def fmt(self) -> str:
        """Format this line of log"""
        return super().fmt(debug=self.debug)


class DamageLog(LogEntry, kind=LogKind.SIM, fmt="{src}, {dmg:<8.3f}, {bracket}"):
    def __init__(self, timestamp: float, bracket: Hashable, src: Hashable, dmg: float) -> None:
        super().__init__(timestamp)
        self._src = src
        self._dmg = dmg
        self._bracket = bracket

    def fmt(self):
        return super().fmt(src=self._src, dmg=self._dmg, bracket=self._bracket)

    def process(self, logger: Logger) -> None:
        if not self._bracket in logger._damage_by_bracket:
            logger._damage_by_bracket[self._bracket] = {}
        if not self._src in logger._damage_by_bracket[self._bracket]:
            logger._damage_by_bracket[self._bracket][self._src] = 0
        logger._damage_by_bracket[self._bracket][self._src] += self._dmg

        if self._timestamp in logger._damage_by_time:
            logger._damage_by_time[self._timestamp] += self._dmg
        else:
            logger._damage_by_time[self._timestamp] = self._dmg


class Loggable:
    """Extends class with function to take a Logger object"""

    def __init_subclass__(cls, entrycls: Type):
        cls._entrycls = entrycls

    @classmethod
    def bind_logger(cls, log: Logger) -> None:
        """Set the classwide logger instance"""
        cls._log = log

    def log(self, *args, **kwargs) -> None:
        """Wrapper for calling the logger"""
        try:
            self._log(self._entrycls, *args, **kwargs)
        except AttributeError:
            pass
