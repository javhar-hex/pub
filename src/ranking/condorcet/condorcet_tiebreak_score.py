from __future__ import annotations

import dataclasses as dc
from typing import TypeVar

from ranking.condorcet.condorcet_matrix import CondorcetMatrix
from ranking.condorcet.condorcet_utils import ranking_cost
from ranking.condorcet.condorcet_rankings import Ranking

T = TypeVar("T")


@dc.dataclass(order=True, frozen=True)
class CondorcetTieBreakScore:
    """
    Collection of scores for a ranking under a Condorcet matrix $M$. Contains four
    scores:

    1. Kemeny score, being the total violation cost in $M$;
    2. total violation cost in the Borda matrix of $M$;
    3. violation score of the sign of $M$, being the _number_ of violations in $M$;
    4. violation score of the sign of the Borda matrix of $M$, being the number of
       violations in the Borda matrix.

    These scores are comparable by the lexicographic ordering of the Kemeny score,
    Borda score, signed Kemeny score, and signed Borda score.
    """

    kemeny: float
    borda: float
    sign_kemeny: float
    sign_borda: float

    @classmethod
    def of(
        cls, ranking: Ranking[T], matrix: CondorcetMatrix[T]
    ) -> CondorcetTieBreakScore:
        return cls(
            kemeny=ranking_cost(ranking, matrix),
            borda=ranking_cost(ranking, matrix.borda),
            sign_kemeny=ranking_cost(ranking, matrix.sign),
            sign_borda=ranking_cost(ranking, matrix.borda.sign),
        )
