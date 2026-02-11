from __future__ import annotations

import dataclasses as dc
from functools import cached_property
from typing import Generic, Iterable, Optional, Tuple, TypeVar

import numpy as np

from util.dtypes.comparable import Comparable
from util.dtypes.numeric import tuple_numeric
from util.dtypes.u01 import U01
from util.functions.piecewise_linear import PiecewiseLinear
from util.functions.steps import Orientation, Steps

"""
Module for computing weighted quantiles.

Classes:
========
    Quantiles(Generic[Val]):
        Represents the quantile function for a sequence of comparable values, optionally
        weighted. Provides methods to compute the median and arbitrary quantiles, with
        options for interpolation.

Usage:
======
    Use Quantiles.of(values, weights) to construct a Quantiles object from a sequence of
        values and optional weights.
    Use .median() or .quantile() methods to retrieve quantile values, with optional
        interpolation.
"""

Val = TypeVar("Val", bound=Comparable)


@dc.dataclass(frozen=True)
class Quantiles(Generic[Val]):
    """
    Represents the quantile function for a sequence of comparable values with weights.

    Attributes:
        values (Tuple[Val, ...]): The sorted values for which quantiles are computed.
        cdf (Tuple[float, ...]): The cumulative distribution function values
            corresponding to `values`.
    """

    values: Tuple[Val, ...]
    cdf: Tuple[float, ...]

    def __len__(self) -> int:
        return len(self.values)

    def median(
        self, interpolate: bool = False, orientation: Orientation = Orientation.RIGHT
    ) -> Val | float:
        """
        Return the median value of the dataset.

        Args:
            interpolate (bool, optional): If True, interpolates between values when the
                median falls between two data points. Defaults to False.
            orientation (orientation, optional): If the median falls on the boundary
                between two quantile buckets, and interpolate is False, then return
                the lower value on the left or the higher value on the right. Defaults
                to Orientation.RIGHT.

        Returns:
            Val | float: The median value of the dataset, either as a Val object or a
                float. A float is returned when interpolating.
        """
        return self.quantile(U01(0.5), interpolate, orientation)

    def quantile(
        self,
        q: U01,
        interpolate: bool = False,
        orientation: Orientation = Orientation.RIGHT,
    ) -> Val | float:
        """
        Return the requested quantile of the dataset.

        Args:
            q (U01): The requested quantile, as an U01 object, which is a float between
                0 and 1, inclusive.
            interpolate (bool, optional): If True, interpolates between values when the
                median falls between two data points. Defaults to False.
            orientation (orientation, optional): If the median falls on the boundary
                between two quantile buckets, and interpolate is False, then return
                the lower value on the left or the higher value on the right. Defaults
                to Orientation.RIGHT.

        Returns:
            Val | float: The median value of the dataset, either as a Val object or a
                float. A float is returned when interpolating.
        """
        if interpolate:
            return self._piecewise_linear_function(q.value, strict=True)
        else:
            return self._step_function(q.value, strict=True, orientation=orientation)

    @cached_property
    def _step_function(self) -> Steps[Val]:
        bounds: tuple[float, ...] = (0.0, *self.cdf)
        return Steps[Val].make(bounds, self.values)

    @cached_property
    def _piecewise_linear_function(self) -> PiecewiseLinear:
        cdf_shifted = (0.0, *self.cdf[:-1])
        mids = tuple((lhs + rhs) / 2 for lhs, rhs in zip(cdf_shifted, self.cdf))
        xs = (0.0, *mids, 1.0)
        nums = tuple_numeric(self.values)
        ys = (nums[0], *nums, nums[-1])
        return PiecewiseLinear.make(xs, ys)

    @classmethod
    def of(
        cls, values: Iterable[Val], weights: Optional[Iterable[float]] = None
    ) -> Quantiles[Val]:
        """
        Create a Quantiles object from the given values, with optional weights. The
        values do not need to be sorted; they will be sorted automatically.

        Args:
            values (Iterable[Val]): a sequence of comparable values.
            weights (Iterable[float], optional): a sequence of weights as floats.
                Defaults to all-ones.

        Returns:
            A Quantiles object containing the quantile function of the dataset.
        Raises:
            ValueError when the sequence of values is empty, when the length of the
                weights does not correspond to the length of the values, when there
                are negative or intinite-valued weights, or when there are no positive
                weights.
        """
        values = _convert_values(values)
        weights = _convert_weights(weights, expected_size=len(values))
        values, weights = _drop_zero_weights(values, weights)
        values, weights = _sort_by_value(values, weights)
        cdf = _cdf(weights)

        return Quantiles(values, cdf)


def _convert_values(values: Iterable[Val]) -> Tuple[Val, ...]:
    values_tuple = tuple(values)
    if len(values_tuple) == 0:
        raise ValueError("values must be non-empty")
    return values_tuple


def _convert_weights(
    weights: Optional[Iterable[float]], expected_size: int
) -> np.ndarray:
    if weights is None:
        return np.ones(expected_size, dtype=float)
    arr = np.asarray(list(weights), dtype=float)
    if arr.ndim != 1:
        raise ValueError("weights must be a 1-D sequence")
    if arr.shape[0] != expected_size:
        raise ValueError(
            f"values and weights must have same length (got {expected_size} and {arr.shape[0]})"
        )
    if not np.isfinite(arr).all():
        raise ValueError("weights must be finite")
    if (arr < 0).any():
        raise ValueError("weights must be non-negative")
    return arr


def _drop_zero_weights(
    values: Tuple[Val, ...], weights: np.ndarray
) -> Tuple[Tuple[Val, ...], np.ndarray]:
    mask = weights > 0
    if not mask.any():
        raise ValueError("all weights are zero; nothing to compute")
    vs_kept = tuple([v for v, m in zip(values, mask) if m])
    ws_kept = weights[mask]

    return vs_kept, ws_kept


def _sort_by_value(
    values: Tuple[Val, ...], weights: np.ndarray
) -> Tuple[Tuple[Val, ...], np.ndarray]:
    order = sorted(range(len(values)), key=lambda i: values[i])
    vs_sorted = tuple([values[i] for i in order])
    ws_sorted = weights[order]

    return vs_sorted, ws_sorted


def _cdf(weights: np.ndarray) -> Tuple[float, ...]:
    total_weight = float(weights.sum())
    masses = weights / total_weight
    return tuple(np.cumsum(masses))
