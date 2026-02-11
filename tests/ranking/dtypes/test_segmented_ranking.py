from ranking.dtypes.ranking import Ranking
from ranking.dtypes.segmented_ranking import SegmentedRankingBuilder


def test_builder_add_item():
    builder = SegmentedRankingBuilder[str]()
    builder.add_item("A").add_item("B")
    segmented_ranking = builder.build()
    assert len(segmented_ranking.segments) == 2
    assert set(segmented_ranking.segments[0]) == {Ranking[str].of(["A"])}
    assert set(segmented_ranking.segments[1]) == {Ranking[str].of(["B"])}

def test_builder_add_segment():
    builder = SegmentedRankingBuilder[str]()
    builder.add_segment([("B", "C", "D"), ("C", "D", "B")])
    segmented_ranking = builder.build()
    assert len(segmented_ranking.segments) == 1
    assert set(segmented_ranking.segments[0]) == {
        Ranking[str].of(["B", "C", "D"]),
        Ranking[str].of(["C", "D", "B"]),
    }

def test_builder_add_both():
    builder = SegmentedRankingBuilder[str]()
    builder.add_item("A")
    builder.add_segment([("B", "C", "D"), ("C", "D", "B")])
    builder.add_item("E")
    segmented_ranking = builder.build()
    assert len(segmented_ranking.segments) == 3
    assert set(segmented_ranking.segments[0]) == {Ranking[str].of(["A"])}
    assert set(segmented_ranking.segments[1]) == {
        Ranking[str].of(["B", "C", "D"]),
        Ranking[str].of(["C", "D", "B"]),
    }
    assert set(segmented_ranking.segments[2]) == {Ranking[str].of(["E"])}

def test_multiplicities():
    builder = SegmentedRankingBuilder[str]()
    builder.add_item("A")
    builder.add_segment([("B", "C", "D"), ("C", "D", "B")])
    builder.add_item("E")
    segmented_ranking = builder.build()
    assert segmented_ranking.multiplicities == (1, 2, 1)
    assert segmented_ranking.multiplicities == (1, 2, 1)

def test_arbitrary():
    builder = SegmentedRankingBuilder[str]()
    builder.add_item("A")
    builder.add_segment([("B", "C", "D"), ("C", "D", "B")])
    builder.add_item("E")
    segmented_ranking = builder.build()
    assert segmented_ranking.arbitrary() in {
        Ranking[str].of(["A", "B", "C", "D", "E"]),
        Ranking[str].of(["A", "C", "D", "B", "E"]),        
    }