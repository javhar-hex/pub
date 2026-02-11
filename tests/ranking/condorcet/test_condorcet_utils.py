import numpy as np


from ranking.condorcet.condorcet_matrix import CondorcetMatrix
from ranking.condorcet.condorcet_utils import ranking_cost, split_cost
from ranking.dtypes.ranking import Ranking
from ranking.dtypes.split import Split
from util.nppd.frozen_nd_array import FrozenNdArray


def test_ranking_violation():
    items = ("A", "B", "C")
    mx = np.array([[0, 1, -2], [-1, 0, 4], [2, -4, 0]])
    matrix = CondorcetMatrix[str](items, FrozenNdArray(mx))

    ranking = Ranking[str].of(("A", "B", "C"))
    assert ranking_cost(ranking, matrix) == 2

    ranking = Ranking[str].of(("A", "C", "B"))
    assert ranking_cost(ranking, matrix) == 6

    ranking = Ranking[str].of(("B", "A", "C"))
    assert ranking_cost(ranking, matrix) == 3

    ranking = Ranking[str].of(("B", "C", "A"))
    assert ranking_cost(ranking, matrix) == 1

    ranking = Ranking[str].of(("C", "A", "B"))
    assert ranking_cost(ranking, matrix) == 4

    ranking = Ranking[str].of(("C", "B", "A"))  # type: ignore
    assert ranking_cost(ranking, matrix) == 5


def test_split_violation():
    items = ("A", "B", "C")
    mx = np.array([[0, 1, -2], [-1, 0, 4], [2, -4, 0]])
    matrix = CondorcetMatrix[str](items, FrozenNdArray(mx))

    split = Split[str].of(("A"), ("B", "C"))
    assert split_cost(split, matrix) == 2

    split = Split[str].of(("B"), ("A", "C"))
    assert split_cost(split, matrix) == 1

    split = Split[str].of(("C"), ("A", "B"))
    assert split_cost(split, matrix) == 4

    split = Split[str].of(("A", "B"), ("C"))
    assert split_cost(split, matrix) == 2

    split = Split[str].of(("A", "C"), ("B"))
    assert split_cost(split, matrix) == 4

    split = Split[str].of(("B", "C"), ("A"))
    assert split_cost(split, matrix) == 1
