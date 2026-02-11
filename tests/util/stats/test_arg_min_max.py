# tests/test_argminmax.py

from __future__ import annotations


from util.stats.arg_min_max import ArgMinMaxAccumulator


def test_basic_min_max_with_ties():
    acc = ArgMinMaxAccumulator[str, int]()
    data = [("a", 3), ("b", 1), ("c", 1), ("d", 9), ("e", 9)]
    for k, v in data:
        acc.process(k, v)

    snap = acc.snapshot()
    assert snap.min == 1
    assert snap.max == 9
    assert snap.argmin == ("b", "c")  # preserves first-seen order
    assert snap.argmax == ("d", "e")


def test_empty_accumulator():
    acc = ArgMinMaxAccumulator[str, int]()
    snap = acc.snapshot()
    assert snap.min is None
    assert snap.max is None
    assert snap.argmin == ()
    assert snap.argmax == ()


def test_snapshot_immutability():
    acc = ArgMinMaxAccumulator[str, int]()
    for k, v in [("x", 2), ("y", 5), ("z", 5)]:
        acc.process(k, v)

    snap1 = acc.snapshot()
    # mutate accumulator after snapshot
    acc.process("w", 1).process("t", 7)

    # snap1 must remain unchanged
    assert snap1.min == 2
    assert snap1.max == 5
    assert snap1.argmin == ("x",)
    assert snap1.argmax == ("y", "z")

    # current snapshot reflects new extrema
    snap2 = acc.snapshot()
    assert snap2.min == 1
    assert snap2.max == 7
    assert snap2.argmin == ("w",)
    assert snap2.argmax == ("t",)


def test_all_equal_values():
    acc = ArgMinMaxAccumulator[str, int]()
    for k in ["a", "b", "c"]:
        acc.process(k, 42)

    snap = acc.snapshot()
    assert snap.min == 42
    assert snap.max == 42
    assert snap.argmin == ("a", "b", "c")
    assert snap.argmax == ("a", "b", "c")
