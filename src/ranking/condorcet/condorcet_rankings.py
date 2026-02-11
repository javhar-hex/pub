from __future__ import annotations

import dataclasses as dc
from collections.abc import Iterable, Iterator, Sequence
from typing import FrozenSet, TypeVar

from ranking.dtypes.ranking import Ranking


T = TypeVar("T", covariant=True)


@dc.dataclass(frozen=True)
class CondorcetRankings(Iterable[Ranking[T]]):
    r"""
    A set of CondorcetRankings, where each ranking has the same Condorcet cost.

    For a given Condorcet matrix $M$, the cost of a pair $(i, j)$ if the items is
    $\max(0, -M_{ij}) = \max(0, M_{ji})$. It is the Condorcet penalty of ranking $i$
    ahead of $j$.

    The cost of a ranking is the sum of the costs over all ordered pairs in the ranking.

    If `is_truncated` is True, then there exist more rankings with the same cost; if
    not, then this list is complete.
    """

    cost: float
    rankings: FrozenSet[Ranking[T]]
    is_truncated: bool

    def __str__(self) -> str:
        rankings_str = "{" + ", ".join(map(str, self.rankings)) + "}"
        return (
            f"CondorcetRankings(cost={self.cost}, "
            f"rankings={rankings_str}, "
            f"is_truncated={self.is_truncated})"
        )

    def __len__(self) -> int:
        return len(self.rankings)

    def __iter__(self) -> Iterator[Ranking[T]]:
        return iter(self.rankings)

    @classmethod
    def of(
        cls, cost: float, rankings: Iterable[Sequence[T]], is_truncated: bool
    ) -> CondorcetRankings[T]:
        return cls(
            cost,
            frozenset(Ranking[T].of(ranking) for ranking in rankings),
            is_truncated,
        )
