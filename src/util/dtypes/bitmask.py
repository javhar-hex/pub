from typing import Iterable


def iter_bits(mask: int) -> Iterable[int]:
    # Iterate over all the bits of the bitmask. Return the indices of the bits that are set.
    b = 0
    while (1 << b) <= mask:
        if mask & (1 << b):
            yield b
        b += 1
        