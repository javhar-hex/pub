r"""
Standalone Condorcet functions.

For cost-related functions: The **violation cost**, or **cost** for short, of a pair
$(i, j)$ in a Condorcet matrix $M$ is $\max(0, -M_{ij}) = \max(0, M_{ji})$. It is the
Condorcet penalty of ranking $i$ ahead of $j$.
"""

from __future__ import annotations

from itertools import combinations, product
from typing import Iterable, Tuple, TypeVar

from ranking.condorcet.condorcet_matrix import CondorcetMatrix
from ranking.dtypes.ranking import Ranking
from ranking.dtypes.split import Split

T = TypeVar("T")


def ranking_cost(ranking: Ranking[T], matrix: CondorcetMatrix[T]) -> float:
    """
    The sum of the cost or all ordered pairs in the ranking.
    """
    item_to_idx = {item: idx for idx, item in enumerate(matrix.items)}
    ranking_idxs = [item_to_idx[item] for item in ranking.items]
    pairs = combinations(ranking_idxs, 2)
    return _idx_pairs_cost(pairs, matrix)


def split_cost(split: Split[T], matrix: CondorcetMatrix[T]) -> float:
    """
    The sum of the cost over the Cartesian product of the head and tail of the split.
    """
    item_to_idx = {item: idx for idx, item in enumerate(matrix.items)}
    head_idxs = [item_to_idx[item] for item in split.head]
    tail_idxs = [item_to_idx[item] for item in split.tail]
    pairs = product(head_idxs, tail_idxs)
    return _idx_pairs_cost(pairs, matrix)


def _idx_pairs_cost(
    pairs: Iterable[Tuple[int, int]], matrix: CondorcetMatrix[T]
) -> float:
    h2hs = [matrix.mx[lhs, rhs] for lhs, rhs in pairs]
    return float(sum([max(0, -h2h) for h2h in h2hs]))
