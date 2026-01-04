"""Example: use `str` paths."""

import os

import pytest

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_files")


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, "img1.jpg"),
    os.path.join(FIXTURE_DIR, "img2.jpg"),
    os.path.join(FIXTURE_DIR, "img3.jpg"),
)
def test_str(datafiles):
    """Work with `str`."""
    assert len(list(datafiles.iterdir())) == 3
