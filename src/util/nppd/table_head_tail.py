import dataclasses as dc
from typing import Optional

import pandas as pd


@dc.dataclass(frozen=True)
class TableHeadTail:
    """
    Simple formatter for dataframes, combining `df.head()` and `df.tail()`. Allows a
    default head and tail length in the constructor, and optional head and/or tail
    overrides in the `format()` method.
    """
    ellipsis: str = "…"
    head: int = 8
    tail: int = 8

    def format(
        self, df: pd.DataFrame, head: Optional[int] = None, tail: Optional[int] = None
    ) -> pd.DataFrame:
        head = self.head if head is None else head
        tail = self.tail if tail is None else tail

        if len(df) <= head + tail:
            return df

        ellipsis_row = pd.DataFrame({c: [self.ellipsis] for c in df.columns})
        ellipsis_row.index = pd.Index([self.ellipsis], name=df.index.name)

        return pd.concat([df.head(head), ellipsis_row, df.tail(tail)])
