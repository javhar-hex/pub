import pandas as pd
import pytest

from util.nppd.semantic_df import SemanticDf

NUM_COL = "nums"
NUM_VALS = (0, 1, 2, 3, 4)
CHAR_COL = "chars"
CHAR_VALS = ("a", "b", "c", "d", "e")
TEST_DF = pd.DataFrame(
    {NUM_COL: NUM_VALS, CHAR_COL: CHAR_VALS, "bools": [True, False, True, False, True]}
)


def make_sdf():
    return SemanticDf(TEST_DF.copy())


def test_col():
    sdf = make_sdf()
    col = sdf.col(NUM_COL)
    assert col.name == NUM_COL
    assert tuple(col.values) == NUM_VALS

    col = sdf.col(CHAR_COL)
    assert col.name == CHAR_COL
    assert tuple(col.values) == CHAR_VALS

def test_col_from_single_index():
    df = TEST_DF.copy().set_index(CHAR_COL, drop=True)
    with pytest.raises(KeyError):
        df[CHAR_COL]
    sdf = SemanticDf(df)
    col = sdf.col(CHAR_COL)
    assert col.name == CHAR_COL
    assert tuple(col.values) == CHAR_VALS

def test_col_from_multi_index():
    df = TEST_DF.copy().set_index([NUM_COL, CHAR_COL], drop=True)
    with pytest.raises(KeyError):
        df[CHAR_COL]
    sdf = SemanticDf(df)
    col = sdf.col(CHAR_COL)
    assert col.name == CHAR_COL
    assert tuple(col.values) == CHAR_VALS

def test_col_immutability():
    sdf = make_sdf()
    col = sdf.col(NUM_COL)
    col[2] = "x"
    assert tuple(col.values) != CHAR_VALS
    assert tuple(sdf.col(CHAR_COL)) == CHAR_VALS


def test_df():
    sdf = make_sdf()
    df = sdf.df()
    assert df.shape == TEST_DF.shape
    assert all(df[NUM_COL] == TEST_DF[NUM_COL])
    assert all(df[CHAR_COL] == TEST_DF[CHAR_COL])


def test_df_immutability():
    sdf = make_sdf()
    df = sdf.df()
    df.loc[1, NUM_COL] = 99
    assert not all(df[NUM_COL] == TEST_DF[NUM_COL])
    assert all(sdf.col(CHAR_COL) == TEST_DF[CHAR_COL])


def test_cols():
    sdf = make_sdf()
    sdf_cols = sdf.cols(NUM_COL, CHAR_COL)
    assert sdf_cols.df().shape[1] == 2
    assert all(sdf.col(NUM_COL) == TEST_DF[NUM_COL])
    assert all(sdf.col(CHAR_COL) == TEST_DF[CHAR_COL])


def test_rows():
    sdf = make_sdf()
    vals = [1, 3]
    idx = sdf.col(NUM_COL).isin(vals)
    sdf_rows = sdf.rows(idx)
    assert sdf_rows.df().shape[1] == TEST_DF.shape[1]
    assert tuple(sdf_rows.col(NUM_COL)) == tuple(vals)
