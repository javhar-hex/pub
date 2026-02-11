from __future__ import annotations

import dataclasses as dc
from typing import Sequence, Tuple, TypeVar, overload

T = TypeVar("T", covariant=True)


@dc.dataclass(frozen=True)
class Ranking(Sequence[T]):
    """
    A ranking of items, which is just a permutation of the items.
    """

    items: Tuple[T, ...]

    def __str__(self) -> str:
        items_str: str = ", ".join(map(str, self.items))
        return f"CondorcetRanking({items_str})"

    def __len__(self) -> int:
        return len(self.items)

    @overload
    def __getitem__(self, idx: int) -> T: ...
    @overload
    def __getitem__(self, idx: slice) -> tuple[T, ...]: ...
    def __getitem__(self, idx: int | slice) -> T | tuple[T, ...]:
        return self.items[idx]

    @classmethod
    def of(cls, items: Sequence[T]) -> Ranking[T]:
        return cls(tuple(items))
