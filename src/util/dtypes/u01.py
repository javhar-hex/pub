import dataclasses as dc

from typing import Protocol, Union
import numpy as np

class SupportsFloat(Protocol):
    def __float__(self) -> float: ...

Number = Union[int, float, np.integer, np.floating, SupportsFloat]

@dc.dataclass(frozen=True, slots=True)
class U01:
    """
    A floating-point value constrained to the interval [0, 1].

    Supports multiplication with values of type alias Number.
    """
    value: float

    def __init__(self, value: SupportsFloat):
        """
        Initialize with a float value in the range [0, 1].
        Raises:
            ValueError: If the converted float value is not in the range [0, 1].
        """
        v = float(value)
        if not 0.0 <= v <= 1.0:
            raise ValueError(f"Expected value in [0, 1], got {v}")
        object.__setattr__(self, "value", v)  # allowed in frozen __init__

    def __float__(self) -> float:
        return self.value

    def __repr__(self) -> str:
        return f"U01({self.value})"

    def __mul__(self, other: Number) -> float:
        return float(self) * float(other)

    def __rmul__(self, other: Number) -> float:
        return float(other) * float(self)


