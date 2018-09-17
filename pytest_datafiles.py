"""
Module containing a 'datafiles' fixture for pytest Tests.
"""

from py import path  # pylint: disable=E0611
import pytest


def _copy(src, target):
    if not src.exists():
        raise ValueError("'%s' does not exist!" % src)
    if src.isdir():
        src.copy(target / src.basename)
    else:  # file
        src.copy(target)


def _copy_all(entry_list, target_dir, on_duplicate):
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


def _is_str(obj):
    """
    Check if 'obj' is a string (both Python 2 and 3)
    """
    try:
        return isinstance(obj, basestring)  # pylint: disable=E0602
    except NameError:
        return isinstance(obj, str)


def _to_py_path(entry_list):
    converted = []
    for entry in entry_list:
        if _is_str(entry):
            converted.append(path.local(entry))
        else:
            converted.append(entry)
    return converted


def _get_all_entries(entry_list, keep_top_dir):
    all_files = []

    entry_list = _to_py_path(entry_list)

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
