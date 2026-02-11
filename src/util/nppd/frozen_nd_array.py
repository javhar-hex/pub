from __future__ import annotations

from typing import Optional

import numpy as np
from numpy.typing import ArrayLike, DTypeLike


class FrozenNdArray:
    """
    Immutable hashable wrapper for numpy ndarrays.

    The immutability is designed to guard against accidental mutation. No guarantees are
    made against intentional mutation nor the resulting behaviour.
    """

    __slots__ = ("_arr", "_hash")

    def __init__(self, data: ArrayLike, *, dtype: Optional[DTypeLike] = None):
        a = np.array(data, dtype=dtype, copy=True, order="C")
        a.setflags(write=False)  # lock base against accidental writes
        self._arr: np.ndarray = a
        self._hash: Optional[int] = None  # lazy cache

    @property
    def arr(self) -> np.ndarray:
        """
        Read-only view of the numpy array.
        (Cooperative callers: do not mutate via .base or similar tricks.)
        """
        vw = self._arr.view()
        vw.setflags(write=False)
        return vw

    def copy(self) -> np.ndarray:
        """
        Writable copy of the numpy array.
        """
        return self._arr.copy(order="C")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FrozenNdArray):
            return NotImplemented
        return np.array_equal(self._arr, other._arr, equal_nan=True)

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = _array_hash(self._arr)
        return self._hash

    def __str__(self) -> str:
        return f"FrozenNdArray(\n" f"{self._arr})"


def _array_hash(arr: np.ndarray) -> int:
    if arr.dtype.kind == "f":
        data = _float_array_data(arr)
    elif arr.dtype.kind == "c":
        data = _complex_array_data(arr)
    else:
        data = arr.tobytes(order="C")

    return hash((arr.dtype.str, arr.shape, data))


def _float_array_data(arr: np.ndarray) -> bytes:
    tmp = arr.copy(order="C")
    tmp[tmp == 0] = 0.0
    idx = np.isnan(tmp)
    if idx.any():
        tmp[idx] = np.nan
    return tmp.tobytes()


def _complex_array_data(arr: np.ndarray) -> bytes:
    return NotImplemented
    # tmp = arr.copy(order="C")
    # re, im = tmp.real, tmp.imag
    # re[re == 0] = 0.0
    # im[im == 0] = 0.0
    # nm = np.isnan(re) | np.isnan(im)
    # if nm.any():
    #     re[nm] = np.nan
    #     im[nm] = np.nan
    # return tmp.tobytes()
