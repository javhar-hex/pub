from typing import Dict, List
import pytest
from util.graphs.digraph import DiGraph, NodeNotFoundError


def test_empty_graph():
    digraph = DiGraph[str].builder().build()
    assert list(digraph.nodes()) == []


def test_multiple_nodes_and_edges():
    edges: Dict[str, List[str]] = {
        'a': ['b', 'c'],
        'b': ['a', 'd'],
        'c': ['z'],
        'd': [],
    }

    builder = DiGraph[str].builder()
    for node, neighbours in edges.items():
        for neighbour in neighbours:
            builder.add_edge(node, neighbour)
    digraph = builder.build()

    assert set(digraph.nodes()) == {'a', 'b', 'c', 'd', 'z'}
    assert set(digraph.neighbours('a')) == {'b', 'c'}
    assert set(digraph.neighbours('b')) == {'a', 'd'}
    assert set(digraph.neighbours('c')) == {'z'}
    assert list(digraph.neighbours('d')) == []
    assert list(digraph.neighbours('z')) == []


def test_isolated_nodes():
    builder = DiGraph[str].builder()
    builder.add_edge('a', 'b')
    builder.add_node('c')
    builder.add_node('a')
    builder.add_node('b')
    digraph = builder.build()

    assert set(digraph.nodes()) == {'a', 'b', 'c'}
    assert set(digraph.neighbours('a')) == {'b'}
    assert list(digraph.neighbours('b')) == []
    assert list(digraph.neighbours('c')) == []


def test_neighbours_nonexistent_node():
    digraph = DiGraph[int].builder().add_edge(0, 1).build()
    with pytest.raises(NodeNotFoundError):
        digraph.neighbours(9)


def test_has_node():
    digraph = DiGraph[int].builder().add_edge(0, 1).build()
    assert digraph.has_node(0)
    assert digraph.has_node(1)
    assert not digraph.has_node(9)


def test_immutability():
    builder = DiGraph[int].builder().add_edge(0, 1)
    digraph = builder.build()
    builder.add_edge(2, 3)
    assert digraph.has_node(0)
    assert digraph.has_node(1)
    assert not digraph.has_node(2)
    assert not digraph.has_node(3)
