from __future__ import annotations

import dataclasses as dc
from typing import FrozenSet, Generic, Iterable, TypeVar

T = TypeVar("T", covariant=True)


@dc.dataclass(frozen=True)
class Split(Generic[T]):
    """
    A split of a set of items into two sets, a head and a tail.
    """

    head: FrozenSet[T]
    tail: FrozenSet[T]

    def __str__(self) -> str:
        head_str = "{" + ", ".join(map(str, self.head)) + "}"
        tail_str = "{" + ", ".join(map(str, self.tail)) + "}"
        return f"CondorcetSplit(head={head_str}, tail={tail_str})"

    @classmethod
    def of(cls, head: Iterable[T], tail: Iterable[T]) -> Split[T]:
        return cls(
            frozenset(head),
            frozenset(tail),
        )
