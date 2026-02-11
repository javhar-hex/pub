import numpy as np
import pytest
from typing import Any, List, Union
import math

from util.dtypes.numeric import tuple_numeric, tuple_numeric_or_none


def test_tuple_numeric_with_valid_ints():
    assert tuple_numeric([1, 2, 3]) == (1.0, 2.0, 3.0)


def test_tuple_numeric_with_valid_floats():
    assert tuple_numeric([1.1, 2.2, 3.3]) == (1.1, 2.2, 3.3)


def test_tuple_numeric_with_numpy_types():
    values: List[Union[np.int32, np.float64]] = [np.int32(1), np.float64(2.5)]
    assert tuple_numeric(values) == (1.0, 2.5)


def test_tuple_numeric_with_mixed_numeric_types():
    values: List[Any] = [1, 2.2, np.int64(3), np.float32(4.4)]
    expected = (1.0, 2.2, 3.0, 4.4)
    for i, (value, expected) in enumerate(zip(tuple_numeric(values), expected)):
        assert math.isclose(value, expected, rel_tol=1e-7)


def test_tuple_numeric_with_non_numeric_raises():
    with pytest.raises(TypeError):
        tuple_numeric([1, "a", 3])


def test_tuple_numeric_or_none_with_valid():
    assert tuple_numeric_or_none([1, 2.2, np.float64(3)]) == (1.0, 2.2, 3.0)


def test_tuple_numeric_or_none_with_non_numeric():
    assert tuple_numeric_or_none([1, "b", 3]) is None


def test_tuple_numeric_or_none_with_empty_sequence():
    assert tuple_numeric_or_none([]) == ()


def test_tuple_numeric_with_empty_sequence():
    assert tuple_numeric([]) == ()
