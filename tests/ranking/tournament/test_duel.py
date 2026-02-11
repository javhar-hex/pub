
from ranking.tournament.duel import Duel
from ranking.tournament.duel_score import DuelScore


class DummySide:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other: object):
        return isinstance(other, DummySide) and self.name == other.name


def test_duel_fields():
    lhs = DummySide("Alice")
    rhs = DummySide("Bob")
    score = DuelScore(1, 0)
    duel = Duel(lhs=lhs, rhs=rhs, score=score)
    assert duel.lhs == lhs
    assert duel.rhs == rhs
    assert duel.score == score
