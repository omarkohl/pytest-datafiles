"""Example: make a subset of the files in a dir available.

Now for another use case: let's say in the directory where your tests are
located, you place a directory named *test_files*. Here you have a lot of
images you want to run tests on. By using this plugin, you make sure the
original files under *test_files* are not modified by every test.

"""

from pathlib import Path

import pytest

# Dir containing 8 files
FIXTURE_DIR = Path(__file__).parent.resolve() / "test_files"


@pytest.mark.datafiles(
    FIXTURE_DIR / "img1.jpg",
    FIXTURE_DIR / "img2.jpg",
    FIXTURE_DIR / "img3.jpg",
)
def test_find_borders(datafiles):
    """Work with a copy of only 3 files."""
    for img in datafiles.iterdir():
        print(img)
        # assert process(img) == some_expected_value

        # and only the referenced files are available
        assert img.name != "img4.jpg"

    assert len(list(datafiles.iterdir())) == 3


@pytest.mark.datafiles(
    FIXTURE_DIR / "img4.jpg",
    FIXTURE_DIR / "img5.jpg",
)
def test_brightness(datafiles):
    """Work with a copy of only 2 files."""
    for img in datafiles.iterdir():
        print(img)
        # assert process(img) == some_expected_value

        # and only the referenced files are available
        assert img.name != "img3.jpg"

    assert len(list(datafiles.iterdir())) == 2


@pytest.mark.datafiles(FIXTURE_DIR)
def test_resize(datafiles):
    """Work with a copy of all files."""
    for img in datafiles.iterdir():
        print(img)
        # assert process(img) == some_expected_value

    assert len(list(datafiles.iterdir())) == 8
