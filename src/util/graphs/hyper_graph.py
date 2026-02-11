from __future__ import annotations

import dataclasses as dc
from typing import Dict, Generic, Iterable, Iterator, Tuple, TypeVar

from util.graphs.hyper_edge import HyperEdge
from util.stats.arg_min_max import ArgMinMaxAccumulator

Node = TypeVar("Node")

@dc.dataclass(frozen=True)
class HyperGraph(Generic[Node]):
    """
    Hypergraph, or equivalently, a family of subsets.

    The hyperedges (subsets) are in fixed deterministic order.
    """
    hyperedges: Tuple[HyperEdge[Node], ...]

    @classmethod
    def of(cls, hyperedges: Iterable[Iterable[Node]]) -> HyperGraph[Node]:
        """Construct the hypergraph from a family of sets of nodes.
        """
        return HyperGraph[Node](tuple(HyperEdge[Node].of(edge) for edge in hyperedges))

    def __str__(self) -> str:
        return "(" + ", ".join(str(edge) for edge in self.hyperedges) + ")"

    def __len__(self) -> int:
        return len(self.hyperedges)

    def __iter__(self) -> Iterator[HyperEdge[Node]]:
        return iter(self.hyperedges)

    def medoid(self) -> HyperGraph[Node]:
        """
        A medoid, or median hyperedge (subset), is one that minimizes the total Hamming
        distance to all other hyperedges. There can be multiple such hyperedges.
        Together they form another hypergraph. Return this hypergraph.
        """
        # Let F be the family of subsets, and U the univere of elements.
        # Let m = |F| be the number of subsets.
        # For i in U let w[i] be the number of subsets in F that contain i.
        # The number of subsets that do not contain i is m - w[i].
        # For S in F let w[S] be sum_{i in S} w[i].
        # The total Hamming distance of S to the other subsets is:
        # * items in S contribute sum_{i in S} (m - w[i]) = m |S| - w[S];
        # * items not in S contribute sum_{i notin S} w[i] = w[U] - w[S].
        # Total distance is m |S| + w[U] - 2 w[S].
        # The term w[U] is constant, so we minimize m |S| - 2 w[S].

        w: Dict[Node, int] = {}
        for hyperedge in self.hyperedges:
            for node in hyperedge:
                w[node] = w.get(node, 0) + 1

        m = len(self)
        
        acc = ArgMinMaxAccumulator[HyperEdge[Node], int]()
        for edge in self.hyperedges:
            score = m * len(edge) - 2 * sum(w[node] for node in edge)
            acc.process(edge, score)
        return HyperGraph(acc.snapshot().argmin)
    