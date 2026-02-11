from util.graphs.condensation import condense
from util.graphs.digraph import DiGraph


def test_condense():
    #        A              +>>> A1       +<< Cc >>+
    #       /  \            ^     v       v    ^   v
    #      B    C    with   ^     v      Ca    ^  Cd     Da <--> Db
    #       \  /           A3 << A2       v    ^   v
    #         D                           +>> Cb <<+
       
    builder = DiGraph[str].builder()
    builder.add_edge("Aa", "Ab").add_edge("Ab", "Ac").add_edge("Ac", "Aa")
    builder.add_edge("Ca", "Cb").add_edge("Cb", "Cc").add_edge("Cc", "Ca")
    builder.add_edge("Cc", "Cd").add_edge("Cd", "Cb")
    builder.add_edge("Da", "Db").add_edge("Db", "Da")
    builder.add_edge("Aa", "B").add_edge("Ab", "Cb").add_edge("Ac", "Da")
    builder.add_edge("Ca", "Da").add_edge("Cb", "Db")
    builder.add_edge("B", "Da").add_edge("B", "Db")
    digraph = builder.build()
    condensation = condense(digraph)

    assert len(condensation.topo_sort.order) == 4

    subgraph_A = condensation.topo_sort.order[0]
    assert set(subgraph_A.nodes()) == {"Aa", "Ab", "Ac"}
    assert set(subgraph_A.neighbours("Aa")) == {"Ab"}
    assert set(subgraph_A.neighbours("Ab")) == {"Ac"}
    assert set(subgraph_A.neighbours("Ac")) == {"Aa"}

    if "B" in condensation.topo_sort.order[1].nodes():
        subgraph_B = condensation.topo_sort.order[1]
        subgraph_C = condensation.topo_sort.order[2]
    elif "B" in condensation.topo_sort.order[2].nodes():
        subgraph_B = condensation.topo_sort.order[2]
        subgraph_C = condensation.topo_sort.order[1]
    else:
        assert False

    assert set(subgraph_B.nodes()) == {"B"}
    assert set(subgraph_B.neighbours("B")) == set()

    assert set(subgraph_C.nodes()) == {"Ca", "Cb", "Cc", "Cd"}
    assert set(subgraph_C.neighbours("Ca")) == {"Cb"}
    assert set(subgraph_C.neighbours("Cb")) == {"Cc"}
    assert set(subgraph_C.neighbours("Cc")) == {"Ca", "Cd"}
    assert set(subgraph_C.neighbours("Cd")) == {"Cb"}

    subgraph_D = condensation.topo_sort.order[3]
    assert set(subgraph_D.nodes()) == {"Da", "Db"}
    assert set(subgraph_D.neighbours("Da")) == {"Db"}
    assert set(subgraph_D.neighbours("Db")) == {"Da"}

    assert set(condensation.reduced_digraph.nodes()) == {
        subgraph_A, subgraph_B, subgraph_C, subgraph_D
    }

    assert set(condensation.reduced_digraph.neighbours(subgraph_A)) == {
        subgraph_B, subgraph_C
    }
    assert set(condensation.reduced_digraph.neighbours(subgraph_B)) == {subgraph_D}
    assert set(condensation.reduced_digraph.neighbours(subgraph_C)) == {subgraph_D}
    assert set(condensation.reduced_digraph.neighbours(subgraph_D)) == set()
