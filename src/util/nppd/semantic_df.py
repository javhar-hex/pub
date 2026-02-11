from __future__ import annotations

import dataclasses as dc

import numpy as np
import pandas as pd

from util.nppd.table import Table


@dc.dataclass(frozen=True)
class SemanticDf(Table):
    """
    Wrapper around a Pandas dataframe, providing shallow immutability. The `col()` and
    `df()` methods return deep copies; the `cols()` and `rows()` methods return another
    `SemanticDf`. In either case, the underlying dataframe will not be mutated.
    """

    _df: pd.DataFrame

    def col(self, header: str) -> pd.Series:
        """
        Deep copy of the column named `header` as a `pd.Series`. The column can be a
        regular column, the index column, or part of a multi-index.
        """
        if header in self._df.columns:
            return self._df.loc[:, header].copy(deep=True)
        if header in (self._df.index.names or []):
            level = self._df.index.get_level_values(header)
            return pd.Series(level, index=self._df.index, name=header)
        raise ValueError(f"Column {header} not found in columns or index.")

    def df(self) -> pd.DataFrame:
        """
        Deep copy of the dataframe as a `pd.DataFrame`.
        """
        return self._df.copy(deep=True)

    def cols(self, *headers: str) -> SemanticDf:
        """
        Selected columns as a new `SemanticDf`. No data is copied.
        """
        return SemanticDf(self._df.loc[:, list(headers)])

    def rows(self, rows: pd.Series | np.ndarray) -> SemanticDf:
        """
        Selected rows as a new `SemanticDf`. No data is copied.
        """
        return SemanticDf(self._df.loc[rows])
