from ranking.condorcet.condorcet_rankings import (
    Ranking,
    CondorcetRankings,
)
from ranking.condorcet.condorcet_matrix import CondorcetMatrixBuilder
from ranking.condorcet.condorcet_ranking_tiebreak import CondorcetRankingTieBreak
from ranking.condorcet.condorcet_tiebreak_score import CondorcetTieBreakScore


def test_constructor():
    builder = CondorcetMatrixBuilder[str](("A", "B", "C", "D"))
    builder.add_entry("A", "B", 1).add_entry("A", "C", -1).add_entry("A", "D", 1)
    builder.add_entry("B", "C", 1).add_entry("B", "D", 2)
    builder.add_entry("C", "D", 4)
    matrix = builder.build()
    ranking_abcd = Ranking[str].of(("A", "B", "C", "D"))
    ranking_bcad = Ranking[str].of(("B", "C", "A", "D"))
    ranking_cabd = Ranking[str].of(("C", "A", "B", "D"))
    rankings = CondorcetRankings[str].of(
        -1,  # purposely incorrect cost
        (ranking_abcd, ranking_bcad, ranking_cabd),
        is_truncated=False,
    )
    tiebreak = CondorcetRankingTieBreak[str].of(rankings, matrix)
    assert not tiebreak.is_truncated
    assert tiebreak.scores[ranking_abcd] == CondorcetTieBreakScore(
        kemeny=1.0, borda=6.0, sign_kemeny=1.0, sign_borda=3.0
    )
    assert tiebreak.scores[ranking_bcad] == CondorcetTieBreakScore(
        kemeny=1.0, borda=2.0, sign_kemeny=1.0, sign_borda=1.0
    )
    assert tiebreak.scores[ranking_cabd] == CondorcetTieBreakScore(
        kemeny=1.0, borda=1.0, sign_kemeny=1.0, sign_borda=1.0
    )


def test_optimum():
    builder = CondorcetMatrixBuilder[str](("A", "B", "C", "D"))
    builder.add_entry("A", "B", 1).add_entry("A", "C", -1).add_entry("A", "D", 1)
    builder.add_entry("B", "C", 1).add_entry("B", "D", 2)
    builder.add_entry("C", "D", 4)
    matrix = builder.build()
    ranking_abcd = Ranking[str].of(("A", "B", "C", "D"))
    ranking_bcad = Ranking[str].of(("B", "C", "A", "D"))
    ranking_cabd = Ranking[str].of(("C", "A", "B", "D"))
    rankings = CondorcetRankings[str].of(
        -1,  # purposely incorrect cost
        (ranking_abcd, ranking_bcad, ranking_cabd),
        is_truncated=False,
    )
    tiebreak = CondorcetRankingTieBreak[str].of(rankings, matrix)

    assert tiebreak.optimum() == CondorcetRankings[str].of(
        cost=1.0, rankings=[ranking_cabd], is_truncated=False
    )
