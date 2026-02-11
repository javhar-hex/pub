from abc import ABC, abstractmethod

import pandas as pd

class Table(ABC):
    """
    Abstract base class for a table, requiring just a `column()` method that returns a
    Pandas series.
    """
    @abstractmethod
    def col(self, header: str) -> pd.Series: ...