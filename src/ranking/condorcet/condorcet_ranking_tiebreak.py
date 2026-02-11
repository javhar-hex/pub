from __future__ import annotations

import dataclasses as dc
from typing import Generic, TypeVar

from immutables import Map

from ranking.condorcet.condorcet_matrix import CondorcetMatrix
from ranking.condorcet.condorcet_tiebreak_score import CondorcetTieBreakScore
from ranking.dtypes.ranking import Ranking
from ranking.condorcet.condorcet_rankings import CondorcetRankings
from util.stats.arg_min_max import ArgMinMaxAccumulator

T = TypeVar("T")


@dc.dataclass(frozen=True)
class CondorcetRankingTieBreak(Generic[T]):
    """
    Container for the results of a tiebreaker investigation into a collection of
    rankings under a given Condorcet matrix $M$. Stores a map from the ranking to its
    `CondorcetTieBreakScore`. The latter contains the Kemeny and Borda scores and
    counts.

    To contruct this object, use the `of()` factory classmethod. The field
    `is_truncated` is carried over from the `CondorcetRankings` object supplied as
    argument to the factory method.
    """

    scores: Map[Ranking[T], CondorcetTieBreakScore]
    is_truncated: bool

    def optimum(self) -> CondorcetRankings[T]:
        """
        Optimum rankings among the rankings contained in the `scores` map. The
        optimum is determined as the argmin of the tiebreak scores in the map. The
        optimum can still consist of multiple rankings.
        """
        acc = ArgMinMaxAccumulator[Ranking[T], CondorcetTieBreakScore]()
        for ranking, tiebreak_score in self.scores.items():
            acc.process(ranking, tiebreak_score)
        snapshot = acc.snapshot()
        if snapshot.min is None:
            raise ValueError("No rankings provided.")
        return CondorcetRankings[T].of(
            cost=snapshot.min.kemeny,
            rankings=snapshot.argmin,
            is_truncated=self.is_truncated,
        )

    @classmethod
    def of(
        cls, rankings: CondorcetRankings[T], matrix: CondorcetMatrix[T]
    ) -> CondorcetRankingTieBreak[T]:
        return cls(
            Map(
                {
                    ranking: CondorcetTieBreakScore.of(ranking, matrix)
                    for ranking in rankings
                }
            ),
            rankings.is_truncated,
        )
