import numpy as np
import pytest
import math

from util.dtypes.u01 import U01


class DummyFloat:
    def __float__(self):
        return 0.5


def test_valid_initialization():
    assert U01(0.0).value == 0.0
    assert U01(1.0).value == 1.0
    assert U01(0.5).value == 0.5
    assert math.isclose(U01(np.float32(0.3)).value, 0.3,rel_tol=1e-7)
    assert U01(np.int32(1)).value == 1.0
    assert U01(DummyFloat()).value == 0.5


def test_invalid_initialization():
    for val in [-0.1, 1.1]:
        with pytest.raises(ValueError):
            U01(val)

    for val in (-1, 2, -199):
        with pytest.raises(ValueError):
            U01(val)

    with pytest.raises(ValueError):
        U01(np.float64(-0.5))

    with pytest.raises(ValueError):
        U01(np.float64(np.int64(2)))


def test_float_conversion():
    u = U01(0.75)
    assert float(u) == 0.75


def test_mul_with_number_types():
    u = U01(0.5)
    assert u * 2 == 1.0
    assert u * 0.5 == 0.25
    assert u * np.float32(4) == 2.0
    assert u * np.int32(3) == 1.5


def test_rmul_with_number_types():
    u = U01(0.5)
    assert 2 * u == 1.0
    assert 0.5 * u == 0.25
    assert np.float32(4) * u == 2.0
    assert np.int32(3) * u == 1.5
