from __future__ import annotations

import dataclasses as dc
from collections import deque
from typing import Dict, Generic, List, Optional, Tuple, TypeVar

from util.graphs.digraph import DiGraph

Node = TypeVar("Node")


@dc.dataclass(frozen=True)
class TopoSort(Generic[Node]):
    """
    Topological sort of the nodes of a DiGraph.

    If the digraph from which this sort was constructed is cyclic, then the `order`
    is empty and `is_dag` is False.

    If the originating digraph is acyclic, then the topological sort exists but is not
    necessarily unique. The TopoSort will then contain one of the possible topological
    orderings.
    """

    _order_opt: Optional[Tuple[Node, ...]]
    is_dag: bool

    def __str__(self) -> str:
        msg = f"order={self._order_opt}" if self.is_dag else "none; cyclic graph"
        return f"TopoSort({msg})"
    
    @property
    def exists(self) -> bool:
        """
        Return True iff a topological ordering exists, which is iff the digraph is
        acyclic. This is equal to the is_dag property.
        """
        return self.is_dag

    @property
    def order(self) -> Tuple[Node, ...]:
        """
        Return a topological ordering. Raise a GraphIsCyclicError if none exists.
        """
        if self._order_opt is None:
            raise GraphIsCyclicError("digraph is cyclic, no topological order exists")
        return self._order_opt

    @classmethod
    def of(cls, digraph: DiGraph[Node]) -> TopoSort[Node]:
        indegrees = _indegrees(digraph)
        q = deque([node for node, degree in indegrees.items() if degree == 0])
        order: List[Node] = []
        while q:
            u = q.popleft()
            order.append(u)
            for v in digraph.neighbours(u):
                indegrees[v] -= 1
                if indegrees[v] == 0:
                    q.append(v)

        if len(order) != len(indegrees):
            return TopoSort(_order_opt=None, is_dag=False)
        else:
            return TopoSort(_order_opt=tuple(order), is_dag=True)


def _indegrees(digraph: DiGraph[Node]) -> Dict[Node, int]:
    indegrees: Dict[Node, int] = {node: 0 for node in digraph.nodes()}
    for node in digraph.nodes():
        for neighbour in digraph.neighbours(node):
            indegrees[neighbour] = indegrees.get(neighbour, 0) + 1
    return indegrees


class GraphIsCyclicError(ValueError):
    """Raised when a graph is not cyclic."""
