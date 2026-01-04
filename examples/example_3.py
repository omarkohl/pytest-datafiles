"""Example: re-use file selection.

If all (or many) of your tests rely on the same files it can be easier to
define one decorator beforehand and apply it to every test.
"""

from pathlib import Path

import pytest

FIXTURE_DIR = Path(__file__).parent.resolve() / "test_files"

ALL_IMGS = pytest.mark.datafiles(
    FIXTURE_DIR / "img1.jpg",
    FIXTURE_DIR / "img2.jpg",
    FIXTURE_DIR / "img3.jpg",
    FIXTURE_DIR / "img4.jpg",
    FIXTURE_DIR / "img5.jpg",
    FIXTURE_DIR / "img6.jpg",
    FIXTURE_DIR / "img7.jpg",
    FIXTURE_DIR / "img8.jpg",
)


@ALL_IMGS
def test_something1(datafiles):
    """Work with copy of all files."""
    for img in datafiles.iterdir():
        print(img)
        # assert process(img) == some_expected_value

    assert len(list(datafiles.iterdir())) == 8

    # we can do something destructive
    (datafiles / "img3.jpg").unlink()
    assert len(list(datafiles.iterdir())) == 7


@ALL_IMGS
def test_something2(datafiles):
    """Work with copy of all files."""
    for img in datafiles.iterdir():
        print(img)
        # assert process(img) == some_expected_value

    assert len(list(datafiles.iterdir())) == 8

    # we can do something destructive
    (datafiles / "img1.jpg").unlink()
    assert len(list(datafiles.iterdir())) == 7
