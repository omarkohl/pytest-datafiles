"""Upgrade to v3."""

import os
from pathlib import Path

import py
import pytest

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "test_files",
)

FIXTURE_DIR_NEW_STYLE = Path(__file__).parent.resolve() / "test_files"


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "img1.jpg"))
def test_convert_to_pypath(datafiles):
    """
    If your tests are taking advantage of py.path the simplest change
    you can make is at the top of each test convert the pathlib.Path
    object back to a py.path .

    Note that it would be better to migrate to pathlib.Path, as shown in
    the next example, because py.path is deprecated.
    """

    # changing the type back to py.path as a quick fix
    datafiles = py.path.local(str(datafiles))

    # code remains as before
    assert len(datafiles.listdir()) == 1
    assert (datafiles / "img1.jpg").check(file=1)


@pytest.mark.datafiles(FIXTURE_DIR_NEW_STYLE / "img1.jpg")
def test_update_to_pathlib(datafiles):
    """Upgrade code to use `pathlib`.

    Some examples showing `pathlib` style.
    """

    # For demo purpose: this is the old-style
    pypath_datafiles = py.path.local(str(datafiles))

    # old style
    assert len(pypath_datafiles.listdir()) == 1
    assert (pypath_datafiles / "img1.jpg").check(file=1)

    # new style  # pylint: disable=R0801
    assert len(list(datafiles.iterdir())) == 1
    assert (datafiles / "img1.jpg").is_file()


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "img1.jpg"))
def test_keep_using_str(datafiles):
    """Keep using plain `os`.

    Nothing changes.
    """

    path = str(datafiles)
    assert len(os.listdir(path)) == 1
    assert os.path.isfile(os.path.join(path, "img1.jpg"))
