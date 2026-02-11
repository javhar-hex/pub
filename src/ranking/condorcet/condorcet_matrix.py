from __future__ import annotations
import dataclasses as dc
from typing import Generic, Hashable, Iterable, Self, Tuple, TypeVar

import numpy as np

from util.nppd.frozen_nd_array import FrozenNdArray

T = TypeVar("T", bound=Hashable)


@dc.dataclass(frozen=True)
class CondorcetMatrix(Generic[T]):
    r"""
    Matrix representing a tuple of items and the score between each pair of items. The
    matrix is antisymmetric: $M^\intercal = -M$ therefore in particular the diagonal
    elements are zero. A positive entry $M_{ij} > 0$ indicates that $i$ should
    preferably be ranked ahead of $j$. Conversely, if $M_{ij} < 0$ then $|M_{ij}|$
    represents the penalty that is incurred when ranking $i$ ahead of $j$.

    To ensure construction in a valid and consistent state, use the accompanying
    CondorcetMatrixBuilder class.
    """

    items: Tuple[T, ...]
    frozen_arr: FrozenNdArray

    def __len__(self) -> int:
        return len(self.items)

    @property
    def mx(self) -> np.ndarray:
        """
        The matrix as an immutable numpy array.
        """
        return self.frozen_arr.arr

    @property
    def violation_mx(self) -> np.ndarray:
        r"""
        Return the matrix of violation penalties. When $M$ is the Condorcet matrix, its
        violation matrix is $\max(0, -M)$.
        """
        return np.maximum(-self.frozen_arr.arr, 0)

    @property
    def borda(self) -> CondorcetMatrix[T]:
        r"""
        Return the Borda transform of this matrix.

        For each item, the Borda count is the sum of the entries in its row. For a
        pair of items, the corresponding entry in the Borda matrix is the difference
        of their Borda counts.

        If $M$ is a Condorcet matrix, so $M^\intercal = -M$, then the Borda transform
        is: $M \mathbf{1} + \mathbf{1} M$, in which $\mathbf{1}$ is the all-1 matrix.
        """
        row_sums = self.frozen_arr.arr.sum(axis=1, keepdims=True)
        col_sums = self.frozen_arr.arr.sum(axis=0, keepdims=True)
        borda_mx = row_sums + col_sums
        return CondorcetMatrix(self.items, FrozenNdArray(borda_mx))
    
    
    @property
    def sign(self) -> CondorcetMatrix[T]:
        """
        Return the sign of this matrix. This replaces all positive entries by +1 and
        all negative entries by -1.
        """
        return CondorcetMatrix(self.items,  FrozenNdArray(np.sign(self.frozen_arr.arr)))


class CondorcetMatrixBuilder(Generic[T]):
    def __init__(self, items: Iterable[T]):
        self._items = tuple(items)
        self._item_idx = {key: idx for idx, key in enumerate(self._items)}
        self._mx = np.zeros((len(self._items), len(self._items)), dtype=int)

    def possibly_add_entry(self, lhs: T, rhs: T, value: int) -> Self:
        r"""
        Add entries $M_{\mathrm{lhs},\mathrm{rhs}} =$ `value` and
        $M_{\mathrm{rhs}, \mathrm{lhs}} =$ `-value` to the matrix $M$. If `lhs` and
        `rhs` do not both exist in the list of items, do nothing.
        """
        self._add_entry(lhs, rhs, value, raise_if_not_exists=False)
        return self

    def add_entry(self, lhs: T, rhs: T, value: int) -> Self:
        r"""
        Add entries $M_{\mathrm{lhs},\mathrm{rhs}} =$ `value` and
        $M_{\mathrm{rhs}, \mathrm{lhs}} =$ `-value` to the matrix $M$. If `lhs` and
        `rhs` do not both exist in the list of items, raise a `ValueError`.
        """
        self._add_entry(lhs, rhs, value, raise_if_not_exists=True)
        return self

    def _add_entry(self, lhs: T, rhs: T, value: int, raise_if_not_exists: bool) -> Self:
        try:
            row = self._item_idx[lhs]
            col = self._item_idx[rhs]
        except KeyError:
            if not raise_if_not_exists:
                return self
            else:
                raise ValueError(
                    f"unknown row, col from {lhs}, {rhs}; " f"values are {self._items}"
                )

        self._mx[row, col] = value
        self._mx[col, row] = -value
        return self

    def build(self) -> CondorcetMatrix[T]:
        return CondorcetMatrix(self._items, FrozenNdArray(self._mx))
