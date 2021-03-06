"""Timeline and Events"""
from __future__ import annotations
from enum import Enum  # default once 3.10
import heapq
from collections.abc import Callable
from functools import total_ordering
from typing import Any, Mapping, MutableMapping, MutableSequence, Optional, Hashable

from core.constants import GLOBAL, EventOrder, ForceTimelineEnd


class Timeline:
    __slots__ = ["name", "_head", "_heap"]
    TIMEOUT = "timeout"
    ACT_END = "act end"

    def __init__(self, name: str = GLOBAL) -> None:
        """Wrapper for heapq that represents a timeline"""
        self.name = name
        self.reset()

    def reset(self):
        self._head = 0.0
        self._heap = []

    @property
    def now(self) -> float:
        """The current time of timeline process"""
        return self._head

    def schedule(self, timeout: float, callback: Optional[Callable] = None, repeat: bool = False, name: Optional[str] = None):
        return Timer(self, timeout, callback=callback, repeat=repeat, name=name)

    def push(self, item: Timer) -> None:
        """Push to heap"""
        heapq.heappush(self._heap, item)

    def pop(self) -> Any:
        """Pop lowest from heap"""
        return heapq.heappop(self._heap)

    def run(self, end: float) -> str:
        """Process all added timers, until heap is empty or end time is reached, return end reason"""
        try:
            while self._heap and self._head < end:
                ntimer = self.pop()
                if ntimer.status:
                    self._head = float(ntimer)
                    ntimer.proc()
            if self._head < end:
                return Timeline.TIMEOUT
            if not self._heap:
                return Timeline.ACT_END
        except ForceTimelineEnd as e:
            return str(e)


@total_ordering
class Timer:
    __slots__ = ["name", "_start", "_timeline", "_timeout", "_callback", "_repeat"]

    def __init__(self, timeline: Timeline, timeout: float, callback: Optional[Callable] = None, repeat: bool = False, name: Optional[str] = None) -> None:
        """Triggers given callback when timeout"""
        self.name = name or self.__class__.__name__
        self._start = None
        self._timeline = timeline
        self._timeout = timeout
        self._callback = callback
        self._repeat = repeat

    def __eq__(self, other: Timer) -> bool:
        return float(self) == float(other)

    def __lt__(self, other: Timer) -> bool:
        return float(self) < float(other)

    def __float__(self) -> float:
        if self._start is None:
            return float("inf")
        else:
            return self._start + self._timeout

    def __str__(self) -> str:
        return f"{self.name}({self._start}, {self._timeout}, {self._callback})"

    @property
    def status(self) -> bool:
        """Whether this timer is active"""
        return self._start is not None

    def __bool__(self) -> bool:
        return self.status

    @property
    def timeleft(self) -> float:
        if self._start is None:
            return 0.0
        else:
            return self._start + self._timeout - self._timeline.now

    @property
    def elapsed(self) -> float:
        if self._start is None:
            return 0.0
        else:
            return self._timeline.now - self._start

    def start(self) -> None:
        """Add timer to timeline"""
        if not self.status:
            self._start = self._timeline.now
            self._timeline.push(self)

    def end(self, callback: bool = False) -> None:
        """End the timer, and optionally trigger the callback"""
        if self.status:
            if callback and self._callback:
                self._callback()
            self._start = None

    def extend(self, add_time: float) -> None:
        """Extend timeout of this timer"""
        self._timeout += add_time

    def proc(self) -> None:
        """Process timer end callback"""
        self.end(callback=True)
        if self._repeat:
            self.start()


class Event:
    __slots__ = ["_key"]

    def __init__(self, key: Hashable) -> None:
        """Hashable event"""
        self._key = key

    def __hash__(self):
        return hash(self._key)

    def __eq__(self, other: Any) -> bool:
        try:
            return self._key == other._key
        except AttributeError:
            return self._key == other

    def __ne__(self, other: Any):
        return self != other


class EventManager:
    __slots__ = ["group", "_events", "_children"]

    def __init__(self) -> None:
        """Manager for events and callbacks"""
        self._events: MutableMapping[Hashable, MutableMapping[EventOrder, MutableSequence[Callable]]] = {}
        self._children: MutableSequence[EventManager] = []

    def add_child(self, child: EventManager):
        self._children.append(child)

    def listen(self, event: Hashable, callback: Callable, order: EventOrder = EventOrder.DURING):
        """Add new listener to a event"""
        try:
            self._events[event][order].append(callback)
        except KeyError:
            self._events[event] = ([], [], [])
            self._events[event][order].append(callback)

    def announce(self, event: Hashable, *args, **kwargs):
        """Notify all listeners of the event"""
        for cb_list in self._events[event]:
            for callback in cb_list:
                callback(*args, **kwargs)
        for child in self._children:
            child.announce(event, *args, **kwargs)
