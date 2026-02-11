from typing import Dict, Generic, List, Set, TypeVar

from util.graphs.digraph import DiGraph
from util.graphs.transitive_reduction import TransitiveReduction

Node = TypeVar("Node")


def condense(digraph: DiGraph[Node]) -> TransitiveReduction[DiGraph[Node]]:
    """
    Create a condensation of the digraph.

    The condensation decomposes the digraph into its strongly connected components. Each
    of those components is a subgraph of the original digraph. The components are
    themselves connected according to the digraph edges from a node in one component to
    a node in another component.

    The condensation is then subjected to transitive reduction, which removes
    superfluous edges between components. The result is a TransitiveReduction object
    that contains a topological sort of the subgraphs, and the minimal digraph that
     maintains the connectivity of the original graph.

    Note that this TransitiveReduction digraph is a graph of graphs: its nodes are
    subgraphs of the original graph.
    """
    components = _tarjan_scc(digraph)
    condensed_dag = _condensed_dag(digraph, components)
    return TransitiveReduction[DiGraph[Node]].of(condensed_dag)


class _TarjanState(Generic[Node]):
    def __init__(self) -> None:
        self.index: Dict[Node, int] = {}
        self.lowlink: Dict[Node, int] = {}
        self.on_stack: Set[Node] = set()
        self.stack: List[Node] = []
        self.idx: int = 0
        self.components: List[List[Node]] = []


def _tarjan_scc(digraph: DiGraph[Node]) -> List[List[Node]]:
    # Tarjan's SCC algorithm main loop.
    state: _TarjanState[Node] = _TarjanState()
    for node in digraph.nodes():
        if node not in state.index:
            state = _strongconnect(state, digraph, node)
    return state.components


def _strongconnect(
    state: _TarjanState[Node], digraph: DiGraph[Node], node: Node
) -> _TarjanState[Node]:
    state = _add_node(node, state)

    for neighbour in digraph.neighbours(node):
        if neighbour not in state.index:
            # Neighbour has not yet been visited; recurse on it.
            _strongconnect(state, digraph, neighbour)
            if state.lowlink[neighbour] < state.lowlink[node]:
                state.lowlink[node] = state.lowlink[neighbour]
        elif neighbour in state.on_stack:
            # Neighbour is in stack and hence in the current SCC.
            if state.index[neighbour] < state.lowlink[node]:
                state.lowlink[node] = state.index[neighbour]

    # If node is a root node, pop the stack and generate an SCC
    if state.lowlink[node] == state.index[node]:
        state = _pop_scc(node, state)

    return state


def _add_node(node: Node, state: _TarjanState[Node]) -> _TarjanState[Node]:
    # Initialize a newly visited node into the state.
    state.index[node] = state.idx
    state.lowlink[node] = state.idx
    state.idx += 1

    state.stack.append(node)
    state.on_stack.add(node)

    return state


def _pop_scc(root_node: Node, state: _TarjanState[Node]) -> _TarjanState[Node]:
    # Pop the stack and add the popped nodes as a new SCC.
    component: List[Node] = []
    while True:
        node = state.stack.pop()
        state.on_stack.remove(node)
        component.append(node)
        if node == root_node:
            break
    state.components.append(component)
    return state


def _condensed_dag(
    digraph: DiGraph[Node], components: List[List[Node]]
) -> DiGraph[DiGraph[Node]]:
    # Create the DAG of the subgraphs.
    subgraphs = [_subgraph(digraph, component) for component in components]
    node_subgraph = {
        node: subgraph for subgraph in subgraphs for node in subgraph.nodes()
    }
    builder = DiGraph[DiGraph[Node]].builder()
    for subgraph in subgraphs:
        builder.add_node(subgraph)
        for node in subgraph.nodes():
            for neighbour in digraph.neighbours(node):
                if node_subgraph[neighbour] != subgraph:
                    builder.add_edge(subgraph, node_subgraph[neighbour])
    return builder.build()


def _subgraph(digraph: DiGraph[Node], component: List[Node]) -> DiGraph[Node]:
    # Create the subgraph containing the nodes of the component
    component_set: Set[Node] = set(component)
    builder = DiGraph[Node].builder()
    for node in component:
        builder.add_node(node)
        for neighbour in digraph.neighbours(node):
            if neighbour in component_set:
                builder.add_edge(node, neighbour)
    return builder.build()
