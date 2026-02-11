from __future__ import annotations

import bisect as bs
import dataclasses as dc
from typing import List, Sequence, Tuple

import numpy as np

"""
Module: piecewise_linear
------------------------

This module provides a generic, immutable implementation of a piecewise linear function.

Classes:
--------

PiecewiseLinear:
    Immutable dataclass representing a piecewise linear function.

Usage Example:
--------------
    func = PiecewiseLinearFunction.make(xs=[0, 1, 2, 5], ys=[10, 13, 11, 2])
    value = func(3) # returns 8
    value = func(-1, strict=False) # returns 10 (extrapolated)
"""


@dc.dataclass(frozen=True)
class PiecewiseLinear:
    """
    A generic piecewise linear function interpolating between the pairs (x, y) from the
    `xs` and `ys`.

    Attributes:
        xs (Tuple[float, ...]): Monotonically increasing x-values of the knot points.
        ys (Tuple[float, ...]): y-values of the knot points.
    """

    xs: Tuple[float, ...]
    ys: Tuple[float, ...]

    def __call__(self, x: float, strict: bool = True) -> float:
        """
        Evaluates the piecewise linear function at the given input value.

        Args:
            x (float): The input value at which to evaluate the function.
            strict (bool, optional): If True, applies strict extrapolation rules.
                Defaults to True.

        Returns:
            float: The evaluated value of the piecewise linear function at `x`.
        Raises:
            ValueError if `x` is outside the bounds and `strict` is True.
        """
        if x < self.xs[0] or x > self.xs[-1]:
            return self._extrapolate(x, strict)
        else:
            return self._interpolate(x)

    def _extrapolate(self, x: float, strict: bool) -> float:
        if strict:
            raise ValueError(f"x={x} outside of bounds [{self.xs[0]}, {self.xs[-1]}]")
        return self.ys[0] if x < self.xs[0] else self.ys[-1]

    def _interpolate(self, x: float) -> float:
        idx_hi: int = np.clip(bs.bisect_left(self.xs, x), 0, len(self.ys) - 1)
        idx_lo = idx_hi - 1
        t = (x - self.xs[idx_lo]) / (self.xs[idx_hi] - self.xs[idx_lo])
        return self.ys[idx_lo] * (1.0 - t) + self.ys[idx_hi] * t

    @classmethod
    def make(cls, xs: Sequence[float], ys: Sequence[float]) -> PiecewiseLinear:
        """
        Create a PiecewiseLinearFunction instance with specified coordinates for the
        knot points.

        Args:
            xs (Sequence[float]): X-coordinates of the knot points.
            ys (Sequence[float]): Y-coordinates of the knot points.

        Returns:
            PiecewiseLinearFunction: A piecewise linear function object.

        Raises:
            ValueError: If xs and ys are empty, or of unequal length, or if xs are not
                strictly increasing.
        """
        msgs: List[str] = []
        if len(xs) <= 1:
            msgs.append("xs and ys must contain at least two points")
        if len(xs) != len(ys):
            msgs.append(
                f"xs and ys must have same length (got {len(xs)} and {len(ys)})"
            )
        for idx in range(len(xs) - 1):
            if xs[idx + 1] <= xs[idx]:
                msgs.append("xs must be strictly increasing")
        if len(msgs) > 0:
            raise ValueError("\n".join(msgs))
        return cls(tuple(xs), tuple(ys))
