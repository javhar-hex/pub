import random
import pandas as pd
import pytest
import os

from util.db.io_github import GitHubIo
import pandas.testing as pdt


REQUIRED = ["GITHUB_TEST_OWNER", "GITHUB_TEST_REPO", "GITHUB_TEST_BRANCH", "GITHUB_TEST_TOKEN", "GITHUB_TEST_FOLDER"]
missing = [k for k in REQUIRED if not os.getenv(k)]
pytestmark = pytest.mark.skipif(len(missing) > 0, reason=f"Missing env vars: {', '.join(missing)}")


def _github_io(include_folder: bool):
    owner  = os.environ["GITHUB_TEST_OWNER"]
    repo   = os.environ["GITHUB_TEST_REPO"]      # the *separate test repo*
    branch = os.environ["GITHUB_TEST_BRANCH"]
    folder = os.environ["GITHUB_TEST_FOLDER"]
    token  = os.environ["GITHUB_TEST_TOKEN"]

    if include_folder:
        return GitHubIo(pat=token, owner=owner, repo=repo, branch=branch, folder=folder)
    else:
        return GitHubIo(pat=token, owner=owner, repo=repo, branch=branch)
    
def _test_df():
    r = random.randrange(1000000)
    return pd.DataFrame({"a": ["a3", "a2", "a1"], "b": [0, 1, r]}).sort_values(by=["a"])

def test_round_trip_include_folder():
    github_io = _github_io(include_folder=True)
    test_df = _test_df()
    filename = "test.csv"

    _ = github_io.upload(test_df, filename, include_index=True, message="github io test round trip include folder")
    return_df = github_io.download(filename, index_col=0)

    pdt.assert_frame_equal(return_df, test_df, check_dtype=False)

def test_round_trip_exclude_folder():
    github_io = _github_io(include_folder=False)
    test_df = _test_df()
    filename = "test.csv"
    folder = "data/test"

    with pytest.raises(ValueError):
        _ = github_io.upload(test_df, filename, include_index=True, message="github io test round trip include folder")
    _ = github_io.upload(test_df, filename, folder=folder, include_index=True)

    with pytest.raises(ValueError):
        return_df = github_io.download(filename)
    return_df = github_io.download(filename, folder=folder, index_col=0)

    pdt.assert_frame_equal(return_df, test_df, check_dtype=False)

def test_round_trip_no_index():
    github_io = _github_io(include_folder=True)
    test_df = _test_df()
    filename = "test.csv"

    _ = github_io.upload(test_df, filename, include_index=False, message="github io test round trip include folder")
    return_df = github_io.download(filename)

    pdt.assert_frame_equal(
        return_df.reset_index(drop=True), 
        test_df.reset_index(drop=True), 
        check_dtype=False
    )
