from ranking.dtypes.split import Split
from ranking.condorcet.condorcet_splits import CondorcetSplits


def test_condorcet_splits_factory():
    splits = CondorcetSplits[str].of_tails(
        cost=3.14, tails=[["A", "C"], ["B", "C"]], items=["A", "B", "C", "D", "E"]
    )
    assert splits.cost == 3.14
    assert len(splits.splits) == 2
    expected = {
        Split[str].of(head=["B", "D", "E"], tail=["A", "C"]),
        Split[str].of(head=["A", "D", "E"], tail=["B", "C"]),
    }
    for split in splits.splits:
        assert split in expected
