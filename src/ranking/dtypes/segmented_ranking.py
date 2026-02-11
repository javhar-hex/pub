from __future__ import annotations
from collections.abc import Iterable
import dataclasses as dc
from functools import cached_property
from typing import FrozenSet, Generic, List, Self, Sequence, Tuple, TypeVar

from ranking.dtypes.ranking import Ranking

T = TypeVar("T")

@dc.dataclass(frozen=True)
class SegmentedRanking(Generic[T]):
    """
    Ranking of items, broken into ordered segments. Within each segment, multiple
    rankings of just that segment can be provided. The number of full rankings of all
    items is the ordered product of all the segment rankings.

    Example: if `segment_rankings` is (1, 2, {(3, 4, 5), (4, 5, 3)}, 6)
    then the possible rankings are: (1, 2, 3, 4, 5, 6) and (1, 2, 4, 5, 3, 6).
    """
    segments: Tuple[FrozenSet[Ranking[T]], ...]

    @cached_property    
    def multiplicities(self) -> Tuple[int, ...]:
        """
        Number of rankings in each segment. The total number of full rankings is the
        product of these numbers.
        """
        return tuple([len(segment) for segment in self.segments])
    
    def arbitrary(self) -> Ranking[T]:
        """
        An arbitrary full ranking among all possible full rankings.
        """
        items: List[T] = []
        for segment in self.segments:
            items.extend(next(iter(segment)))
        return Ranking[T].of(items)
    
class SegmentedRankingBuilder(Generic[T]):
    """
    Builder for segmented rankings. In practice, most segments will contain just one
    item, in which case it can be added with `add_item()`.
    """

    def __init__(self):
        self._segments: List[FrozenSet[Ranking[T]]] = []

    def add_item(self, item: T) -> Self:
        segment = [[item]]
        return self.add_segment(segment)
    
    def add_segment(self, segment: Iterable[Sequence[T]]):
        rankings = [Ranking[T].of(items) for items in segment]
        self._segments.append(frozenset(rankings))
        return self
    
    def build(self) -> SegmentedRanking[T]:
        return SegmentedRanking[T](tuple(self._segments))

