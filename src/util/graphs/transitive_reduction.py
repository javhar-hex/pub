from __future__ import annotations

import dataclasses as dc
from typing import Dict, Generic, Optional, TypeVar

from util.graphs.digraph import DiGraph
from util.graphs.topo_sort import GraphIsCyclicError, TopoSort

Node = TypeVar("Node")


@dc.dataclass(frozen=True)
class TransitiveReduction(Generic[Node]):
    """
    Transitive reduction of a digraph.

    If the digraph is acyclic, the transitive reduction is the unique smallest subgraph
    with the following equivalent properties:
    * The reduced graph has the same transitive closure as the original graph.
    * The reduced graph has the same nodes, if there exists a path between two nodes in
      the original graph then there also exists a path in the reduced graph.
    * The reduced graph is obtained by removing "superfluous edges", where an edge
      is superfluous if there is also an indirect path between the two nodes.

    If the digraph is cyclic, the transitive closure does not exist. This can be 
    tested with the `exists` property.

    In the course of computing the transitive closure, a topological sort of the digraph
    is created. The topological ordering is recorded in this object for convenience.
    """

    _reduced_digraph_opt: Optional[DiGraph[Node]]
    topo_sort: TopoSort[Node]

    def __str__(self) -> str:
        msg = "reduced_digraph=%s, %s" % (self._reduced_digraph_opt,
            str(self.topo_sort),
        ) if self._reduced_digraph_opt else "none; cyclic graph"
        return f"TransitiveReduction({msg})"

    @property
    def reduced_digraph(self) -> DiGraph[Node]:
        """
        Return the transitive reduction. If none exists, raise a GraphIsCyclicError.
        """
        if self._reduced_digraph_opt is None:
            raise GraphIsCyclicError("graph is cyclic, no transitive reduction exists")
        return self._reduced_digraph_opt
    
    @property
    def exists(self) -> bool:
        """
        Return True iff a transitive reduction exists, which is iff the digraph is
        acyclic.
        """
        return self._reduced_digraph_opt is not None
    
    @classmethod
    def of(cls, digraph: DiGraph[Node]) -> TransitiveReduction[Node]:
        topo_sort = TopoSort[Node].of(digraph)
        if not topo_sort.is_dag:
            return TransitiveReduction(_reduced_digraph_opt=None, topo_sort=topo_sort)

        node_index: Dict[Node, int] = {
            node: idx for idx, node in enumerate(topo_sort.order)
        }

        node_descendants = _node_descendants(digraph, topo_sort, node_index)

        builder = DiGraph[Node].builder()

        for node in topo_sort.order:
            builder.add_node(node)
            for neighbour in _reduced_neighbours(
                digraph, node_index, node_descendants, node
            ):
                builder.add_edge(node, neighbour)

        reduced_digraph = builder.build()
        return TransitiveReduction(reduced_digraph, topo_sort)


def _node_descendants(
    digraph: DiGraph[Node], topo_sort: TopoSort[Node], node_index: Dict[Node, int]
):
    bitmasks: Dict[Node, int] = {node: 0 for node in digraph.nodes()}
    for node in reversed(topo_sort.order):
        r = 0
        for neighbour in digraph.neighbours(node):
            r |= (1 << node_index[neighbour]) | bitmasks[neighbour]
        bitmasks[node] = r
    return bitmasks


def _reduced_neighbours(
    digraph: DiGraph[Node],
    node_index: Dict[Node, int],
    node_descendants: Dict[Node, int],
    node: Node,
):
    neighbours = list(digraph.neighbours(node))
    out_degree = len(neighbours)
    if out_degree == 0:
        return

    descendants_via = [
        (1 << node_index[neighbour]) | node_descendants[neighbour]
        for neighbour in neighbours
    ]

    # prefix/suffix OR so we can get union of "all except position i" in O(1)
    prefix = [0] * out_degree
    suffix = [0] * out_degree
    acc = 0
    for i in range(out_degree):
        acc |= descendants_via[i]
        prefix[i] = acc
    acc = 0
    for i in reversed(range(out_degree)):
        acc |= descendants_via[i]
        suffix[i] = acc

    for idx, neighbour in enumerate(neighbours):
        # union of all successors EXCEPT v
        left = prefix[idx - 1] if idx > 0 else 0
        right = suffix[idx + 1] if idx + 1 < out_degree else 0
        union_except_neighbour = left | right

        # if neighbour's bit is present via others, edge u->v is redundant
        if (union_except_neighbour >> node_index[neighbour]) & 1 == 0:
            yield neighbour
