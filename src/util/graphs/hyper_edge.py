from __future__ import annotations
from typing import TypeVar, Generic, FrozenSet, Iterator, Iterable
import dataclasses as dc

Node = TypeVar("Node")

@dc.dataclass(frozen=True)
class HyperEdge(Generic[Node]):
    """
    A simple immutable hyper-edge: a frozen set of nodes.
    """
    nodes: FrozenSet[Node]

    def __str__(self) -> str:
        ordered_nodes: list[Node] = sorted(self.nodes, key=str)
        return '{' + ", ".join(str(node) for node in ordered_nodes) + '}'

    def __len__(self) -> int:
        return len(self.nodes)

    def __iter__(self) -> Iterator[Node]:
        return iter(self.nodes)

    @classmethod
    def of(cls, nodes: Iterable[Node]) -> HyperEdge[Node]:
        return cls(frozenset(nodes))
