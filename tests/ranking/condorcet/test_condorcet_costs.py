import numpy as np

from ranking.condorcet.condorcet_subset_costs import CondorcetSubsetCosts
from ranking.condorcet.condorcet_matrix import CondorcetMatrixBuilder


def make_instance_5_complicated() -> CondorcetSubsetCosts[str]:
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
    return CondorcetSubsetCosts[str].of(matrix)


def test_items():
    costs = make_instance_5_complicated()
    assert costs.items == ("A", "B", "C", "D", "E")


def test_num_items():
    costs = make_instance_5_complicated()
    assert costs.num_items == 5


def test_split_costs():
    costs = make_instance_5_complicated()
    expected = np.array([0,3,516,515,384,385,772,769,48,50,532,530,416,416,772,768,72,67,76,67,200,193,76,65,56,50,28,18,168,160,12,0])
    assert np.array_equal(costs.split_costs, expected)

    
def test_mask_sizes():
    costs = make_instance_5_complicated()
    expected = np.array([0,1,1,2,1,2,2,3,1,2,2,3,2,3,3,4,1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5])
    assert np.array_equal(costs.mask_sizes, expected)


def test_incremental_cost():
    costs = make_instance_5_complicated()
    expected = [
        [0,-99,4,-99,0,-99,4,-99,0,-99,4,-99,0,-99,4,-99,8,-99,12,-99,8,-99,12,-99,8,-99,12,-99,8,-99,12,-99],
        [0,0,-99,-99,128,128,-99,-99,32,32,-99,-99,160,160,-99,-99,0,0,-99,-99,128,128,-99,-99,32,32,-99,-99,160,160,-99,-99],
        [0,2,0,2,-99,-99,-99,-99,16,18,16,18,-99,-99,-99,-99,0,2,0,2,-99,-99,-99,-99,16,18,16,18,-99,-99,-99,-99],
        [0,1,0,1,0,1,0,1,-99,-99,-99,-99,-99,-99,-99,-99,64,65,64,65,64,65,64,65,-99,-99,-99,-99,-99,-99,-99,-99],
        [0,0,512,512,256,256,768,768,0,0,512,512,256,256,768,768,-99,-99,-99,-99,-99,-99,-99,-99,-99,-99,-99,-99,-99,-99,-99,-99]
    ]
    for bit, row in enumerate(expected):
        for mask, entry in enumerate(row):
            if entry != -99:
                assert costs.incremental_cost(bit, mask) == entry


def test_optimal_cost():
    costs = make_instance_5_complicated()
    expected = [0,0,0,0,0,0,0,2,0,0,0,1,0,0,0,3,0,0,0,0,0,2,0,2,0,0,32,32,16,18,48,50]
    for mask, entry in enumerate(expected):
        assert costs.optimal_cost(mask) == entry
    assert costs.optimal_cost() == expected[-1]


def test_mask_to_items():
    costs = make_instance_5_complicated()
    assert costs.mask_to_items(0) == ()
    assert costs.mask_to_items(1) == ("A",)
    assert costs.mask_to_items(11) == ("A", "B", "D")
    assert costs.mask_to_items(31) == ("A", "B", "C", "D", "E")
