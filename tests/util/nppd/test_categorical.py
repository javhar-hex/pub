


import pandas as pd
import pytest
from util.nppd.categorical import Categorical


def test_cast():
    cat = Categorical.of({"apple", "banana", "coconut"})
    vals = ("apple", "apple", "coconut", "banana", "apple")
    s = pd.Series(vals)
    assert tuple(cat.cast(s)) == vals
    assert isinstance(cat.cast(s).dtype, pd.CategoricalDtype)

def test_cat_illegal_val():
    cat = Categorical.of({"apple", "banana", "coconut"})
    s = pd.Series(("apple", "apple", "coconut", "banana", "grapefruit"))
    with pytest.raises(ValueError):
        cat.cast(s)

def test_normalize():
    cat = Categorical.of({"apple", "banana", "coconut"})
    colname = "col"
    vals = ("apple", "apple", "coconut", "banana", "apple")
    df = pd.DataFrame({colname: vals})
    assert not isinstance(df[colname].dtype, pd.CategoricalDtype)
    df = cat.normalize(df, colname)
    assert tuple(df[colname]) == vals
    assert isinstance(df[colname].dtype, pd.CategoricalDtype)
    
def test_normalize_illegal_val():
    cat = Categorical.of({"apple", "banana", "coconut"})
    colname = "col"
    vals = ("apple", "apple", "coconut", "banana", "grapefruit")
    df = pd.DataFrame({colname: vals})
    with pytest.raises(ValueError):
        cat.normalize(df, colname)
