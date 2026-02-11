import ranking.tournament_ranking as tr
from ranking.dtypes.ranking import Ranking
from ranking.tournament.tournament import TournamentBuilder


def test_tournament_ranking_no_tiebreaker():
    votes = [
        ["a", "b", "c", "d", "e"],
        ["a", "c", "d", "b", "e"],
        ["a", "d", "b", "c", "e"],
        ["b", "a"],
        ["c", "e"],
    ]
    tournament = TournamentBuilder[str]().add_paths(votes).build()
    ranking = tr.tournament_ranking(tournament, use_tiebreaker=False)
    assert len(ranking.segments) == 3
    assert set(ranking.segments[0]) == {Ranking[str].of(["a"])}
    assert set(ranking.segments[1]) == {
        Ranking[str].of(["b", "c", "d"]),
        Ranking[str].of(["c", "d", "b"]),
        Ranking[str].of(["d", "b", "c"]),
    }
    assert set(ranking.segments[2]) == {Ranking[str].of(["e"])}


def test_tournament_ranking_with_tiebreaker():
    votes = [
        ["a", "b", "c", "d", "e"],
        ["a", "c", "d", "b", "e"],
        ["a", "d", "b", "c", "e"],
        ["b", "a"],
        ["c", "e"],
    ]
    tournament = TournamentBuilder[str]().add_paths(votes).build()
    ranking = tr.tournament_ranking(tournament, use_tiebreaker=True)
    assert len(ranking.segments) == 3
    assert set(ranking.segments[0]) == {Ranking[str].of(["a"])}
    assert set(ranking.segments[1]) == {Ranking[str].of(["b", "c", "d"])}
    assert set(ranking.segments[2]) == {Ranking[str].of(["e"])}
