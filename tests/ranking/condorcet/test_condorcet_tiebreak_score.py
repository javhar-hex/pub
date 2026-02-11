from ranking.condorcet.condorcet_matrix import CondorcetMatrixBuilder
from ranking.condorcet.condorcet_tiebreak_score import CondorcetTieBreakScore
from ranking.condorcet.condorcet_rankings import Ranking


def test_constructor():
    builder = CondorcetMatrixBuilder[str](("A", "B", "C", "D"))
    builder.add_entry("A", "B", 1).add_entry("A", "C", 2).add_entry("A", "D", -4)
    builder.add_entry("B", "C", 8).add_entry("B", "D", 16)
    builder.add_entry("C", "D", 32)
    matrix = builder.build()
    ranking = Ranking[str].of(("A", "B", "C", "D"))
    score = CondorcetTieBreakScore.of(ranking, matrix)

    assert score.kemeny == 4.0
    assert score.borda == 47.0
    assert score.sign_kemeny == 1.0
    assert score.sign_borda == 2.0

def test_ordering():
    lhs = CondorcetTieBreakScore(0.0, 0.0, 0.0, 0.0)

    for rhs in [
        CondorcetTieBreakScore(1.0, -1.0, -1.0, -1.0),
        CondorcetTieBreakScore(0.0,  1.0, -1.0, -1.0),
        CondorcetTieBreakScore(0.0,  0.0,  1.0, -1.0),
        CondorcetTieBreakScore(0.0,  0.0,  0.0,  1.0),
    ]:
        assert rhs > lhs
        assert lhs < rhs
        assert not rhs < lhs
        assert not lhs > rhs
        assert not rhs == lhs

    for rhs in [
        CondorcetTieBreakScore(-1.0,  1.0,  1.0,  1.0),
        CondorcetTieBreakScore( 0.0, -1.0,  1.0,  1.0),
        CondorcetTieBreakScore( 0.0,  0.0, -1.0,  1.0),
        CondorcetTieBreakScore( 0.0,  0.0,  0.0, -1.0),
    ]:
        assert rhs < lhs
        assert lhs > rhs
        assert not rhs > lhs
        assert not lhs < rhs
        assert not rhs == lhs

    rhs = CondorcetTieBreakScore(0.0, 0.0, 0.0, 0.0)
    assert not rhs < lhs
    assert not lhs > rhs
    assert not rhs > lhs
    assert not lhs < rhs
    assert rhs == lhs
