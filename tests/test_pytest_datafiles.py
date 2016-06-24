"""
Tests for the pytest-datafiles pytest plugin
"""

import os
from py import path  # pylint: disable=E0611
import pytest


pytest_plugins = 'pytester'


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


@pytest.mark.datafiles(
    path.local(FIXTURE_DIR) / 'dir1',
    path.local(FIXTURE_DIR) / 'dir2',
    keep_top_dir=True,
    )
def test_keep_top_dir(datafiles):
    """
    Verify top level directory is kept (instead of only copying the content)
    """
    assert len(datafiles.listdir()) == 2
    assert (datafiles / 'dir1').check(dir=1)


@pytest.mark.datafiles(
    path.local(FIXTURE_DIR) / 'dir1',
    path.local(FIXTURE_DIR) / 'dir2',
    path.local(FIXTURE_DIR) / 'dir3',
    on_duplicate='ignore',
    )
def test_on_duplicate_ignore_dir_with_file(datafiles):
    """
    Verify duplicate files are ignored (i.e. the first one is kept)

    If duplicate files appear (to be copied) then the duplicates are ignored
    and the first occurence is kept. In this example the file 'file1' appears
    both in dir1 and dir3 and 'file4' appears both in dir2 and dir3.
    """
    assert len(datafiles.listdir()) == 6
    assert (datafiles / 'file1').read() == "dir1\n123\n"
    assert (datafiles / 'file4').read() == "dir2\n101112\n"


@pytest.mark.datafiles(
    path.local(FIXTURE_DIR) / 'dir1',
    path.local(FIXTURE_DIR) / 'dir2',
    path.local(FIXTURE_DIR) / 'dir3',
    on_duplicate='overwrite',
    )
def test_on_duplicate_overwrite(datafiles):
    """
    Verify duplicate files are overwritten (i.e. the last one is kept)

    If duplicate files appear (to be copied) then the duplicates are
    overwritten and the first last is kept. In this example the file 'file1'
    appears both in dir1 and dir3 and 'file4' appears both in dir2 and dir3.
    """
    assert len(datafiles.listdir()) == 6
    assert (datafiles / 'file1').read() == "dir3\n123\n"
    assert (datafiles / 'file4').read() == "dir3\n101112\n"


def test_on_duplicate_exception(testdir):
    """
    Verify that a ValueError is raised when duplicate files appear

    This is the default behaviour.

    If duplicate files appear (to be copied) then a ValueError is raised. In
    this example the file 'file1' appears both in dir1 and dir3 and 'file4'
    appears both in dir2 and dir3.
    """
    testdir.makepyfile('''
        import pytest
        from py import path

        FIXTURE_DIR = '{0}'

        @pytest.mark.datafiles(
            path.local(FIXTURE_DIR) / 'dir1',
            path.local(FIXTURE_DIR) / 'dir2',
            path.local(FIXTURE_DIR) / 'dir3',
            )
        def test_ode(datafiles):
            assert len(datafiles.listdir()) == 6
    '''.format(FIXTURE_DIR))
    result = testdir.runpytest('-s')
    result.stdout.fnmatch_lines(["E*ValueError:*file1'*already exists*"])


def test_on_duplicate_exception2(testdir):
    """
    Verify that a ValueError is raised when duplicate files appear
    """
    testdir.makepyfile('''
        import pytest
        from py import path

        FIXTURE_DIR = '{0}'

        @pytest.mark.datafiles(
            path.local(FIXTURE_DIR) / 'dir1' / 'file1',
            path.local(FIXTURE_DIR) / 'dir3' / 'file1',
            )
        def test_ode(datafiles):
            assert len(datafiles.listdir()) == 2
    '''.format(FIXTURE_DIR))
    result = testdir.runpytest('-s')
    result.stdout.fnmatch_lines(["E*ValueError:*file1'*already exists*"])


def test_on_duplicate_exception_dir(testdir):
    """
    Verify that a ValueError is raised when duplicate directories appear

    This is the default behaviour.

    If duplicate files appear (to be copied) then a ValueError is raised. In
    this example the directory 'subdir1' appears twice.
    """
    testdir.makepyfile('''
        import pytest
        from py import path

        FIXTURE_DIR = '{0}'

        @pytest.mark.datafiles(
            path.local(FIXTURE_DIR) / 'dir4' / 'subdir1',
            path.local(FIXTURE_DIR) / 'dir5' / 'subdir1',
            keep_top_dir=True,
            )
        def test_duplicate_dir(datafiles):
            assert True
    '''.format(FIXTURE_DIR))
    result = testdir.runpytest('-s')
    result.stdout.fnmatch_lines(["E*ValueError:*subdir1'*already exists*"])


@pytest.mark.datafiles(
    path.local(FIXTURE_DIR) / 'dir4' / 'subdir1',
    path.local(FIXTURE_DIR) / 'dir5' / 'subdir1',
    keep_top_dir=True,
    on_duplicate='ignore',
    )
def test_on_duplicate_ignore_dir(datafiles):
    """
    Verify that the second (duplicate) directory is ignored.
    """
    assert (datafiles / 'subdir1' / 'file1').check(file=1)


@pytest.mark.datafiles(
    path.local(FIXTURE_DIR) / 'dir1' / 'file1',
    path.local(FIXTURE_DIR) / 'dir3' / 'file1',
    on_duplicate='ignore',
    )
def test_on_duplicate_ignore_file(datafiles):
    """
    Verify on_duplicate=ignore causes the first file to be used
    """
    assert (datafiles / 'file1').check(file=1)
    assert (datafiles / 'file1').read() == "dir1\n123\n"


def test_non_existing_file(testdir):
    """
    Verify exception is raised if file doesn't exist.
    """
    testdir.makepyfile('''
        import pytest
        from py import path

        FIXTURE_DIR = '{0}'

        @pytest.mark.datafiles(
            path.local(FIXTURE_DIR) / 'fileZZ',
            )
        def test_ode(datafiles):
            assert len(datafiles.listdir()) == 1
    '''.format(FIXTURE_DIR))
    result = testdir.runpytest('-s')
    result.stdout.fnmatch_lines([
        "E*ValueError:*fileZZ'*is neither file nor dir.*",
        ])


def test_invalid_keep_top_dir(testdir):
    """
    Verify ValueError is raised if parameter isn't boolean
    """
    testdir.makepyfile('''
        import pytest
        from py import path

        FIXTURE_DIR = '{0}'

        @pytest.mark.datafiles(
            path.local(FIXTURE_DIR) / 'fileZZ',
            keep_top_dir='invalid-value',
            )
        def test_invalid_param(datafiles):
            assert True
    '''.format(FIXTURE_DIR))
    result = testdir.runpytest('-s')
    result.stdout.fnmatch_lines([
        "E*ValueError: 'keep_top_dir' must be True or False*",
        ])


def test_invalid_on_duplicate(testdir):
    """
    Verify ValueError is raised if parameter isn't boolean
    """
    testdir.makepyfile('''
        import pytest
        from py import path

        FIXTURE_DIR = '{0}'

        @pytest.mark.datafiles(
            path.local(FIXTURE_DIR) / 'fileZZ',
            on_duplicate='invalid-value',
            )
        def test_invalid_param(datafiles):
            assert True
    '''.format(FIXTURE_DIR))
    result = testdir.runpytest('-s')
    result.stdout.fnmatch_lines([
        "E*ValueError: 'on_duplicate' must be 'exception', 'ignore' or *",
        ])
