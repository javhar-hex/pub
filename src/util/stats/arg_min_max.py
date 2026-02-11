from __future__ import annotations
from typing import Generic, List, Optional, Self, Tuple, TypeVar

from util.dtypes.comparable import Comparable
import dataclasses as dc

Arg = TypeVar("Arg")
Val = TypeVar("Val", bound=Comparable)


@dc.dataclass(frozen=True)
class ArgMinMax(Generic[Arg, Val]):
    "Immutable snapshot of extrema and their arguments."
    min: Optional[Val]
    max: Optional[Val]
    argmin: Tuple[Arg, ...]
    argmax: Tuple[Arg, ...]


class ArgMinMaxAccumulator(Generic[Arg, Val]):
    """
    Streaming accumulator. Call .snapshot() to get an ArgMinMax.
    """

    def __init__(self):
        self._min: Optional[Val] = None
        self._max: Optional[Val] = None
        self._argmin: List[Arg] = []
        self._argmax: List[Arg] = []

    def process(self, item: Arg, value: Val) -> Self:
        """Ingest one (item, value)."""
        if self._min is None or value < self._min:
            self._min, self._argmin = value, [item]
        elif value == self._min:
            self._argmin.append(item)

        if self._max is None or value > self._max:
            self._max, self._argmax = value, [item]
        elif value == self._max:
            self._argmax.append(item)

        return self

    def snapshot(self) -> ArgMinMax[Arg, Val]:
        """Immutable snapshot of current min, max, argmin, argmax."""
        return ArgMinMax(self._min, self._max, tuple(self._argmin), tuple(self._argmax))
