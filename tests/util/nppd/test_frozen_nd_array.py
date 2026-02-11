import numpy as np
import pytest

from util.nppd.frozen_nd_array import FrozenNdArray


def test_arr():
    arr_py = [[0, 1, 2], [-1, 0, 4], [-2, -4, 0]]
    arr_np = np.array(arr_py)

    frozen_arr = FrozenNdArray(arr_py)
    assert np.array_equal(frozen_arr.arr, arr_np)

    frozen_arr = FrozenNdArray(arr_np)
    assert np.array_equal(frozen_arr.arr, arr_np)


def test_immutable_view():
    arr_np = np.array([[0, 1], [-1, 2]])
    frozen_arr = FrozenNdArray(arr_np)

    arr_np[0, 0] = 99
    assert np.array_equal(frozen_arr.arr, np.array([[0, 1], [-1, 2]]))

    with pytest.raises(ValueError):
        frozen_arr.arr[0, 0] = 88


def test_copy():
    arr_np = np.array([[0, 1], [-1, 2]])
    frozen_arr = FrozenNdArray(arr_np)

    vw = frozen_arr.copy()
    assert np.array_equal(vw, arr_np)

    vw[0, 0] = -99
    assert np.array_equal(vw, np.array([[-99, 1], [-1, 2]]))
    assert np.array_equal(frozen_arr.arr, np.array([[0, 1], [-1, 2]]))


def test_eq():
    lhs = FrozenNdArray([[0, 1], [-1, 2]])
    rhs = FrozenNdArray(np.array([[0, 1], [-1, 2]]))
    assert lhs == rhs
    assert hash(lhs) == hash(rhs)


def test_hash_reflexive_and_stable():
    frozen_arr = FrozenNdArray([[0, 1], [-1, 2]])
    h1 = hash(frozen_arr)
    h2 = hash(frozen_arr)
    assert isinstance(h1, int)
    assert h1 == h2  # stable across calls


def test_equal_nan_semantics_same_hash():
    lhs = FrozenNdArray(np.array([1.0, np.nan, -0.0, 0.0]))
    rhs = FrozenNdArray(np.array([1.0, np.nan, -0.0, 0.0]))
    assert lhs == rhs
    assert hash(lhs) == hash(rhs)


def test_minus_zero_plus_zero_hash_equal():
    lhs = FrozenNdArray([-0.0, 1.0])
    rhs = FrozenNdArray([+0.0, 1.0])
    assert lhs == rhs
    assert hash(lhs) == hash(rhs)


def test_not_equal_may_have_diff_hash_sanity():
    lhs = FrozenNdArray([1.0, 2.0, 3.0])
    rhs = FrozenNdArray([1.0, 2.0, 3.1])
    assert lhs != rhs
    assert hash(lhs) != hash(rhs)


def test_shape_affects_hash():
    lhs = FrozenNdArray(np.arange(6, dtype=np.float64).reshape(2, 3))
    rhs = FrozenNdArray(np.arange(6, dtype=np.float64).reshape(3, 2))
    assert lhs != rhs
    assert hash(lhs) != hash(rhs)


def test_hash_works_as_dict_key():
    key = FrozenNdArray([[1, 2], [3, 4]])
    d = {key: "ok"}
    other_key = FrozenNdArray([[1, 2], [3, 4]])
    assert d[other_key] == "ok"


def test_hash_not_invalidated_by_readonly_view():
    arr = FrozenNdArray([1.0, 2.0, 3.0])
    h = hash(arr)
    _ = arr.arr
    assert hash(arr) == h
