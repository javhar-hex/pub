from typing import List

import pytest

from util.functions.steps import Orientation, Steps


def test_make_valid_right_orientation():
    bounds = [0, 1, 2]
    values = [10, 20]
    sf = Steps[int].make(bounds, values)
    assert sf.bounds == (0, 1, 2)
    assert sf.values == (10, 20)
    assert sf.orientation == Orientation.RIGHT


def test_make_valid_left_orientation():
    bounds = [0, 1, 2]
    values = [10, 20]
    sf = Steps[int].make(bounds, values, orientation=Orientation.LEFT)
    assert sf.bounds == (0, 1, 2)
    assert sf.values == (10, 20)
    assert sf.orientation == Orientation.LEFT


def test_make_empty_values_raises():
    bounds = [0, 1]
    values: List[int] = []
    with pytest.raises(ValueError) as excinfo:
        Steps[int].make(bounds, values)
    assert "values must be nonempty" in str(excinfo.value)


def test_make_bounds_not_one_longer_than_values_raises():
    bounds = [0, 1, 2, 3]
    values = [10, 20]
    with pytest.raises(ValueError) as excinfo:
        Steps[int].make(bounds, values)
    assert "bounds must be one longer than values" in str(excinfo.value)


def test_make_bounds_not_strictly_increasing_raises():
    bounds = [0, 2, 1]
    values = [10, 20]
    with pytest.raises(ValueError) as excinfo:
        Steps[int].make(bounds, values)
    assert "bounds must be strictly increasing" in str(excinfo.value)


def test_interpolation_left():
    bounds = [0, 1, 2]
    values = [10, 20]
    sf = Steps[int].make(bounds, values, orientation=Orientation.LEFT)
    assert sf(0) == 10
    assert sf(0.5) == 10
    assert sf(1) == 10
    assert sf(1.5) == 20
    assert sf(2) == 20


def test_interpolation_right():
    bounds = [0, 1, 2]
    values = [10, 20]
    sf = Steps[int].make(bounds, values, orientation=Orientation.RIGHT)
    assert sf(0) == 10
    assert sf(0.5) == 10
    assert sf(1) == 20
    assert sf(1.5) == 20
    assert sf(2) == 20


def test_override_orientation():
    bounds = [0, 1, 2]
    values = [10, 20]

    sf = Steps[int].make(bounds, values, orientation=Orientation.RIGHT)
    assert sf(1) == 20
    assert sf(1, orientation=Orientation.LEFT) == 10
    assert sf(1, orientation=Orientation.RIGHT) == 20

    sf = Steps[int].make(bounds, values, orientation=Orientation.LEFT)
    assert sf(1) == 10
    assert sf(1, orientation=Orientation.LEFT) == 10
    assert sf(1, orientation=Orientation.RIGHT) == 20


def test_extrapolation():
    bounds = [0, 1, 2]
    values = [10, 20]
    sf = Steps[int].make(bounds, values, orientation=Orientation.RIGHT)
    assert sf(-1, strict=False) == 10
    assert sf(3, strict=False) == 20
    with pytest.raises(ValueError):
        sf(-1, strict=True)
    with pytest.raises(ValueError):
        sf(3, strict=True)
