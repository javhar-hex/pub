from __future__ import annotations

import dataclasses as dc
from typing import Iterable, Tuple

import pandas as pd


@dc.dataclass(frozen=True)
class Categorical:
    """
    Wrapper for Panda's categorical dtype, can provide sanity checks.
    """
    categories: Tuple[str, ...]

    def normalize(self, df: pd.DataFrame, col: str) -> pd.DataFrame:
        """
        Cast the given col to this categorical dtype, in-place.
        """
        df[col] = self.cast(df[col])
        return df

    def cast(self, series: pd.Series) -> pd.Series:
        """
        Cast the pd.Series to the cateorical datatype. Raise `ValueError` if there are
        unrecognized values.
        """
        dtype = pd.CategoricalDtype(list(self.categories), ordered=False)
        typed = series.astype(dtype)
        unrecognized = list(series[typed.isna()].unique())
        if len(unrecognized) > 0:
            raise ValueError(
                f"Unrecognized values {unrecognized} for categories {self.categories}."
            )
        return typed

    @classmethod
    def of(cls, categories: Iterable[str]) -> Categorical:
        return cls(tuple(categories))
