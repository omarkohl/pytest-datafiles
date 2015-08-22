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


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, 'dir1'))
def test_single_dir_str(datafiles):
    """
    Verify that a single directory (specified as a string) is copied correctly.

    The content of the directory is copied.
    """
    assert len(datafiles.listdir()) == 3
    assert (datafiles / 'file1').check(file=1)
    assert (datafiles / 'file2').check(file=1)
    assert (datafiles / 'file3').check(file=1)


@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'dir1'),
    os.path.join(FIXTURE_DIR, 'dir2'),
    )
def test_multi_dir_str(datafiles):
    """
    Verify that multiple directories (strings) are copied correctly.

    The content of the directories is copied.
    """
    assert len(datafiles.listdir()) == 6
    # files from dir1
    assert (datafiles / 'file1').check(file=1)
    assert (datafiles / 'file2').check(file=1)
    assert (datafiles / 'file3').check(file=1)
    # files from dir2
    assert (datafiles / 'file4').check(file=1)
    assert (datafiles / 'file5').check(file=1)
    assert (datafiles / 'file6').check(file=1)


@pytest.mark.datafiles(
    path.local(FIXTURE_DIR) / 'dir1',
    path.local(FIXTURE_DIR) / 'dir2',
    path.local(FIXTURE_DIR) / 'dir3',
    )
def test_multi_dir_overwrite(datafiles):
    """
    Verify files with the same name are overwritten

    When copying from multiple directories if files have the same name they are
    overwritten by the last occurence.
    """
    assert len(datafiles.listdir()) == 6
    # file1 and file4 appear twice and are overwritten by the one in dir3
    assert (datafiles / 'file1').read() == "dir3\n123\n"
    assert (datafiles / 'file2').read() == "dir1\n456\n"
    assert (datafiles / 'file3').read() == "dir1\n789\n"
    assert (datafiles / 'file4').read() == "dir3\n101112\n"
    assert (datafiles / 'file5').read() == "dir2\n131415\n"
    assert (datafiles / 'file6').read() == "dir2\n161718\n"


@pytest.mark.datafiles(
    path.local(FIXTURE_DIR) / 'dir1',
    path.local(FIXTURE_FILES[0]),  # huckleberry.txt
    path.local(FIXTURE_DIR) / 'dir4',
    path.local(FIXTURE_FILES[1]),  # random.bin
    )
def test_multiple(datafiles):
    """
    Verify multiple files and directories (with subdirectories) are copied
    """
    assert len(datafiles.listdir()) == 7
    assert (datafiles / 'huckleberry.txt').check(file=1)
    assert (datafiles / 'random.bin').check(file=1)
    assert (datafiles / 'file1').check(file=1)
    assert (datafiles / 'file2').check(file=1)
    assert (datafiles / 'file3').check(file=1)
    assert (datafiles / 'subdir1').check(dir=1)
    assert (datafiles / 'subdir2').check(dir=1)
    assert (datafiles / 'subdir1' / 'file1').check(file=1)
    assert (datafiles / 'subdir1' / 'file1').check(file=1)
    assert (datafiles / 'subdir2' / 'file2').check(file=1)
    assert (datafiles / 'subdir2' / 'file2').check(file=1)