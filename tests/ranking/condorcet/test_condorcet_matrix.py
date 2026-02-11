import numpy as np
import pytest

from ranking.condorcet.condorcet_matrix import CondorcetMatrix, CondorcetMatrixBuilder
from util.nppd.frozen_nd_array import FrozenNdArray


def test_condorcet_matrix_fields():
    items = ("A", "B", "C")
    mx = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    condorcet_matrix = CondorcetMatrix(items, FrozenNdArray(mx))
    assert condorcet_matrix.items == items
    assert len(condorcet_matrix) == 3
    assert np.array_equal(condorcet_matrix.mx, mx)


def test_violation_matrix():
    items = ("A", "B", "C")
    mx = np.array([[0, 1, -1], [2, -2, 3], [-3, 0, 0]])

    matrix = CondorcetMatrix(items, FrozenNdArray(mx))
    expected = np.array([[0, 0, 1], [0, 2, 0], [3, 0, 0]])
    assert np.array_equal(matrix.violation_mx, expected)


def test_borda():
    items = ("A", "B", "C")
    mx = np.array([[0, 1, -2], [-1, 0, 4], [2, -4, 0]])
    matrix = CondorcetMatrix(items, FrozenNdArray(mx))
    borda_matrix = matrix.borda
    assert borda_matrix.items == matrix.items
    expected = np.array([[0, -4, 1], [4, 0, 5], [-1, -5, 0]])
    assert np.array_equal(borda_matrix.mx, expected)


def test_sign():
    items = ("A", "B", "C")
    mx = np.array([[0, 1, -2], [-1, 0, 4], [2, -4, 0]])
    matrix = CondorcetMatrix(items, FrozenNdArray(mx))
    sign_matrix = matrix.sign
    assert sign_matrix.items == matrix.items
    expected = np.array([[0, 1, -1], [-1, 0, 1], [1, -1, 0]])
    assert np.array_equal(sign_matrix.mx, expected)


def test_condorcet_matrix_immutability():
    items = ("A", "B", "C")
    mx = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    condorcet_matrix = CondorcetMatrix(items, FrozenNdArray(mx))

    mx2 = condorcet_matrix.violation_mx
    mx2[0, 0] = 99
    assert np.array_equal(condorcet_matrix.mx, mx)


def test_builder():
    builder = CondorcetMatrixBuilder[str](["A", "B", "C", "D"])
    builder.add_entry("A", "B", 3)
    builder.add_entry("B", "C", 5)
    builder.add_entry("D", "A", 8)
    condorcet_matrix = builder.build()

    expected = np.array(
        [
            [0, 3, 0, -8],
            [-3, 0, 5, 0],
            [0, -5, 0, 0],
            [8, 0, 0, 0],
        ]
    )

    assert condorcet_matrix.items == ("A", "B", "C", "D")
    assert len(condorcet_matrix) == 4
    assert np.array_equal(condorcet_matrix.mx, expected)


def test_builder_add_invalid_entry():
    builder = CondorcetMatrixBuilder[str](["A", "B", "C"])
    builder.possibly_add_entry("A", "E", 3)
    builder.possibly_add_entry("E", "B", 5)
    builder.possibly_add_entry("E", "F", 8)

    condorcet_matrix = builder.build()

    assert np.array_equal(np.zeros([3, 3]), condorcet_matrix.mx)

    with pytest.raises(ValueError):
        builder.add_entry("A", "E", 3)
    with pytest.raises(ValueError):
        builder.add_entry("E", "B", 5)
    with pytest.raises(ValueError):
        builder.add_entry("E", "F", 8)


def test_immutability_after_builder():
    builder = CondorcetMatrixBuilder[str](["A", "B", "C"])
    builder.add_entry("A", "B", 3)
    condorcet_matrix_1 = builder.build()

    builder.add_entry("A", "C", 5)
    condorcet_matrix_2 = builder.build()

    expected_1 = np.array(
        [
            [0, 3, 0],
            [-3, 0, 0],
            [0, 0, 0],
        ]
    )
    expected_2 = np.array(
        [
            [0, 3, 5],
            [-3, 0, 0],
            [-5, 0, 0],
        ]
    )

    assert np.array_equal(condorcet_matrix_1.mx, expected_1)
    assert np.array_equal(condorcet_matrix_2.mx, expected_2)
