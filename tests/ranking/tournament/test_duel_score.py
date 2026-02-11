import pytest

from ranking.tournament.duel_score import DuelScore


def test_duel_score():
    score = DuelScore(3, 2)
    assert score.lhs == 3
    assert score.rhs == 2


def test_duel_score_add():
    score1 = DuelScore(lhs=2, rhs=1)
    score2 = DuelScore(lhs=4, rhs=3)
    result = score1 + score2
    assert isinstance(result, DuelScore)
    assert result.lhs == 6
    assert result.rhs == 4

    score1 += DuelScore(5, 3)
    assert score1.lhs == 7
    assert score1.rhs == 4


def test_duel_score_plus():
    score1 = DuelScore(lhs=5, rhs=7)
    score2 = DuelScore(lhs=1, rhs=2)
    result = score1.plus(score2)
    assert result == DuelScore(lhs=6, rhs=9)


def test_duel_score_add_invalid_type():
    score = DuelScore(lhs=1, rhs=2)
    with pytest.raises(TypeError):
        _ = score + 5
