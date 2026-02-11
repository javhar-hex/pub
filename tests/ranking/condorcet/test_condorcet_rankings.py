from ranking.condorcet.condorcet_rankings import (
    Ranking,
    CondorcetRankings,
)


def test_condorcet_rankings_factory():
    rankings = CondorcetRankings[str].of(
        cost=3.14, rankings=[["A", "B", "C"], ["B", "C", "A"]], is_truncated=False
    )
    assert rankings.cost == 3.14
    assert len(rankings.rankings) == 2
    expected = {
        Ranking[str].of(("A", "B", "C")),
        Ranking[str].of(("B", "C", "A")),
    }
    for ranking in rankings.rankings:
        assert ranking in expected
    assert not rankings.is_truncated
