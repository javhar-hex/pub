from __future__ import annotations

import dataclasses as dc
from itertools import islice
from typing import Generator, Generic, List, Optional, Tuple, TypeVar

import numpy as np

from ranking.condorcet.condorcet_matrix import CondorcetMatrix
from ranking.condorcet.condorcet_subset_costs import CondorcetSubsetCosts
from ranking.condorcet.condorcet_rankings import CondorcetRankings
from ranking.condorcet.condorcet_splits import CondorcetSplits
from util.dtypes.bitmask import iter_bits

T = TypeVar("T")


@dc.dataclass(frozen=True)
class CondorcetOptimum(Generic[T]):
    """
    Class to generate the optimal rankings and optimal splits of a Condorcet matrix.

    A Condorcet matrix is an anti-symmetric matrix, where the entry [i,j] indicates
    how much i is preferred over j. If entry is e < 0, then the penalty paid for
    arranging i and j in the non-preferred order is -e. If e > 0 then the penalty is
    zero.

    The cost of a permutation is the sum of the penalties over all pairs of items. It
    is if and only if no item is preferred over an iteam that appeared before it.

    The cost of a split of the items into a head group and a tail group is the
    penalty over all pairs of an item from the head group and an item from the tail
    group.
    """
    costs: CondorcetSubsetCosts[T]

    def rankings(self, max_num: Optional[int] = None) -> CondorcetRankings[T]:
        score = self.costs.optimal_cost()

        if max_num is not None:
            permutations = list(islice(self._rankings(), max_num + 1))
            truncated = len(permutations) > max_num
            permutations = permutations[:max_num]
        else:
            permutations = list(self._rankings())
            truncated = False

        item_permutations = [
            [self.costs.items[idx] for idx in permutation]
            for permutation in permutations
        ]

        return CondorcetRankings[T].of(score, item_permutations, truncated)

    def splits(self, head_size: int) -> CondorcetSplits[T]:
        tail_size = len(self.costs.items) - head_size
        idxs = self.costs.mask_sizes == tail_size
        min_val = self.costs.split_costs[idxs].min()
        tail_masks = np.where(idxs & (self.costs.split_costs == min_val))[0]
        return CondorcetSplits[T].of_tails(
            cost=float(min_val),
            tails=(self.costs.mask_to_items(tail_mask) for tail_mask in tail_masks),
            items=self.costs.items,
        )

    def _rankings(self) -> Generator[Tuple[int, ...]]:
        n = self.costs.num_items
        mask = (1 << n) - 1
        suffix: List[int] = []
        for permutation in self._rankings_recursive(mask, suffix):
            yield permutation

    def _rankings_recursive(
        self,
        mask: int,
        suffix: List[int],
    ) -> Generator[Tuple[int, ...]]:
        if mask == 0:
            yield tuple(suffix)
        else:
            for bit in iter_bits(mask):
                prev = mask ^ (1 << bit)
                if np.isclose(
                    self.costs.optimal_cost(mask),
                    self.costs.optimal_cost(prev)
                    + self.costs.incremental_cost(bit, prev),
                ):
                    suffix.append(bit)
                    for permutation in self._rankings_recursive(
                        prev,
                        suffix,
                    ):
                        yield permutation
                    suffix.pop()

    @classmethod
    def of(cls, matrix: CondorcetMatrix[T]) -> CondorcetOptimum[T]:
        costs = CondorcetSubsetCosts[T].of(matrix)
        return cls(costs)
