import pytest
from util.graphs.digraph import DiGraph
from util.graphs.topo_sort import GraphIsCyclicError
from util.graphs.transitive_reduction import TransitiveReduction


def test_dag():
    builder = DiGraph[str].builder()
    digraph = builder.add_edge("a", "b").add_edge("a", "c").add_edge("b", "c").build()
    tred = TransitiveReduction[str].of(digraph)
    assert tred.exists 
    assert set(tred.reduced_digraph.neighbours('a')) == {'b'} # edge a->c is gone
    assert set(tred.reduced_digraph.neighbours('b')) == {'c'}
    assert set(tred.reduced_digraph.neighbours('c')) == set()


def test_big_dag():
    builder = DiGraph[str].builder()
    nodes = ('c', 'a', 'e', 'd', 'b')
    for idx, neighbour in enumerate(nodes):
        for node in nodes[:idx]:
            builder.add_edge(node, neighbour)
    digraph = builder.build()
    tred = TransitiveReduction[str].of(digraph)
    assert tred.exists 
    assert set(tred.reduced_digraph.neighbours('c')) == {'a'} 
    assert set(tred.reduced_digraph.neighbours('a')) == {'e'} 
    assert set(tred.reduced_digraph.neighbours('e')) == {'d'} 
    assert set(tred.reduced_digraph.neighbours('d')) == {'b'} 
    assert set(tred.reduced_digraph.neighbours('b')) == set()
    assert tuple(tred.topo_sort.order) == nodes


def test_nontrivial_dag():
    builder = DiGraph[str].builder()
    builder.add_edge('a', 'b').add_edge('a', 'c').add_edge('a', 'd').add_edge('a', 'e')
    builder.add_edge('b', 'c').add_edge('b', 'd').add_edge('b', 'e')
    builder.add_edge('c', 'e').add_edge('d', 'e')
    digraph = builder.build()
    tred = TransitiveReduction[str].of(digraph)
    assert tred.exists 
    assert set(tred.reduced_digraph.neighbours('a')) == {'b'} 
    assert set(tred.reduced_digraph.neighbours('b')) == {'c', 'd'} 
    assert set(tred.reduced_digraph.neighbours('c')) == {'e'} 
    assert set(tred.reduced_digraph.neighbours('d')) == {'e'} 
    assert set(tred.reduced_digraph.neighbours('e')) == set()
    assert tuple(tred.topo_sort.order) in [
        ('a', 'b', 'c', 'd', 'e'), 
        ('a', 'b', 'd', 'c', 'e'),
    ]


def test_cyclic_graph():
    builder = DiGraph[str].builder()
    digraph = builder.add_edge("a", "b").add_edge("b", "c").add_edge("c", "a").build()
    tred = TransitiveReduction[str].of(digraph)
    assert not tred.exists
    with pytest.raises(GraphIsCyclicError):
        tred.reduced_digraph
    assert not tred.topo_sort.is_dag


def test_empty_graph():
    digraph = DiGraph[int].builder().build()
    tred = TransitiveReduction[int].of(digraph)
    assert tred.exists is True
    assert tuple(tred.reduced_digraph.nodes()) == ()
    assert tred.topo_sort.order == ()


def test_single_node_graph():
    digraph = DiGraph[str].builder().add_node('x').build()
    tred = TransitiveReduction[str].of(digraph)
    assert tred.exists is True
    assert tuple(tred.reduced_digraph.nodes()) == ('x',)
    assert tuple(tred.reduced_digraph.neighbours('x')) == ()
    assert tred.topo_sort.order == ('x',)
