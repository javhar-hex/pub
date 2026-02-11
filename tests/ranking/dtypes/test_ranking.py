from ranking.dtypes.ranking import Ranking


def test_constructor():
    items = ("A", "B", "C")
    ranking = Ranking[str].of(tuple(items))
    assert ranking.items == items

    ranking = Ranking[str].of(list(items))
    assert ranking.items == items
    

def test_len():
    ranking = Ranking[str].of(["A", "B", "C"])
    assert len(ranking) == 3


def test_indexing():
    items = ("A", "B", "C", "D")
    ranking = Ranking[str].of(tuple(items))
    assert ranking[0] == "A"
    assert ranking[1] == "B"
    assert ranking[2] == "C"
    assert ranking[3] == "D"
    assert ranking[:1] == ("A", )
    assert ranking[:2] == ("A", "B")
    assert ranking[-1] == "D"
    assert ranking[-2:] == ("C", "D")
    assert ranking[1:3] == ("B", "C")
