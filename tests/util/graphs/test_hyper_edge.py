import dataclasses as dc

from util.graphs.hyper_edge import HyperEdge


def test_of_deduplicates_and_len_and_iter():
    edge: HyperEdge[int] = HyperEdge[int].of([1, 2, 2, 3])
    assert len(edge) == 3
    # Iteration returns all elements (order unspecified, so compare as sets)
    assert set(iter(edge)) == {1, 2, 3}


def test_equality_and_hashability():
    e1 = HyperEdge[int].of([1, 2, 3])
    e2 = HyperEdge[int].of([3, 2, 1])  # same members, different order in input
    assert e1 == e2
    # Hashable (can be used as dict key / in a set)
    s = {e1, e2}
    assert len(s) == 1


def test_str_is_deterministic_for_orderable_nodes():
    # Sorted by str(), not numeric order, but same for these strings
    e = HyperEdge[str].of(["b", "a", "c"])
    assert str(e) == "{a, b, c}"


def test_str_is_deterministic_for_unorderable_nodes():
    # Define nodes that do NOT implement ordering, but do implement __str__
    @dc.dataclass(frozen=True)
    class N:
        name: str
        def __str__(self) -> str:
            return self.name

    n3, n1, n2 = N("gamma"), N("alpha"), N("beta")
    e = HyperEdge[N].of([n3, n1, n2])
    # __str__ must order lexicographically by the str() key
    assert str(e) == "{alpha, beta, gamma}"


def test_of_accepts_any_iterable():
    # generator works too
    gen = (i for i in range(3))
    e = HyperEdge[int].of(gen)
    assert set(e) == {0, 1, 2}
    # tuple as well
    e2 = HyperEdge[int].of((0, 0, 1))
    assert set(e2) == {0, 1}


def test_repr_like_roundtrip_expectation():
    # Not a strict repr/ast literal, but at least contains members
    e = HyperEdge[str].of(["x", "y"])
    s = str(e)
    for part in ("{", "}", "x", "y", ","):
        assert part in s
