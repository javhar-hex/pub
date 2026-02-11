from collections.abc import Iterable
from typing import Optional, TypeVar

from ranking.condorcet.condorcet_matrix import CondorcetMatrixBuilder
from ranking.condorcet.condorcet_optimum import CondorcetOptimum
from ranking.condorcet.condorcet_ranking_tiebreak import CondorcetRankingTieBreak
from ranking.dtypes.segmented_ranking import SegmentedRanking, SegmentedRankingBuilder
from ranking.tournament.tournament import Tournament
from util.graphs.condensation import condense

Side = TypeVar("Side")

def tournament_ranking(tournament: Tournament[Side], use_tiebreaker: bool = True) -> SegmentedRanking[Side]:
    """
    Segmented optimal ranking of the tournament. The ranking is broken into ordered segments. Within each segment,
    multiple rankings of just that segment can be provided. The number of full rankings of all items is the
    ordered product of all the segment rankings.
    """
    digraph = tournament.h2h_digraph()
    condensed = condense(digraph)
    overall_cmx = _make_condorcet_matrix(tournament)
    builder = SegmentedRankingBuilder[Side]()
    for subgraph in condensed.topo_sort.order:
        nodes = list(subgraph.nodes())
        if len(nodes) == 1:
            builder.add_item(nodes[0])
        else:
            # optimize SCC = Condorcet tangle
            segment_cmx = _make_condorcet_matrix(tournament, nodes)
            optimum = CondorcetOptimum[Side].of(segment_cmx)
            component_rankings = optimum.rankings()
            if len(component_rankings) == 1 or not use_tiebreaker:
                builder.add_segment(component_rankings)
            else:
                tiebreaker = CondorcetRankingTieBreak[Side].of(component_rankings, overall_cmx)
                builder.add_segment(tiebreaker.optimum())
    return builder.build()


def _make_condorcet_matrix(tournament: Tournament[Side], sides: Optional[Iterable[Side]] = None):
    if sides is None:
        sides = tournament.sides
    builder = CondorcetMatrixBuilder(sides)
    for duel in tournament.duels():
        builder.possibly_add_entry(duel.lhs, duel.rhs, duel.score.lhs - duel.score.rhs)
    return builder.build()