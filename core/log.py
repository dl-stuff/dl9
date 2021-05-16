import sys
from enum import Enum
from typing import Any, Type


class LogKind(Enum):
    DEBUG = -1
    SIM = 0
    THINK = 1
    ACT = 2
    SIG = 3
    TIMER = 4


class Logger(list):
    PRINT_ASAP = True

    def __init__(self, timeline):
        self._timeline = timeline

    def __call__(self, entrycls: Type, *args, **kwargs) -> None:
        entry = entrycls(self._timeline.now, *args, **kwargs)
        if self.PRINT_ASAP:
            print(entry.fmt(), flush=True)
        self.append(entry)

    def write(self, output=sys.stdout):
        for entry in self:
            output.write(entry.fmt())
            output.write("\n")


class LogEntry:
    def __init_subclass__(cls, kind: LogKind = LogKind.DEBUG, fmt: str = "") -> None:
        cls._kind = kind
        cls._fmt = "{ts:>8.3f}:{kind:>5}| " + fmt

    def __init__(self, timestamp: float) -> None:
        self._timestamp = timestamp

    def fmt(self, *args, **kwargs) -> str:
        return self._fmt.format(kind=self._kind.name, ts=self._timestamp, *args, **kwargs)


class TimelineLog(LogEntry, kind=LogKind.TIMER, fmt="{}"):
    def __init__(self, timestamp: float, timer: object) -> None:
        super().__init__(timestamp)
        self._timer = timer

    def fmt(self):
        return super().fmt(self._timer)


class Loggable:
    """Extends class with function to take a Logger object"""

    def __init_subclass__(cls, entrycls: Type):
        cls._entrycls = entrycls

    @classmethod
    def bind_logger(cls, log) -> None:
        cls._log = log

    def log(self, *args, **kwargs) -> None:
        try:
            self._log(self._entrycls, *args, **kwargs)
        except AttributeError:
            pass