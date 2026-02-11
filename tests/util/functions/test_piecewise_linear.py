import pytest

from util.functions.piecewise_linear import PiecewiseLinear


def test_make_valid_input():
    xs = [0, 1, 2]
    ys = [10, 20, 30]
    func = PiecewiseLinear.make(xs, ys)
    assert func.xs == (0, 1, 2)
    assert func.ys == (10, 20, 30)


def test_make_empty_input():
    with pytest.raises(ValueError):
        PiecewiseLinear.make([], [])


def test_make_single_knot_input():
    with pytest.raises(ValueError):
        PiecewiseLinear.make([0], [5])


def test_make_unequal_length():
    xs = [0, 1]
    ys = [10]
    with pytest.raises(ValueError) as excinfo:
        PiecewiseLinear.make(xs, ys)
    assert "xs and ys must have same length" in str(excinfo.value)


def test_make_non_strictly_increasing_xs():
    xs = [0, 1, 1]
    ys = [10, 20, 30]
    with pytest.raises(ValueError) as excinfo:
        PiecewiseLinear.make(xs, ys)
    assert "xs must be strictly increasing" in str(excinfo.value)


def test_interpolate():
    xs = [0, 1, 3]
    ys = [10, 11, 7]
    func = PiecewiseLinear.make(xs, ys)
    assert func(0) == 10
    assert func(1) == 11
    assert func(3) == 7
    assert func(0.5) == 10.5
    assert func(2) == 9


def test_extrapolate():
    xs = [0, 1, 3]
    ys = [10, 11, 7]
    func = PiecewiseLinear.make(xs, ys)
    assert func(-1, strict=False) == 10
    assert func(5, strict=False) == 7
    with pytest.raises(ValueError):
        func(-1, strict=True)
    with pytest.raises(ValueError):
        func(5, strict=True)
