from __future__ import annotations

import dataclasses as dc
from functools import cached_property
from typing import Generic, Self, Tuple, TypeVar

import numpy as np

from ranking.condorcet.condorcet_matrix import CondorcetMatrix
from util.dtypes.bitmask import iter_bits

T = TypeVar("T")


@dc.dataclass(frozen=True)
class CondorcetSubsetCosts(Generic[T]):
    """
    Container to encapsulate the incremental cost and optimal cost structure of a
    Condorcet matrix.

    The incremental cost of a node v and a set of nodes S, with v not in S, is the
    total violation penalty of placing v ahead of S. It is the sum over u in S of the
    violation penalty of putting v ahead of u.

    The optimal cost of a set of nodes S is the minimum violation penalty paid to
    arrange the items of S.

    These incremental costs and optimal costs are used to determine the optimal
    Condorcet rankings and the optimal Condorcet splits.
    """

    items: Tuple[T, ...]
    _incremental_costs: np.ndarray

    @property
    def num_items(self) -> int:
        return len(self.items)

    @property
    def split_costs(self) -> np.ndarray:
        """
        Return a numpy array containing the split cost per mask. A mask encodes a
        subset of the items as an int bitvector. The split cost is the Condorcet
        penalty paid to arrange the items in the mask after the items outside the mask.
        """
        return self._split_costs.copy()

    @property
    def mask_sizes(self) -> np.ndarray:
        """
        Return a numpy array containing the bitmask sizes, being the number of bits in
        each integer.
        """
        return self._mask_sizes.copy()

    def incremental_cost(self, bit: int, mask: int) -> float:
        """
        Return the penalty cost of arranging the item represented by the bit before the
        items represented by the bitmask.
        """
        return float(self._incremental_costs[bit, mask])

    def optimal_cost(self, mask: int = -1) -> float:
        """
        Return the minimal cost paid to arrange the items represented by the bitmask.
        """
        return self._optimal_costs[mask]

    def mask_to_items(self, mask: int) -> Tuple[T, ...]:
        """
        Convert the bitmask to a tuple of the items that it represents.
        """
        return tuple(self.items[idx] for idx in iter_bits(mask))

    @cached_property
    def _split_costs(self) -> np.ndarray:
        return np.nansum(self._incremental_costs, axis=0)

    @cached_property
    def _mask_sizes(self) -> np.ndarray:
        return np.sum(np.isnan(self._incremental_costs), axis=0)

    @cached_property
    def _optimal_costs(self) -> np.ndarray:
        size = 1 << self.num_items
        optimal_costs = np.full(size, np.inf, dtype=np.float64)
        optimal_costs[0] = 0.0
        for mask in range(1, size):
            best = np.inf
            for bit in iter_bits(mask):
                prev = mask ^ (1 << bit)
                cost = optimal_costs[prev] + self._incremental_costs[bit, prev]
                if cost < best:
                    best = cost
                    if best == 0.0:
                        break
            optimal_costs[mask] = best
        return optimal_costs

    @classmethod
    def of(cls, condorcet_matrix: CondorcetMatrix[T]) -> Self:
        violation_mx = condorcet_matrix.violation_mx.astype(np.float64)
        n = len(condorcet_matrix)
        size = 1 << len(condorcet_matrix)
        incremental_cost = np.zeros((n, size), dtype=np.float64)
        for item_idx in range(n):
            row = violation_mx[item_idx]
            bit = 1 << item_idx
            for mask in range(1, size):
                if mask & bit:  # invalid: bit is in mask.
                    incremental_cost[item_idx, mask] = np.nan
                    continue
                lsb = mask & -mask
                u = lsb.bit_length() - 1
                incremental_cost[item_idx, mask] = (
                    incremental_cost[item_idx, mask ^ lsb] + row[u]
                )
        return cls(condorcet_matrix.items, incremental_cost)
