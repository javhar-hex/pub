from __future__ import annotations

import dataclasses as dc
from typing import Dict, Generic, Hashable, Iterable, Self, Set, Tuple, TypeVar

from immutables import Map

Node = TypeVar("Node", bound=Hashable)


@dc.dataclass(frozen=True)
class DiGraph(Generic[Node]):
    """
    Immutable directed graph.

    To ensure construction in a consistent state, use the provided `DiGraphBuilder`
    class, also reachable via `DiGraph.builder()`.
    """

    edges: Map[Node, Tuple[Node, ...]]

    def __str__(self) -> str:
        def children_str(children: Iterable[Node]) -> str:
            return str(set(children)) if children else "∅"

        tokens = [
            f"{node} -> {children_str(neighbours)}"
            for node, neighbours in self.edges.items()
        ]
        token_list = ", ".join(tokens)
        return f"DiGraph({token_list})"

    def has_node(self, node: Node) -> bool:
        """
        True iff the node is in the digraph, either as the source or as the sink of an
        edge.
        """
        return node in self.edges

    def nodes(self) -> Iterable[Node]:
        """
        Iterable of all nodes in the digraph.
        """
        return self.edges.keys()

    def neighbours(self, node: Node) -> Iterable[Node]:
        """
        Iterable of neighboring nodes directly connected to `node`. Raise
        `NodeNotFoundError` if `node` does not exist in the digraph.
        """
        try:
            return self.edges[node]
        except KeyError as _:
            raise NodeNotFoundError(f"Node {node!r} not in DiGraph.") from None

    @classmethod
    def builder(cls: type[DiGraph[Node]]) -> DiGraphBuilder[Node]:
        return DiGraphBuilder()


class DiGraphBuilder(Generic[Node]):
    """
    Builder for `DiGraph` objects.
    """

    def __init__(self) -> None:
        self.edges: Dict[Node, Set[Node]] = {}

    def add_edge(self, source: Node, sink: Node) -> Self:
        for node in source, sink:
            self.add_node(node)
        self.edges[source].add(sink)
        return self

    def add_node(self, node: Node) -> Self:
        """
        Add `node` if it is not already present. Do not add any edges.
        """
        if node not in self.edges:
            self.edges[node] = set()
        return self

    def build(self) -> DiGraph[Node]:
        edges_map = Map(
            {node: tuple(neighbours) for node, neighbours in self.edges.items()}
        )
        return DiGraph(edges_map)


class NodeNotFoundError(KeyError):
    """Raised when a node is not present in the graph."""
