"""
Module containing a 'datafiles' fixture for pytest Tests.
"""

from py import path  # pylint: disable=E0611
import pytest


def _copy(src, target):
    """
    Copies a single entry (file, dir) named 'src' to 'target'. Softlinks are
    processed properly as well.
    """
    if not src.exists():
        raise ValueError("'%s' does not exist!" % src)

    if src.isdir():
        src.copy(target / src.basename)
    elif src.islink():
        (target / src.basename).mksymlinkto(src.realpath())
    else:  # file
        src.copy(target)


def _copy_all(entry_list, target_dir, on_duplicate):
    """
    Copies all entries (files, dirs) from 'entry_list' to 'target_dir' taking
    into account the 'on_duplicate' option (which defines what should happen if
    an entry already exists: raise an exception, overwrite it or ignore it).
    """
    for entry in entry_list:
        target_entry = target_dir / entry.basename
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

    entry_list = [path.local(entry) for entry in entry_list]

    if keep_top_dir:
        all_files = entry_list
    else:
        for entry in entry_list:
            if entry.isdir():
                all_files.extend(entry.listdir())
            else:
                all_files.append(entry)
    return all_files


@pytest.fixture
def datafiles(request, tmpdir):
    """
    pytest fixture to define a 'tmpdir' containing files or directories
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
        raise ValueError("'on_duplicate' must be 'exception', 'ignore' or "
                         "'overwrite'")

    all_entries = _get_all_entries(entry_list, keep_top_dir)
    _copy_all(all_entries, tmpdir, on_duplicate)
    return tmpdir
