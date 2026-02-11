from immutables import Map

from ranking.tournament.duel import Duel
from ranking.tournament.duel_score import DuelScore
from ranking.tournament.tournament import Tournament, TournamentBuilder


def _make_simple_tournament() -> Tournament[str]:
    # Note that this is NOT a Tournament in normalized state; it does not contain
    # the inverse of each score.
    return Tournament(
        Map({"A": Map({"B": DuelScore(3, 2)}), "B": Map({"C": DuelScore(5, 3)})})
    )


def test_sides():
    tournament = _make_simple_tournament()
    assert set(tournament.sides) == {"A", "B", "C"}


def test_score_or_zero():
    tournament = _make_simple_tournament()
    assert tournament.score_or_zero("A", "B") == DuelScore(3, 2)
    assert tournament.score_or_zero("B", "C") == DuelScore(5, 3)
    assert tournament.score_or_zero("A", "C") == DuelScore(0, 0)


def test_duels():
    tournament = _make_simple_tournament()
    assert set(tournament.duels()) == {
        Duel(lhs="A", rhs="B", score=DuelScore(3, 2)),
        Duel(lhs="B", rhs="C", score=DuelScore(5, 3)),
    }


def test_match_results():
    builder = TournamentBuilder[str]()
    builder.add_win("A", "B")
    builder.add_win("A", "B")
    builder.add_win("B", "A")
    builder.add_win("B", "C")
    tournament = builder.build()
    #  A  2-1  0-0
    # 1-2  B   1-0
    # 0-0 0-1   C
    assert tournament.match_results("A") == DuelScore(1, 0)
    assert tournament.match_results("B") == DuelScore(1, 1)
    assert tournament.match_results("C") == DuelScore(0, 1)


def test_total_score():
    builder = TournamentBuilder[str]()
    builder.add_win("A", "B")
    builder.add_win("A", "B")
    builder.add_win("B", "A")
    builder.add_win("B", "C")
    tournament = builder.build()
    #  A  2-1  0-0
    # 1-2  B   1-0
    # 0-0 0-1   C
    assert tournament.total_score("A") == DuelScore(2, 1)
    assert tournament.total_score("B") == DuelScore(2, 2)
    assert tournament.total_score("C") == DuelScore(0, 1)


def test_select():
    builder = TournamentBuilder[str]()
    builder.add_paths([["A", "B", "C", "D", "E"], ["B", "D", "A", "E", "C"]])
    main_tournament = builder.build()
    select_tournament = main_tournament.select(["A", "B", "C"])
    assert set(main_tournament.sides) == {"A", "B", "C", "D", "E"}
    for lhs in select_tournament.sides:
        for rhs in select_tournament.sides:
            assert select_tournament.score_or_zero(
                lhs, rhs
            ) == main_tournament.score_or_zero(lhs, rhs)


def test_drop():
    builder = TournamentBuilder[str]()
    builder.add_paths([["A", "B", "C", "D", "E"], ["B", "D", "A", "E", "C"]])
    main_tournament = builder.build()
    drop_tournament = main_tournament.drop({"A", "B"})
    assert set(main_tournament.sides) == {"A", "B", "C", "D", "E"}
    assert set(drop_tournament.sides) == {"C", "D", "E"}
    for lhs in drop_tournament.sides:
        for rhs in drop_tournament.sides:
            assert drop_tournament.score_or_zero(
                lhs, rhs
            ) == main_tournament.score_or_zero(lhs, rhs)


def test_h2h_digraph():
    tournament = _make_simple_tournament()
    h2h = tournament.h2h_digraph()
    assert set(h2h.nodes()) == {"A", "B", "C"}
    assert set(h2h.neighbours("A")) == {"B"}
    assert set(h2h.neighbours("B")) == {"C"}
    assert set(h2h.neighbours("C")) == set()


def test_builder_empty():
    tournament = TournamentBuilder[str]().build()
    assert set(tournament.sides) == set()
    assert set(tournament.duels()) == set()


def test_builder_add_win():
    builder = TournamentBuilder[str]()
    builder.add_win("A", "B")
    builder.add_win("A", "B")
    builder.add_win("B", "A")
    builder.add_win("B", "C")
    tournament = builder.build()
    assert set(tournament.sides) == {"A", "B", "C"}
    assert set(tournament.duels()) == {
        Duel(lhs="A", rhs="B", score=DuelScore(2, 1)),
        Duel(lhs="B", rhs="A", score=DuelScore(1, 2)),
        Duel(lhs="B", rhs="C", score=DuelScore(1, 0)),
        Duel(lhs="C", rhs="B", score=DuelScore(0, 1)),
    }


def test_builder_add_path():
    builder = TournamentBuilder[str]()
    builder.add_path(["A", "B", "C"])
    tournament = builder.build()
    assert set(tournament.sides) == {"A", "B", "C"}
    assert set(tournament.duels()) == {
        Duel(lhs="A", rhs="B", score=DuelScore(1, 0)),
        Duel(lhs="A", rhs="C", score=DuelScore(1, 0)),
        Duel(lhs="B", rhs="A", score=DuelScore(0, 1)),
        Duel(lhs="B", rhs="C", score=DuelScore(1, 0)),
        Duel(lhs="C", rhs="A", score=DuelScore(0, 1)),
        Duel(lhs="C", rhs="B", score=DuelScore(0, 1)),
    }


def test_builder_add_paths():
    builder = TournamentBuilder[str]()
    builder.add_paths({("A", "B", "C"), ("C", "D", "B")})
    tournament = builder.build()
    assert set(tournament.sides) == {"A", "B", "C", "D"}
    assert set(tournament.duels()) == {
        Duel(lhs="A", rhs="B", score=DuelScore(1, 0)),
        Duel(lhs="A", rhs="C", score=DuelScore(1, 0)),
        Duel(lhs="B", rhs="A", score=DuelScore(0, 1)),
        Duel(lhs="B", rhs="C", score=DuelScore(1, 1)),
        Duel(lhs="B", rhs="D", score=DuelScore(0, 1)),
        Duel(lhs="C", rhs="A", score=DuelScore(0, 1)),
        Duel(lhs="C", rhs="B", score=DuelScore(1, 1)),
        Duel(lhs="C", rhs="D", score=DuelScore(1, 0)),
        Duel(lhs="D", rhs="B", score=DuelScore(1, 0)),
        Duel(lhs="D", rhs="C", score=DuelScore(0, 1)),
    }


def test_immutability():
    builder = TournamentBuilder[str]()
    tournament = builder.build()
    builder.add_win("A", "B")
    assert set(tournament.sides) == set()
