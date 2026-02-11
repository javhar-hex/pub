from typing import Sequence, Tuple, TypeVar

import pytest

from util.graphs.digraph import DiGraph
from util.graphs.topo_sort import GraphIsCyclicError, TopoSort

Node = TypeVar("Node")


def test_toposort_on_acyclic_graph():
    # a -> b -> c
    edges = [
        ("a", "b"),
        ("b", "c"),
    ]
    digraph = make_digraph(edges)
    toposort = TopoSort[str].of(digraph)
    assert toposort.is_dag
    assert toposort.exists
    assert_topo_sort_integrity(toposort, edges)


def test_toposort_on_cyclic_graph():
    # a -> b -> c -> a (cycle)
    builder = DiGraph[str].builder()
    digraph = builder.add_edge("a", "b").add_edge("b", "c").add_edge("c", "a").build()
    toposort = TopoSort[str].of(digraph)
    assert not toposort.is_dag
    assert not toposort.exists
    with pytest.raises(GraphIsCyclicError):
        toposort.order


def test_toposort_on_disconnected_graph():
    # a -> b, c (disconnected)
    builder = DiGraph[str].builder()
    digraph = builder.add_edge("a", "b").add_node("c").build()
    toposort = TopoSort[str].of(digraph)
    assert toposort.is_dag
    assert toposort.exists
    assert set(toposort.order) == {"a", "b", "c"}
    node_idx = {node: idx for idx, node in enumerate(toposort.order)}
    assert node_idx["a"] < node_idx["b"]


def test_toposort_on_empty_graph():
    digraph = DiGraph[str].builder().build()
    toposort = TopoSort[str].of(digraph)
    assert toposort.is_dag
    assert toposort.exists
    assert toposort.order == ()


def test_toposort_on_multiple_edges():
    # a -> b, a -> c, b -> c
    edges = [
        ("a", "b"),
        ("a", "c"),
        ("b", "c"),
    ]
    digraph: DiGraph[str] = make_digraph(edges)
    toposort = TopoSort[str].of(digraph)
    assert toposort.is_dag
    assert toposort.exists
    assert_topo_sort_integrity(toposort, edges)


def test_toposort_on_self_loop():
    # a -> a (self-loop)
    digraph: DiGraph[str] = make_digraph([("a", "a")])
    toposort = TopoSort[str].of(digraph)
    assert not toposort.is_dag
    assert not toposort.exists
    with pytest.raises(GraphIsCyclicError):
        toposort.order


def test_nontrivial_sparse_dag():
    # a -> b, b -> c, b -> d, c -> e, d -> e
    edges = [
        ("a", "b"),
        ("b", "c"),
        ("b", "d"),
        ("c", "e"),
        ("d", "e"),
    ]
    digraph = make_digraph(edges)
    toposort = TopoSort[str].of(digraph)
    assert toposort.is_dag
    assert toposort.exists
    assert_topo_sort_integrity(toposort, edges)


def test_nontrivial_dense_dag():
    # a -> b, b -> c, b -> d, c -> e, d -> e
    edges = [
        ("a", "b"),
        ("a", "c"),
        ("a", "d"),
        ("a", "e"),
        ("b", "c"),
        ("b", "d"),
        ("b", "e"),
        ("c", "e"),
        ("d", "e"),
    ]
    digraph = make_digraph(edges)
    toposort = TopoSort[str].of(digraph)
    assert toposort.is_dag
    assert toposort.exists
    assert_topo_sort_integrity(toposort, edges)


def make_digraph(edges: Sequence[Tuple[Node, Node]]):
    builder = DiGraph[Node].builder()
    for head, tail in edges:
        builder.add_edge(head, tail)
    return builder.build()


def assert_topo_sort_integrity(
    topo_sort: TopoSort[Node], edges: Sequence[Tuple[Node, Node]]
):
    node_idx = {node: idx for idx, node in enumerate(topo_sort.order)}
    for head, tail in edges:
        assert node_idx[head] < node_idx[tail]
