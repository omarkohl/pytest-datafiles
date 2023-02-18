"""Upgrade to v3."""
import os

import pytest
import py


@pytest.mark.datafiles('/tmp/big_files/film1.mp4')
def test_convert_to_pypath(datafiles):
    """Convert `datafiles` to `py.path` in place.

    Changing the type back to py.path - should be avoided!

    Better to update the tests to make use of `pathlib`.
    """

    # changing the type back to py.path - should be avoided
    datafiles = py.path.local(str(datafiles))

    # code remains as before
    assert len(datafiles.listdir()) == 1
    assert (datafiles / 'film1.mp4').check(file=1)


@pytest.mark.datafiles('/tmp/big_files/film1.mp4')
def test_update_to_pathlib(datafiles):
    """Upgrade code to use `pathlib`.

    Some examples showing `pathlib` style.
    """

    # For demo purpose: this is the old-style
    pypath_datafiles = py.path.local(str(datafiles))

    # old style
    assert len(pypath_datafiles.listdir()) == 1
    assert (pypath_datafiles / 'film1.mp4').check(file=1)

    # new style  # pylint: disable=R0801
    assert len(list(datafiles.iterdir())) == 1
    assert (datafiles / 'film1.mp4').is_file()


@pytest.mark.datafiles('/tmp/big_files/film1.mp4')
def test_keep_using_str(datafiles):
    """Keep using plain `os`.

    Nothing changes.
    """

    path = str(datafiles)
    assert len(os.listdir(path)) == 1
    assert os.path.isfile(os.path.join(path, 'film1.mp4'))
