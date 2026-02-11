from __future__ import annotations

import dataclasses as dc
from typing import Generic, TypeVar

from ranking.tournament.duel_score import DuelScore

Side = TypeVar("Side")


@dc.dataclass(frozen=True)
class Duel(Generic[Side]):
    """
    Simple container for the score of a duel between two competitors. Contains the
    identities of the competitors, and the outcome of the duel.
    """

    lhs: Side
    rhs: Side
    score: DuelScore

    def __str__(self) -> str:
        return f"{self.lhs} {self.score} {self.rhs}"
