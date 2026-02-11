from typing import Any, Optional, Sequence, Tuple, TypeAlias

import numpy as np

"""
This module provides utilities for handling numeric types and converting sequences to
tuples of floats.

Type Aliases:
    Numeric: Represents a union of int, float, numpy integer, and numpy floating types.
"""


Numeric: TypeAlias = int | float | np.integer | np.floating


def tuple_numeric(values: Sequence[Any]) -> Tuple[float, ...]:
    """
    Converts a sequence of values to a tuple of floats.

    Attempt to convert each value in the input sequence to a float. If conversion is
    successful for all values, return a tuple of floats.

    Args:
        values (Sequence[Any]): A sequence of values to be converted to floats.

    Returns:
        Tuple[float, ...]: A tuple containing the converted float values.

    Raises:
        TypeError: If any value in the sequence cannot be converted to float.
    """
    result = tuple_numeric_or_none(values)
    if result is not None:
        return result
    else:
        raise TypeError("Values cannot be converted to float.")


def tuple_numeric_or_none(values: Sequence[Any]) -> Optional[Tuple[float, ...]]:
    """
    Converts a sequence of numeric values to a tuple of floats, or returns None if any
    value is not numeric.

    Args:
        values (Sequence[Any]): A sequence of values to be checked and converted.

    Returns:
        Optional[Tuple[float, ...]]: A tuple of floats if all values are numeric,
        otherwise None.
    """
    admissible_types = (int, float, np.integer, np.floating)
    if all(isinstance(value, admissible_types) for value in values):
        return tuple(map(float, values))
    else:
        return None
