"""
Tests for the pytest-datafiles pytest plugin
"""

import os
from pathlib import Path

import pytest

pytest_plugins = "pytester"  # pylint: disable=C0103


TEST_DIR = Path(__file__).parent.resolve()
FIXTURE_DIR = TEST_DIR / "_fixture_files"
FIXTURE_FILES = [
    FIXTURE_DIR / name
    for name in [
        "huckleberry.txt",
        "random.bin",
        "sparrow.jpg",
    ]
]


@pytest.mark.datafiles(FIXTURE_FILES[0])  # huckleberry.txt
def test_single_file_path(datafiles):
    """
    Verify that a single file (pathlib.Path) is copied correctly
    """
    assert (datafiles / "huckleberry.txt").is_file()
    assert "Mark Twain" in (datafiles / "huckleberry.txt").read_text("utf-8")


@pytest.mark.datafiles(str(FIXTURE_FILES[0]))  # huckleberry.txt
def test_single_file_str(datafiles):
    """
    Verify that a single file (str) is copied correctly
    """
    assert (datafiles / "huckleberry.txt").is_file()
    assert "Mark Twain" in (datafiles / "huckleberry.txt").read_text("utf-8")


@pytest.mark.datafiles(*FIXTURE_FILES)
def test_multiple_files_path(datafiles):
    """
    Verify multiple files (pathlib.Path) are copied correctly
    """
    assert (datafiles / "huckleberry.txt").is_file()
    assert (datafiles / "random.bin").is_file()
    assert (datafiles / "sparrow.jpg").is_file()
    assert len(list(datafiles.iterdir())) == 3


@pytest.mark.datafiles(*[str(f) for f in FIXTURE_FILES])
def test_multiple_files_str(datafiles):
    """
    Verify multiple files (str) are copied correctly
    """
    assert (datafiles / "huckleberry.txt").is_file()
    assert (datafiles / "random.bin").is_file()
    assert (datafiles / "sparrow.jpg").is_file()
    assert len(list(datafiles.iterdir())) == 3


@pytest.mark.datafiles(FIXTURE_FILES[0])
@pytest.mark.datafiles(FIXTURE_FILES[1])
@pytest.mark.datafiles(FIXTURE_FILES[2])
def test_multiple_marks(datafiles):
    """
    Verify multiple marks are combined
    """
    assert (datafiles / "huckleberry.txt").is_file()
    assert (datafiles / "random.bin").is_file()
    assert (datafiles / "sparrow.jpg").is_file()
    assert len(list(datafiles.iterdir())) == 3


@pytest.mark.datafiles
def test_no_files1(datafiles):
    """
    Verify if datafiles marker is set but empty the directory is empty
    """
    assert not list(datafiles.iterdir())


def test_no_files2(datafiles):
    """
    Verify if datafiles marker is not set the directory is empty
    """
    assert not list(datafiles.iterdir())


@pytest.mark.datafiles(os.path.join(str(FIXTURE_DIR), "dir1"))
def test_single_dir_str(datafiles):
    """
    Verify that a single directory (specified as a string) is copied correctly.

    The content of the directory is copied.
    """
    assert len(list(datafiles.iterdir())) == 3
    assert (datafiles / "file1").is_file()
    assert (datafiles / "file2").is_file()
    assert (datafiles / "file3").is_file()


@pytest.mark.datafiles(
    os.path.join(str(FIXTURE_DIR), "dir1"),
    os.path.join(str(FIXTURE_DIR), "dir2"),
)
def test_multi_dir_str(datafiles):
    """
    Verify that multiple directories (strings) are copied correctly.

    The content of the directories is copied.
    """
    assert len(list(datafiles.iterdir())) == 6
    # files from dir1
    assert (datafiles / "file1").is_file()
    assert (datafiles / "file2").is_file()
    assert (datafiles / "file3").is_file()
    # files from dir2
    assert (datafiles / "file4").is_file()
    assert (datafiles / "file5").is_file()
    assert (datafiles / "file6").is_file()


@pytest.mark.datafiles(
    FIXTURE_DIR / "dir1",
    FIXTURE_FILES[0],  # huckleberry.txt
    FIXTURE_DIR / "dir4",
    FIXTURE_FILES[1],  # random.bin
)
def test_multiple(datafiles):
    """
    Verify multiple files and directories (with subdirectories) are copied
    """
    assert len(list(datafiles.iterdir())) == 7
    assert (datafiles / "huckleberry.txt").is_file()
    assert (datafiles / "random.bin").is_file()
    assert (datafiles / "file1").is_file()
    assert (datafiles / "file2").is_file()
    assert (datafiles / "file3").is_file()
    assert (datafiles / "subdir1").is_dir()
    assert (datafiles / "subdir2").is_dir()
    assert (datafiles / "subdir1" / "file1").is_file()
    assert (datafiles / "subdir1" / "file1").is_file()
    assert (datafiles / "subdir2" / "file2").is_file()
    assert (datafiles / "subdir2" / "file2").is_file()


@pytest.mark.datafiles(
    FIXTURE_DIR / "dir1",
    FIXTURE_DIR / "dir2",
    keep_top_dir=True,
)
def test_keep_top_dir(datafiles):
    """
    Verify top level directory is kept (instead of only copying the content)
    """
    assert len(list(datafiles.iterdir())) == 2
    assert (datafiles / "dir1").is_dir()


@pytest.mark.datafiles(
    FIXTURE_DIR / "dir1",
    FIXTURE_DIR / "dir2",
    FIXTURE_DIR / "dir3",
    on_duplicate="ignore",
)
def test_on_duplicate_ignore_dir_with_file(datafiles):
    """
    Verify duplicate files are ignored (i.e. the first one is kept)

    If duplicate files appear (to be copied) then the duplicates are ignored
    and the first occurrence is kept. In this example the file 'file1' appears
    both in dir1 and dir3 and 'file4' appears both in dir2 and dir3.
    """
    assert len(list(datafiles.iterdir())) == 6
    assert (datafiles / "file1").read_text() == "dir1\n123\n"
    assert (datafiles / "file4").read_text() == "dir2\n101112\n"


@pytest.mark.datafiles(
    FIXTURE_DIR / "dir1",
    FIXTURE_DIR / "dir2",
    FIXTURE_DIR / "dir3",
    on_duplicate="overwrite",
)
def test_on_duplicate_overwrite(datafiles):
    """
    Verify duplicate files are overwritten (i.e. the last one is kept)

    If duplicate files appear (to be copied) then the duplicates are
    overwritten and the first last is kept. In this example the file 'file1'
    appears both in dir1 and dir3 and 'file4' appears both in dir2 and dir3.
    """
    assert len(list(datafiles.iterdir())) == 6
    assert (datafiles / "file1").read_text() == "dir3\n123\n"
    assert (datafiles / "file4").read_text() == "dir3\n101112\n"


def test_on_duplicate_exception(testdir):
    """
    Verify that a ValueError is raised when duplicate files appear

    This is the default behaviour.

    If duplicate files appear (to be copied) then a ValueError is raised. In
    this example the file 'file1' appears both in dir1 and dir3.
    """
    testdir.makepyfile(f"""
        import pytest
        from pathlib import Path

        FIXTURE_DIR = Path('{FIXTURE_DIR}')

        @pytest.mark.datafiles(
            FIXTURE_DIR / 'dir1',
            FIXTURE_DIR / 'dir3',
            )
        def test_ode(datafiles):
            assert len(list(datafiles.iterdir())) == 6
    """)
    result = testdir.runpytest("-s")
    result.stdout.fnmatch_lines(["E*ValueError:*file1'*already exists*"])


def test_on_duplicate_exception2(testdir):
    """
    Verify that a ValueError is raised when duplicate files appear
    """
    testdir.makepyfile(f"""
        import pytest
        from pathlib import Path

        FIXTURE_DIR = Path('{FIXTURE_DIR}')

        @pytest.mark.datafiles(
            FIXTURE_DIR / 'dir1' / 'file1',
            FIXTURE_DIR / 'dir3' / 'file1',
            )
        def test_ode(datafiles):
            assert len(list(datafiles.iterdir())) == 2
    """)
    result = testdir.runpytest("-s")
    result.stdout.fnmatch_lines(["E*ValueError:*file1'*already exists*"])


def test_on_duplicate_exception_dir(testdir):
    """
    Verify that a ValueError is raised when duplicate directories appear

    This is the default behaviour.

    If duplicate files appear (to be copied) then a ValueError is raised. In
    this example the directory 'subdir1' appears twice.
    """
    testdir.makepyfile(f"""
        import pytest
        from pathlib import Path

        FIXTURE_DIR = Path('{FIXTURE_DIR}')

        @pytest.mark.datafiles(
            FIXTURE_DIR / 'dir4' / 'subdir1',
            FIXTURE_DIR / 'dir5' / 'subdir1',
            keep_top_dir=True,
            )
        def test_duplicate_dir(datafiles):
            assert True
    """)
    result = testdir.runpytest("-s")
    result.stdout.fnmatch_lines(["E*ValueError:*subdir1'*already exists*"])


@pytest.mark.datafiles(
    FIXTURE_DIR / "dir4" / "subdir1",
    FIXTURE_DIR / "dir5" / "subdir1",
    keep_top_dir=True,
    on_duplicate="ignore",
)
def test_on_duplicate_ignore_dir(datafiles):
    """
    Verify that the second (duplicate) directory is ignored.
    """
    assert (datafiles / "subdir1" / "file1").is_file()


@pytest.mark.datafiles(
    FIXTURE_DIR / "dir1" / "file1",
    FIXTURE_DIR / "dir3" / "file1",
    on_duplicate="ignore",
)
def test_on_duplicate_ignore_file(datafiles):
    """
    Verify on_duplicate=ignore causes the first file to be used
    """
    assert (datafiles / "file1").is_file()
    assert (datafiles / "file1").read_text() == "dir1\n123\n"


def test_non_existing_file(testdir):
    """
    Verify exception is raised if file doesn't exist.
    """
    testdir.makepyfile(f"""
        import pytest
        from pathlib import Path

        FIXTURE_DIR = Path('{FIXTURE_DIR}')

        @pytest.mark.datafiles(
            FIXTURE_DIR / 'fileZZ',
            )
        def test_ode(datafiles):
            assert len(list(datafiles.iterdir())) == 1
    """)
    result = testdir.runpytest("-s")
    result.stdout.fnmatch_lines(
        [
            "E*FileNotFoundError:*fileZZ'",
        ]
    )


def test_invalid_keep_top_dir(testdir):
    """
    Verify ValueError is raised if parameter isn't boolean
    """
    testdir.makepyfile(f"""
        import pytest
        from pathlib import Path

        FIXTURE_DIR = Path('{FIXTURE_DIR}')

        @pytest.mark.datafiles(
            FIXTURE_DIR / 'fileZZ',
            keep_top_dir='invalid-value',
            )
        def test_invalid_param(datafiles):
            assert True
    """)
    result = testdir.runpytest("-s")
    result.stdout.fnmatch_lines(
        [
            "E*ValueError: 'keep_top_dir' must be True or False*",
        ]
    )


def test_invalid_on_duplicate(testdir):
    """
    Verify ValueError is raised if parameter isn't boolean
    """
    testdir.makepyfile(f"""
        import pytest
        from pathlib import Path

        FIXTURE_DIR = Path('{FIXTURE_DIR}')

        @pytest.mark.datafiles(
            FIXTURE_DIR / 'fileZZ',
            on_duplicate='invalid-value',
            )
        def test_invalid_param(datafiles):
            assert True
    """)
    result = testdir.runpytest("-s")
    result.stdout.fnmatch_lines(
        [
            "E*ValueError: 'on_duplicate' must be 'exception', 'ignore' or *",
        ]
    )


@pytest.mark.datafiles(FIXTURE_DIR / "sparrow_link.jpg")
def test_copy_symlink(datafiles):
    """
    Verify that symlinks are copied and not their targets.
    """
    assert len(list(datafiles.iterdir())) == 1
    assert (datafiles / "sparrow_link.jpg").is_symlink()


@pytest.mark.datafiles(FIXTURE_DIR / "dir6")
def test_copy_symlink_in_dir(datafiles):
    """
    Verify that symlinks are copied and not their targets.
    """
    assert len(list(datafiles.iterdir())) == 1
    assert (datafiles / "sparrow_link.jpg").is_symlink()


@pytest.mark.datafiles(
    FIXTURE_DIR / "dir6",
    keep_top_dir=True,
)
def test_copy_symlink_in_dir2(datafiles):
    """
    Verify that symlinks are copied and not their targets.
    """
    assert len(list(datafiles.iterdir())) == 1
    assert len(list((datafiles / "dir6").iterdir())) == 1
    assert (datafiles / "dir6" / "sparrow_link.jpg").is_symlink()


@pytest.mark.datafiles(FIXTURE_DIR / "executable.sh")
def test_file_mode_bits_preserved(datafiles):
    """
    Verify that file permission bits are preserved when copying files.

    Regression test for issue #11.
    """
    original_file = FIXTURE_DIR / "executable.sh"
    copied_file = datafiles / "executable.sh"

    # Get the mode of both files
    original_mode = original_file.stat().st_mode
    copied_mode = copied_file.stat().st_mode

    # The mode bits should match
    assert original_mode == copied_mode, (
        f"File permissions not preserved: "
        f"original={oct(original_mode)}, copied={oct(copied_mode)}"
    )
