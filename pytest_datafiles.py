"""
Module containing a 'datafiles' fixture for pytest Tests.
"""
import shutil
from pathlib import Path
from typing import List

import pytest

from _pytest.config import Config


def pytest_configure(config: Config) -> None:
    """Perform initial configuration."""
    config.addinivalue_line(
        "markers",
        "datafiles(path, ..., *, keep_top_dir=False, "
        "on_duplicate='exception'): Paths to copy to tmpdir before the test. "
        "'keep_top_dir': For all parameters that represent directories, keep "
        "that directory instead of only (recursively) copying its content "
        "(default is False). Use the option 'on_duplicate' to specify the "
        "action to take when duplicate files/directories are found. Possible "
        "values are: exception, ignore and replace. The default value is "
        "exception.",
    )


def _copy_all(entry_list: List[Path], target_dir: Path, on_duplicate: str):
    """
    Copies all entries (files, dirs) from 'entry_list' to 'target_dir' taking
    into account the 'on_duplicate' option (which defines what should happen if
    an entry already exists: raise an exception, overwrite it or ignore it).
    """
    for entry in entry_list:
        target_entry = target_dir / entry.name
        if not target_entry.exists() or on_duplicate == 'overwrite':
            if entry.is_file():
                shutil.copy(entry, target_entry, follow_symlinks=False)
            else:
                shutil.copytree(entry, target_entry, symlinks=True)
        elif on_duplicate == 'exception':
            raise ValueError(f"'{target_entry}' already exists (src {entry})")
        else:  # ignore
            continue


def _get_all_entries(entry_list: List[str], keep_top_dir: bool) -> List[Path]:
    """
    Returns a list of all entries (files, directories) that should be copied.
    The main purpose of this function is to evaluate 'keep_top_dir' and in case
    it should not be kept use all the entries below the top-level directories.
    """
    all_files = []

    entry_list = [Path(entry) for entry in entry_list]

    if keep_top_dir:
        return entry_list

    for entry in entry_list:
        if entry.is_dir():
            all_files.extend(entry.iterdir())
        else:
            all_files.append(entry)
    return all_files


@pytest.fixture
def datafiles(request, tmp_path: Path) -> Path:
    """
    pytest fixture to define a 'tmp_path' containing files or directories
    specified with a 'datafiles' mark.
    """
    entry_list = []
    options = {
        'keep_top_dir': False,
        'on_duplicate': 'exception',  # ignore, overwrite
        }
    for mark in request.node.iter_markers('datafiles'):
        entry_list.extend(mark.args)
        options.update(mark.kwargs)

    on_duplicate = options['on_duplicate']
    keep_top_dir = options['keep_top_dir']

    if keep_top_dir not in (True, False):
        raise ValueError("'keep_top_dir' must be True or False")
    if on_duplicate not in ('exception', 'ignore', 'overwrite'):
        raise ValueError(f"'on_duplicate' must be 'exception', 'ignore' or "
                         f"'overwrite', got '{on_duplicate}'")

    all_entries = _get_all_entries(entry_list, keep_top_dir)
    _copy_all(all_entries, tmp_path, on_duplicate)
    return tmp_path
