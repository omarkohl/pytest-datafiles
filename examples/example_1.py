"""Example: Reference files anywhere.

One possible use case is when you are running tests on very big files that are
not included or packaged with your tests. For example, your test files are
large video files stored under */opt/big_files/* . You don't want your tests
modifying the original files, but the files are required by the tests.

"""

import os

import pytest


@pytest.mark.datafiles("/opt/big_files/film1.mp4")
def test_fast_forward(datafiles):
    """Work with a copy of the big file."""
    assert len(list(datafiles.iterdir())) == 1
    assert (datafiles / "film1.mp4").is_file()
    # assert some_operation(datafiles / 'film1.mp4') == expected_result


@pytest.mark.datafiles("/opt/big_files/film1.mp4")
def test_fast_forward_alternative(datafiles):
    """Work with a copy of the bigfile, using `str`."""
    path = str(datafiles)  # Convert from py.path object to path (str)
    assert len(os.listdir(path)) == 1
    assert os.path.isfile(os.path.join(path, "film1.mp4"))
    # assert some_operation(os.path.join(path, 'film1.mp4')) == expected_result
