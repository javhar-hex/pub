from __future__ import annotations

import dataclasses as dc
from functools import cached_property
from typing import (
    Dict,
    FrozenSet,
    Generic,
    Hashable,
    Iterable,
    Iterator,
    Self,
    Sequence,
    Set,
    TypeVar,
)

from immutables import Map

from ranking.tournament.duel import Duel
from ranking.tournament.duel_score import DuelScore
from util.graphs.digraph import DiGraph, DiGraphBuilder

Side = TypeVar("Side", bound=Hashable)


@dc.dataclass(frozen=True)
class Tournament(Generic[Side]):
    """
    An immutable matrix of `DuelScore`s, accessible as a two-level map `lhs` → `rhs` →
    `DuelScore`.

    Not all `(lhs, rhs)` pairs are guaranteed to be in the `scores` map. Use the
    provided `score_or_zero()` method that returns a 0-0 score if the pair is not in the
    map.

    To ensure construction in a consistent state, use the provided `TournamentBuilder`.
    """

    scores: Map[Side, Map[Side, DuelScore]]

    @cached_property
    def sides(self) -> FrozenSet[Side]:
        result = set(self.scores.keys())
        for inner in self.scores.values():
            for key in inner.keys():
                result.add(key)
        return frozenset(result)

    def score_or_zero(self, lhs: Side, rhs: Side) -> DuelScore:
        try:
            return self.scores[lhs][rhs]
        except KeyError:
            return DuelScore(0, 0)

    def duels(self) -> Iterator[Duel[Side]]:
        """
        Iterator over all the head-to-head duels in this tournament. If the `Tournament`
        is constructed with the `TournamentBuilder`, each head-to-head duel will appear
        twice in this iteration: Once from the perspective for each side.
        """
        for lhs, inner in self.scores.items():
            for rhs, score in inner.items():
                yield Duel(lhs, rhs, score)

    def match_results(self, side: Side) -> DuelScore:
        """
        Number of wins and losses for `side` in head-to-head matchups.
        """
        wins = losses = 0
        for opponent in self.sides:
            score = self.score_or_zero(side, opponent)
            if score.lhs > score.rhs:
                wins += 1
            elif score.lhs < score.rhs:
                losses += 1
        return DuelScore(wins, losses)

    def total_score(self, side: Side) -> DuelScore:
        """
        Aggregate score for `side` against all opponents.
        """
        score = DuelScore(0, 0)
        for opponent in self.sides:
            score += self.score_or_zero(side, opponent)
        return score

    def select(self, sides: Iterable[Side]) -> Tournament[Side]:
        """
        Tournament restricted to just the `sides`, retaining the head-to-head scores.
        """
        return self._select(set(sides))

    def drop(self, sides: Iterable[Side]) -> Tournament[Side]:
        """
        Tournament with `sides` removed, retraining the head-to-head scores of the
        remaining sides.
        """
        return self._select(set(self.sides) - set(sides))

    def _select(self, sides: Set[Side]) -> Tournament[Side]:
        return Tournament(
            Map(
                {
                    lhs: Map(
                        {rhs: score for rhs, score in inner.items() if rhs in sides}
                    )
                    for lhs, inner in self.scores.items()
                    if lhs in sides
                }
            )
        )

    def h2h_digraph(self) -> DiGraph[Side]:
        """
        Directed graph representing the head-to-head structure of this tournament. There
        is a directed edge from node $u$ to nove $v$ iff $u$ has a winning head-to-head
        against $v$.
        """
        builder = DiGraphBuilder[Side]()
        for duel in self.duels():
            if duel.score.lhs > duel.score.rhs:
                builder.add_edge(duel.lhs, duel.rhs)
        return builder.build()


class TournamentBuilder(Generic[Side]):
    """
    Builder to construct a `Tournament` in a consistent and normalized state. The
    normalized state includes each head-to-head score twice: Once from the perspective
    of each side.
    """

    def __init__(self):
        self.scores: Dict[Side, Dict[Side, DuelScore]] = {}

    def add_paths(self, paths: Iterable[Sequence[Side]]) -> Self:
        """
        Add a collection of paths. Each path encodes a full ranking of the sides in it.
        For each ordered pair in the path, a single win is recorded for the left hand
        side over the right hand side.
        """
        for path in paths:
            self.add_path(path)
        return self

    def add_path(self, path: Sequence[Side]) -> Self:
        """
        Add one path, encoding a full ranking. For each ordered pair in the path, a
        single win is recorded for the left hand side over the right hand side.
        """
        for idx, rhs in enumerate(path):
            for lhs in path[:idx]:
                self.add_win(lhs, rhs)
        return self

    def add_win(self, lhs: Side, rhs: Side) -> Self:
        """
        Record a win of `lhs` against `rhs`, and a loss of `rhs` against `lhs`.
        """
        return self._add_score(lhs, rhs, DuelScore(1, 0))._add_score(
            rhs, lhs, DuelScore(0, 1)
        )

    def _add_score(self, lhs: Side, rhs: Side, score: DuelScore):
        if lhs not in self.scores:
            self.scores[lhs] = {}
        if rhs not in self.scores[lhs]:
            self.scores[lhs][rhs] = score
        else:
            self.scores[lhs][rhs] += score
        return self

    def build(self) -> Tournament[Side]:
        return Tournament(Map({lhs: Map(val) for lhs, val in self.scores.items()}))
