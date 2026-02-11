from __future__ import annotations

import dataclasses as dc


@dc.dataclass(frozen=True)
class DuelScore:
    """
    Simple container for the score of a matchup: lhs versus rhs. This can be used to
    represent the number of wins and losses in a head-to-head comparison, or the
    number of goals for and goals against, or points scored.

    The score respects the + and +- operators.
    """

    lhs: int
    rhs: int

    def __str__(self) -> str:
        return f"{self.lhs}-{self.rhs}"

    def __add__(self, other: object) -> DuelScore:
        if not isinstance(other, DuelScore):
            return NotImplemented
        return self.plus(other)

    def plus(self, other: DuelScore) -> DuelScore:
        return DuelScore(lhs=self.lhs + other.lhs, rhs=self.rhs + other.rhs)
