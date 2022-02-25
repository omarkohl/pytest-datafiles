"""
Module containing a 'datafiles' fixture for pytest Tests.
"""
import os
import shutil
from functools import partial

from pathlib import Path
import pytest


def _copy(src, target):
    """
    Copies a single entry (file, dir) named 'src' to 'target'. Softlinks are
    processed properly as well.
    """
    if not src.exists():
        raise ValueError("'%s' does not exist!" % src)

    if src.is_dir():
        shutil.copytree(src, target / src.name)
    elif src.is_simlink():
        os.symlink(os.readlink(src), target / src.name)
    else:  # file
        shutil.copy(src, target)


def _copy_all(entry_list, target_dir, on_duplicate):
    """
    Copies all entries (files, dirs) from 'entry_list' to 'target_dir' taking
    into account the 'on_duplicate' option (which defines what should happen if
    an entry already exists: raise an exception, overwrite it or ignore it).
    """
    for entry in entry_list:
        target_entry = target_dir / entry.name
        if not target_entry.exists() or on_duplicate == 'overwrite':
            _copy(entry, target_dir)
        elif on_duplicate == 'exception':
            raise ValueError(
                "'%s' already exists (src %s)" % (
                    target_entry,
                    entry,
                    )
                )
        else:  # ignore
            continue


def _get_all_entries(entry_list, keep_top_dir):
    """
    Returns a list of all entries (files, directories) that should be copied.
    The main purpose of this function is to evaluate 'keep_top_dir' and in case
    it should not be kept use all the entries below the top-level directories.
    """
    all_files = []

    entry_list = [Path(entry) for entry in entry_list]

    if keep_top_dir:
        all_files = entry_list
    else:
        for entry in entry_list:
            if entry.is_dir():
                all_files.extend(list(entry.glob('*')))
            else:
                all_files.append(entry)
    return all_files


class DataFilesPlugin:
    def __init__(self, root=""):
        self.root = Path(root)

    @pytest.fixture
    def datafiles(self, request, tmpdir):
        """
        pytest fixture to define a 'tmpdir' containing files or directories
        specified with a 'datafiles' mark.
        """
        entry_list = []
        options = {
            "keep_top_dir": False,
            "on_duplicate": "exception",  # ignore, overwrite
        }
        for mark in request.node.iter_markers("datafiles"):
            entries = [self.root / entry for entry in mark.args]
            entry_list.extend(entries)
            options.update(mark.kwargs)

        on_duplicate = options["on_duplicate"]
        keep_top_dir = options["keep_top_dir"]

        if keep_top_dir not in (True, False):
            raise ValueError("'keep_top_dir' must be True or False")
        if on_duplicate not in ("exception", "ignore", "overwrite"):
            raise ValueError(
                "'on_duplicate' must be 'exception', 'ignore' or " "'overwrite'"
            )

        all_entries = _get_all_entries(entry_list, keep_top_dir)
        _copy_all(all_entries, Path(tmpdir), on_duplicate)
        return tmpdir


def pytest_addoption(parser):
    parser.addini("datafiles_root", "Root folder for datafiles fixure")


def pytest_configure(config):
    root = config.getini("datafiles_root")
    config.pluginmanager.register(DataFilesPlugin(root))
    config.addinivalue_line(
        "markers",
        "datafiles(*args): Set list of files to use " "with the datafile fixure.",
    )
