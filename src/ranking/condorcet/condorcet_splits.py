from __future__ import annotations
import dataclasses as dc
from typing import FrozenSet, Iterable, Iterator, TypeVar

from ranking.dtypes.split import Split


T = TypeVar("T", covariant=True)


@dc.dataclass(frozen=True)
class CondorcetSplits(Iterable[Split[T]]):
    r"""
    A set of CondorcetSplits, each having the same Condorcet cost.

    For a given Condorcet matrix $M$, the cost of a pair $(i, j)$ if the items is
    $\max(0, -M_{ij}) = \max(0, M_{ji})$. It is the Condorcet penalty of ranking $i$
    ahead of $j$.

    The cost of a split is the sum of the costs over the Cartesian product of the
    head and tail of the split.
    """

    cost: float
    splits: FrozenSet[Split[T]]

    def __str__(self) -> str:
        splits_str = "{" + ", ".join(map(str, self.splits)) + "}"
        return f"CondorcetSplits(cost={self.cost}, splits={splits_str})"

    def __len__(self) -> int:
        return len(self.splits)

    def __iter__(self) -> Iterator[Split[T]]:
        return iter(self.splits)

    @classmethod
    def of_tails(
        cls, cost: float, tails: Iterable[Iterable[T]], items: Iterable[T]
    ) -> CondorcetSplits[T]:
        items_set = set(items)
        return CondorcetSplits(
            cost,
            frozenset(
                Split[T].of(items_set - set(tail), tail) for tail in tails
            ),
        )