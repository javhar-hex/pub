from ranking.condorcet.condorcet_matrix import CondorcetMatrixBuilder
from ranking.condorcet.condorcet_optimum import CondorcetOptimum
from ranking.condorcet.condorcet_rankings import CondorcetRankings
from ranking.condorcet.condorcet_splits import CondorcetSplits


def test_optimal_rankings_5_difficult():
    optimum = make_instance_5_complicated()

    assert optimum.rankings() == CondorcetRankings[str].of(
        cost=50.0, rankings=[["C", "B", "E", "A", "D"]], is_truncated=False
    )


def test_optimal_rankings_5_cycle():
    optimum = make_instance_5_cycle()
    expected = CondorcetRankings[str].of(
        cost=3.0,
        rankings=[
            ("A", "B", "C", "D", "E"),
            ("B", "C", "D", "E", "A"),
            ("C", "D", "E", "A", "B"),
            ("D", "E", "A", "B", "C"),
            ("E", "A", "B", "C", "D"),
        ],
        is_truncated=False,
    )
    assert optimum.rankings() == expected
    for max_num_permutations in (5, 6):
        assert optimum.rankings(max_num_permutations) == expected


def test_optimal_rankings_truncated():
    optimum = make_instance_5_cycle()

    for max_num in (1, 2, 3, 4):

        solution = optimum.rankings(max_num)
        assert solution.cost == 3.0
        assert len(solution.rankings) == max_num
        assert len(set(solution.rankings)) == max_num
        expected = {
            ("A", "B", "C", "D", "E"),
            ("B", "C", "D", "E", "A"),
            ("C", "D", "E", "A", "B"),
            ("D", "E", "A", "B", "C"),
            ("E", "A", "B", "C", "D"),
        }
        for ranking in solution.rankings:
            assert ranking.items in expected
        assert solution.is_truncated


def test_optimal_splits_5_complicated():
    optimum = make_instance_5_complicated()

    assert optimum.splits(1) == CondorcetSplits[str].of_tails(
        cost=12.0, tails=[["B", "C", "D", "E"]], items=["A", "B", "C", "D", "E"]
    )

    assert optimum.splits(2) == CondorcetSplits[str].of_tails(
        cost=28.0, tails=[["B", "D", "E"]], items=["A", "B", "C", "D", "E"]
    )

    assert optimum.splits(3) == CondorcetSplits[str].of_tails(
        cost=50.0, tails=[["A", "D"]], items=["A", "B", "C", "D", "E"]
    )

    assert optimum.splits(4) == CondorcetSplits[str].of_tails(
        cost=3.0, tails=[["A"]], items=["A", "B", "C", "D", "E"]
    )


def test_optimal_splits_5_cycle():
    optimum = make_instance_5_cycle()

    assert optimum.splits(1) == CondorcetSplits[str].of_tails(
        cost=2.0,
        tails=[
            ["A", "B", "C", "D"],
            ["A", "B", "C", "E"],
            ["A", "B", "D", "E"],
            ["A", "C", "D", "E"],
            ["B", "C", "D", "E"]],
        items=["A", "B", "C", "D", "E"]
    )

    assert optimum.splits(2) == CondorcetSplits[str].of_tails(
        cost=3.0,
        tails=[
            ["A", "B", "C"],
            ["A", "B", "D"],
            ["A", "B", "E"],
            ["A", "C", "D"],
            ["A", "C", "E"],
            ["A", "D", "E"],
            ["B", "C", "D"],
            ["B", "C", "E"],
            ["B", "D", "E"],
            ["C", "D", "E"]],
        items=["A", "B", "C", "D", "E"]
    )

    assert optimum.splits(3) == CondorcetSplits[str].of_tails(
        cost=3.0,
        tails=[
            ["A", "B"],
            ["A", "C"],
            ["A", "D"],
            ["A", "E"],
            ["B", "C"],
            ["B", "D"],
            ["B", "E"],
            ["C", "D"],
            ["C", "E"],
            ["B", "D"],
            ["D", "E"]],
        items=["A", "B", "C", "D", "E"]
    )

    assert optimum.splits(4) == CondorcetSplits[str].of_tails(
        cost=2.0,
        tails=[
            ["A"], ["B"], ["C"], ["D"], ["E"]],
        items=["A", "B", "C", "D", "E"]
    )


def make_instance_5_complicated():
    builder = CondorcetMatrixBuilder[str](("A", "B", "C", "D", "E"))
    builder.add_entry("A", "B", -4)
    builder.add_entry("A", "C", 2)
    builder.add_entry("A", "D", 1)
    builder.add_entry("A", "E", -8)
    builder.add_entry("B", "C", -128)
    builder.add_entry("B", "D", -32)
    builder.add_entry("B", "E", 512)
    builder.add_entry("C", "D", -16)
    builder.add_entry("C", "E", 256)
    builder.add_entry("D", "E", -64)
    matrix = builder.build()
    return CondorcetOptimum[str].of(matrix)


def make_instance_5_cycle():
    builder = CondorcetMatrixBuilder[str](("A", "B", "C", "D", "E"))
    builder.add_entry("A", "B", 1)
    builder.add_entry("A", "C", 1)
    builder.add_entry("A", "D", -1)
    builder.add_entry("A", "E", -1)
    builder.add_entry("B", "C", 1)
    builder.add_entry("B", "D", 1)
    builder.add_entry("B", "E", -1)
    builder.add_entry("C", "D", 1)
    builder.add_entry("C", "E", 1)
    builder.add_entry("D", "E", 1)
    matrix = builder.build()
    return CondorcetOptimum[str].of(matrix)
