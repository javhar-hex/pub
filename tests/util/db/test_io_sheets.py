import pytest
from util.db.io_sheets import df_from_sheet
import os


TEST_URL = "https://docs.google.com/spreadsheets/d/170-9hL9RiodvRLpLVfQUHpwLVYeRG1Ho-eZjN1gNCK4/edit?gid=587177675#gid=587177675"
TEST_ENV = "TEST_GOOGLE_SHEETS"

pytestmark = pytest.mark.skipif(
    not os.getenv(TEST_ENV), 
    reason=f"Missing env var: {TEST_ENV}")



def test_from_sheet():
    df = df_from_sheet(TEST_URL)
    assert tuple(df.columns) == ("idx", "a", "b")
    assert tuple(df["idx"]) == ("2", "0", "1")
    assert tuple(df["a"]) == ("a1", "a2", "a3")
    assert tuple(df["b"]) == ("b3", "b2", "b1")


def test_with_index_num():
    df = df_from_sheet(TEST_URL, index_col=0)
    assert tuple(df.columns) == ("a", "b")
    assert df.index.name == "idx"
    assert tuple(df.index) == (2, 0, 1)
    assert tuple(df["a"]) == ("a1", "a2", "a3")
    assert tuple(df["b"]) == ("b3", "b2", "b1")


def test_with_index_name():
    df = df_from_sheet(TEST_URL, index_col="a")
    assert tuple(df.columns) == ("idx", "b")
    assert df.index.name == "a"
    assert tuple(df["idx"]) == ("2", "0", "1")
    assert tuple(df.index) == ("a1", "a2", "a3")
    assert tuple(df["b"]) == ("b3", "b2", "b1")
