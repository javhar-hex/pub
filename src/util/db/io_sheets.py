from typing import Optional, Sequence, Union

import pandas as pd

IndexCol = Optional[Union[int, str, Sequence[int], Sequence[str]]]


def df_from_sheet(url: str, index_col: IndexCol = None) -> pd.DataFrame:
    req_url = url.replace("/edit?gid=", "/gviz/tq?tqx=out:csv&gid=")
    return pd.read_csv(
        req_url,
        engine="python",
        dtype=str,
        na_filter=False,
        keep_default_na=False,
        index_col=index_col,
    )
