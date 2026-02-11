from util.graphs.hyper_edge import HyperEdge
from util.graphs.hyper_graph import HyperGraph


def test_medoid_unique_solution():
    hg = HyperGraph[str].of([["a", "b"], ["a"], ["b"]])
    med = hg.medoid()
    assert len(med) == 1
    assert med.hyperedges[0] == HyperEdge[str].of(["a", "b"])


def test_medoid_multiple_medoids_simple_pair():
    """
    Family: [{a}, {b}] with m=2, c[a]=1, c[b]=1.
    Scores: 2*1 - 2*1 = 0 for both => both medoids.
    """
    hg = HyperGraph[str].of([["a"], ["b"]])
    med = hg.medoid()
    assert {edge for edge in med.hyperedges} == {
        HyperEdge[str].of(["a"]),
        HyperEdge[str].of(["b"]),
    }


def test_medoid_multiple_solutions_m_factor():
    # Test that the factor m in m |S| - 2 w[S] is properly accounted for.
    hg = HyperGraph[str].of([["a", "b", "c"], ["a"], ["b"], ["c"]])
    # Correct medoid is all of them.
    # Incorrect medoid, when omitting the factor m, is only ["a", "b", "c"].

    med = hg.medoid()
    assert {edge for edge in med.hyperedges} == {
        HyperEdge[str].of(["a", "b", "c"]),
        HyperEdge[str].of(["a"]),
        HyperEdge[str].of(["b"]),
        HyperEdge[str].of(["c"]),
    }


def test_medoid_nontrivial():
    hg = HyperGraph[str].of([
        ["a", "b", "c", "d",         ],
        [     "b", "c",      "e",    ],
        [     "b", "c",      "e", "f"],
        [     "b",                   ],
        [               "d", "e",    ],
        [               "d",      "f"],
    ])

    med = hg.medoid()
    assert {edge for edge in med.hyperedges} == {
        HyperEdge[str].of(["b", "c", "e"]),
        HyperEdge[str].of(["b"]),
    }
