import pandas as pd
import pandas.testing as pdt

from util.nppd.table_head_tail import TableHeadTail

TEST_ENTRIES = list(range(10))
TEST_COL = "test_col"
TEST_DF = pd.DataFrame({TEST_COL: TEST_ENTRIES})


def test_defauls():
    df = TEST_DF
    fmt = TableHeadTail()
    pdt.assert_frame_equal(fmt.format(df), df)


def test_constructor():
    df = TEST_DF
    fmt = TableHeadTail(head=3, tail=2)
    df_fmtd = fmt.format(df)
    assert len(df_fmtd) == 6
    assert tuple(df.head(3)[TEST_COL]) == tuple(df_fmtd.head(3)[TEST_COL])
    assert tuple(df.tail(2)[TEST_COL]) == tuple(df_fmtd.tail(2)[TEST_COL])


def test_override():
    df = TEST_DF
    fmt = TableHeadTail(head=3, tail=2)
    df_fmtd = fmt.format(df, head=2, tail=4)
    assert len(df_fmtd) == 7
    assert tuple(df.head(2)[TEST_COL]) == tuple(df_fmtd.head(2)[TEST_COL])
    assert tuple(df.tail(4)[TEST_COL]) == tuple(df_fmtd.tail(4)[TEST_COL])
