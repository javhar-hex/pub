from typing import List
import pytest

from src.util.dtypes.bitmask import iter_bits


@pytest.mark.parametrize(
    "mask,expected",
    [
        (0, []),
        (1, [0]),
        (2, [1]),
        (3, [0, 1]),
        (7, [0, 1, 2]),
        (8, [3]),
        (13, [0, 2, 3]),
        (255, list(range(8))),
        (1024, [10]),
    ]
)
def test_iter_bits(mask: int, expected: List[int]):
    assert list(iter_bits(mask)) == expected