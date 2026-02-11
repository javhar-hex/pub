from __future__ import annotations

import bisect as bsct
import dataclasses as dc
from enum import StrEnum
from typing import Generic, List, Optional, Sequence, Tuple, TypeVar

import numpy as np

"""
Module: steps
-------------

This module provides a generic, immutable step function implementation. It allows
mapping intervals, as defined by bounds, to values. It allows configurable orientation
specifying whether the boundary values are to be mapped to the left or to the right
interval. The step function supports interpolation within bounds and extrapolation
outside bounds, with optional strictness.

Classes:
--------

Orientation(StrEnum):
    Enum to specify interval orientation:
        - LEFT: Boundary values are mapped to the interval on the left.
        - RIGHT: Boundary values are mapped to the interval on the right.

Steps(Generic[Val]):
    Immutable dataclass representing a step function.

Usage Example:
--------------
    func = Steps[int].make(bounds=[0, 1, 3, 4], values=[11, 12, 13])
    value = func(2)  # Returns 12
    value = func(-1, strict=False)  # Returns 11 (extrapolated)

Notes:
------
- The bounds must be strictly increasing and one longer than values. The provided
  factory method Steps.make() can be used to construct a Steps function in a consistent
  state.
- Extrapolation outside bounds can be strict, which raises an error, or non-strict,
  which returns the outer boundary value.
"""

Val = TypeVar("Val")


class Orientation(StrEnum):
    LEFT = "left"
    RIGHT = "right"

    def get_idx(self, bounds: Tuple[float, ...], x: float) -> int:
        bisector = bsct.bisect_left if self is Orientation.LEFT else bsct.bisect_right
        return bisector(bounds, x)


@dc.dataclass(frozen=True)
class Steps(Generic[Val]):
    """
    A generic step function mapping intervals defined by `bounds` to corresponding
    `values`.

    Attributes:
        bounds (Tuple[float, ...]): Monotonically increasing sequence of interval
            boundaries.
        values (Tuple[Val, ...]): Sequence of values assigned to each interval.
        orientation (Orientation): Determines whether boundary values are mapped to the
            interval on the left or on the right.
    """

    bounds: Tuple[float, ...]
    values: Tuple[Val, ...]
    orientation: Orientation

    def __call__(
        self, x: float, strict: bool = True, orientation: Optional[Orientation] = None
    ) -> Val:
        """
        Evaluates the step function at the given input value.

        Args:
            x (float): The input value at which to evaluate the function.
            strict (bool, optional): If True, applies strict extrapolation rules.
                Defaults to True.
            orientation (Orientation, optional): For boundary values, map to the value
                on the left or the value on the right. Defaults to the orientation of
                the step function.

        Returns:
            Val: The evaluated value of the step function at `x`.
        Raises:
            ValueError if `x` is outside the bounds and `strict` is True.
        """
        if orientation is None:
            orientation = self.orientation
        if x < self.bounds[0] or x > self.bounds[-1]:
            return self._extrapolate(x, strict)
        else:
            return self._interpolate(x, orientation)

    def _extrapolate(self, x: float, strict: bool) -> Val:
        if strict:
            msg = f"x={x} outside of bounds [{self.bounds[0]}, {self.bounds[-1]}]"
            raise ValueError(msg)
        return self.values[0] if x < self.bounds[0] else self.values[-1]

    def _interpolate(self, x: float, orientation: Orientation) -> Val:
        idx: int = orientation.get_idx(self.bounds, x) - 1
        idx = np.clip(idx, 0, len(self.values) - 1)
        return self.values[idx]

    @classmethod
    def make(
        cls,
        bounds: Sequence[float],
        values: Sequence[Val],
        orientation: Orientation = Orientation.RIGHT,
    ) -> Steps[Val]:
        """
        Creates a Steps instance with specified bounds, values, and orientation.

        Args:
            bounds (Sequence[float]): A sequence of boundary values that must be
                strictly increasing. The length of bounds must be one greater than the
                length of values.
            values (Sequence[Val]): A non-empty sequence of values associated with each
                interval.
            orientation (Orientation, optional): The orientation of the step function.
                Defaults to Orientation.RIGHT.

        Returns:
            Steps[Val]: A step function object.

        Raises:
            ValueError: If values is empty, if bounds is not one longer than values, or
                if bounds is not strictly increasing.
        """
        msgs: List[str] = []
        if len(values) < 1:
            msgs.append("values must be nonempty")
        if len(bounds) != len(values) + 1:
            msgs.append(
                "bounds must be one longer than values "
                f"(got {len(bounds)} and {len(values)})"
            )
        for idx in range(len(bounds) - 1):
            if bounds[idx + 1] <= bounds[idx]:
                msgs.append("bounds must be strictly increasing")
                break
        if len(msgs) > 0:
            raise ValueError("\n".join(msgs))

        return cls(tuple(bounds), tuple(values), orientation)
