import numpy as np
import pytest
import math

from util.dtypes.u01 import U01
from util.functions.steps import Orientation
from util.stats.quantiles import Quantiles


def test_quantiles_basic():
    q = Quantiles[str].of(["a", "b", "c"])
    assert len(q) == 3
    assert q.values == ("a", "b", "c")
    assert all(0 < cdf <= 1 for cdf in q.cdf)
    assert q.median() == "b"
    assert q.quantile(U01(0.0)) == "a"
    assert q.quantile(U01(1.0)) == "c"


def test_quantiles_with_weights():
    values = ["x", "y", "z"]
    weights = [1, 2, 3]
    q = Quantiles[str].of(values, weights)
    assert len(q) == 3
    assert q.values == ("x", "y", "z")
    assert np.isclose(sum(np.diff((0.0, *q.cdf))), 1.0)
    assert q.quantile(U01(0.0)) == "x"
    assert q.quantile(U01(0.16)) == "x"
    assert q.quantile(U01(0.17)) == "y"
    assert q.quantile(U01(0.49)) == "y"
    assert q.quantile(U01(0.51)) == "z"
    assert q.quantile(U01(1.0)) == "z"

    assert q.quantile(U01(0.5), orientation=Orientation.LEFT) == "y"
    assert q.quantile(U01(0.5), orientation=Orientation.RIGHT) == "z"


def test_quantiles_interpolate():
    values = [10, 0, 40, 30]
    q = Quantiles[int].of(values)
    median = q.median(interpolate=True)
    assert isinstance(median, float)
    assert 10 < median < 30

    assert q.quantile(U01(0.0), interpolate=True) == 0
    assert q.quantile(U01(0.125), interpolate=True) == 0
    assert q.quantile(U01(0.25 ), interpolate=True) == 5
    assert q.quantile(U01(0.375), interpolate=True) == 10
    assert q.quantile(U01(0.5  ), interpolate=True) == 20
    assert q.quantile(U01(0.625), interpolate=True) == 30
    assert q.quantile(U01(0.75 ), interpolate=True) == 35
    assert q.quantile(U01(0.875), interpolate=True) == 40
    assert q.quantile(U01(1.0), interpolate=True) == 40


def test_weighted_quantiles_interpolate():
    values = [15, 0, 59, 45]
    weights = [1, 2, 3, 4]
    q = Quantiles[int].of(values, weights)

    assert math.isclose(q.quantile(U01(0.0 ), interpolate=True),  0, rel_tol=1e-7)
    assert math.isclose(q.quantile(U01(0.05), interpolate=True),  0, rel_tol=1e-7)
    assert math.isclose(q.quantile(U01(0.1 ), interpolate=True),  0, rel_tol=1e-7) # 1st
    assert math.isclose(q.quantile(U01(0.15), interpolate=True),  5, rel_tol=1e-7)
    assert math.isclose(q.quantile(U01(0.2 ), interpolate=True), 10, rel_tol=1e-7)
    assert math.isclose(q.quantile(U01(0.25), interpolate=True), 15, rel_tol=1e-7) # 2nd
    assert math.isclose(q.quantile(U01(0.3 ), interpolate=True), 21, rel_tol=1e-7)
    assert math.isclose(q.quantile(U01(0.45), interpolate=True), 39, rel_tol=1e-7)
    assert math.isclose(q.quantile(U01(0.5 ), interpolate=True), 45, rel_tol=1e-7) # 3rd
    assert math.isclose(q.quantile(U01(0.55), interpolate=True), 47, rel_tol=1e-7)
    assert math.isclose(q.quantile(U01(0.8 ), interpolate=True), 57, rel_tol=1e-7)
    assert math.isclose(q.quantile(U01(0.85), interpolate=True), 59, rel_tol=1e-7) # 4th
    assert math.isclose(q.quantile(U01(0.9 ), interpolate=True), 59, rel_tol=1e-7)
    assert math.isclose(q.quantile(U01(1.0 ), interpolate=True), 59, rel_tol=1e-7)


def test_quantiles_length_one():
    q = Quantiles[int].of([42])
    assert len(q) == 1
    assert q.median() == 42
    assert q.quantile(U01(0.0)) == 42
    assert q.quantile(U01(1.0)) == 42


def test_quantiles_zero_weights_raises():
    with pytest.raises(ValueError):
        Quantiles[int].of([1, 2, 3], [0, 0, 0])


def test_quantiles_empty_values_raises():
    with pytest.raises(ValueError):
        Quantiles[int].of([])


def test_quantiles_weights_length_mismatch():
    with pytest.raises(ValueError):
        Quantiles[int].of([1, 2], [1])


def test_quantiles_negative_weights_raises():
    with pytest.raises(ValueError):
        Quantiles[int].of([1, 2], [1, -1])


def test_quantiles_nonfinite_weights_raises():
    with pytest.raises(ValueError):
        Quantiles[int].of([1, 2], [1, float("inf")])
