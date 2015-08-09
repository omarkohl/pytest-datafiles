"""
Tests for the pytest-datafiles pytest plugin
"""

import os
from py import path  # pylint: disable=E0611
import pytest


TEST_DIR = os.path.dirname(os.path.realpath(__file__))
FIXTURE_DIR = os.path.join(TEST_DIR, '_fixture_files')
FIXTURE_FILES = [
    os.path.join(FIXTURE_DIR, name)
    for name in [
        'huckleberry.txt',
        'random.bin',
        'sparrow.jpg',
        ]
    ]


@pytest.mark.datafiles(
    path.local(
        FIXTURE_FILES[0],  # huckleberry.txt
        )
    )
def test_single_file_pypath(datafiles):
    """
    Verify that a single file (py.path.local) is copied correctly
    """
    assert (datafiles / 'huckleberry.txt').check(file=1)
    assert 'Mark Twain' in (datafiles / 'huckleberry.txt').read_text('utf-8')


@pytest.mark.datafiles(FIXTURE_FILES[0])  # huckleberry.txt
def test_single_file_str(datafiles):
    """
    Verify that a single file (str) is copied correctly
    """
    assert (datafiles / 'huckleberry.txt').check(file=1)
    assert 'Mark Twain' in (datafiles / 'huckleberry.txt').read_text('utf-8')


@pytest.mark.datafiles(
    *[path.local(p) for p in FIXTURE_FILES]
    )
def test_multiple_files_pypath(datafiles):
    """
    Verify multiple files (py.path.local) are copied correctly
    """
    assert (datafiles / 'huckleberry.txt').check(file=1)
    assert (datafiles / 'random.bin').check(file=1)
    assert (datafiles / 'sparrow.jpg').check(file=1)
    assert len((datafiles).listdir()) == 3


@pytest.mark.datafiles(*FIXTURE_FILES)
def test_multiple_files_str(datafiles):
    """
    Verify multiple files (str) are copied correctly
    """
    assert (datafiles / 'huckleberry.txt').check(file=1)
    assert (datafiles / 'random.bin').check(file=1)
    assert (datafiles / 'sparrow.jpg').check(file=1)
    assert len((datafiles).listdir()) == 3


@pytest.mark.datafiles
def test_no_files1(datafiles):
    """
    Verify if datafiles marker is set but empty the directory is empty
    """
    assert len((datafiles).listdir()) == 0


def test_no_files2(datafiles):
    """
    Verify if datafiles marker is not set the directory is empty
    """
    assert len((datafiles).listdir()) == 0
