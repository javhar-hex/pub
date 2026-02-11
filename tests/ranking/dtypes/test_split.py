from ranking.dtypes.split import Split


def test_condorcet_split_factory():
    split = Split[str].of(head=("A", "B"), tail=("C", "D", "E"))
    assert set(split.head) == {"A", "B"}
    assert set(split.tail) == {"C", "D", "E"}
