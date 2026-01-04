"""Example: files with same names.

Imagine you have 3 directories (*dir1*, *dir2*, *dir3*) each containing
the files (*fileA* and *fileB*).

This example clarifies the options **on_duplicate** and **keep_top_dir**.
"""

from pathlib import Path

import pytest

FIXTURE_DIR = Path(__file__).parent.resolve() / "_fixture_files"


@pytest.mark.datafiles(
    FIXTURE_DIR / "dir1",
    FIXTURE_DIR / "dir2",
    FIXTURE_DIR / "dir3",
    on_duplicate="ignore",
)
def test_dir_ignore(datafiles):
    """Use files from dir1 (first dir added)."""
    assert len(list(datafiles.iterdir())) == 2
    assert (datafiles / "fileA").exists()
    assert (datafiles / "fileA").read_text() == "1a\n"


@pytest.mark.datafiles(
    FIXTURE_DIR / "dir2",
    FIXTURE_DIR / "dir1",
    FIXTURE_DIR / "dir3",
    on_duplicate="ignore",
)
def test_dir_ignore2(datafiles):
    """Use files from dir2 (first dir added)."""
    assert len(list(datafiles.iterdir())) == 2
    assert (datafiles / "fileA").exists()
    assert (datafiles / "fileA").read_text() == "2a\n"


@pytest.mark.datafiles(
    FIXTURE_DIR / "dir1",
    FIXTURE_DIR / "dir2",
    FIXTURE_DIR / "dir3",
    on_duplicate="overwrite",
)
def test_dir_overwrite(datafiles):
    """Use files from dir3 (last dir added)."""
    assert len(list(datafiles.iterdir())) == 2
    assert (datafiles / "fileA").exists()
    assert (datafiles / "fileA").read_text() == "3a\n"


@pytest.mark.datafiles(
    FIXTURE_DIR / "dir1",
    FIXTURE_DIR / "dir2",
    FIXTURE_DIR / "dir3",
    # on_duplicate='exception' is the default
)
def test_dir_exception(datafiles):  # pylint: disable=W0613
    """Raise exception because of duplicate filename fileA."""
    pytest.fail("Expected to fail due to duplicate files")


@pytest.mark.datafiles(
    FIXTURE_DIR / "dir1",
    FIXTURE_DIR / "dir2",
    FIXTURE_DIR / "dir3",
    keep_top_dir=True,
)
def test_dir_keep_top_dir(datafiles):
    """Use all files."""
    # 3 subdirs
    assert len(list(datafiles.iterdir())) == 3
    # 3 subdirs with each 2 files: 3 + 3*2
    assert len(list(datafiles.glob("**/*"))) == 9
    assert (datafiles / "dir3" / "fileA").exists()
    assert (datafiles / "dir3" / "fileA").read_text() == "3a\n"
