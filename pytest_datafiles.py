"""
Module containing a 'datafiles' fixture for pytest Tests.
"""

from py import path  # pylint: disable=E0611
import pytest


def _is_str(obj):
    """
    Check if 'obj' is a string (both Python 2 and 3)
    """
    try:
        return isinstance(obj, basestring)  # pylint: disable=E0602
    except NameError:
        return isinstance(obj, str)


def _copy_file(target_dir, entry, on_duplicate):
    basename = entry.basename
    if on_duplicate == 'overwrite' or not (target_dir / basename).exists():
        entry.copy(target_dir)
    elif on_duplicate == 'exception':
        raise ValueError(
            "'%s' already exists (entry %s)" % (basename, entry)
            )
    else:
        # on_duplicate == 'ignore': do nothing with entry
        pass


def _copy_dir(target_dir, entry, on_duplicate, keep_top_dir):
    basename = entry.basename
    if keep_top_dir:
        if on_duplicate == 'overwrite' or not (target_dir / basename).exists():
            entry.copy(target_dir / basename)
        elif on_duplicate == 'exception':
            raise ValueError(
                "'%s' already exists (entry %s)" % (basename, entry)
                )
        # else: on_duplicate == 'ignore': do nothing with entry
    else:
        # Regular directory (no keep_top_dir). Need to check every file
        # for duplicates
        if on_duplicate == 'overwrite':
            entry.copy(target_dir)
            return
        for sub_entry in entry.listdir():
            if not (target_dir / sub_entry.basename).exists():
                sub_entry.copy(target_dir / sub_entry.basename)
                continue
            if on_duplicate == 'exception':
                # target exists
                raise ValueError(
                    "'%s' already exists (entry %s)" % (
                        (target_dir / sub_entry.basename),
                        sub_entry,
                        )
                    )
            # on_duplicate == 'ignore': do nothing with e2


@pytest.fixture
def datafiles(request, tmpdir):
    """
    pytest fixture to define a 'tmpdir' containing files or directories
    specified with a 'datafiles' mark.
    """
    if 'datafiles' not in request.keywords:
        return tmpdir
    content = request.keywords.get('datafiles').args
    options = {
        'keep_top_dir': False,
        'on_duplicate': 'exception',  # ignore, overwrite
        }
    options.update(request.keywords.get('datafiles').kwargs)
    on_duplicate = options['on_duplicate']
    keep_top_dir = options['keep_top_dir']
    if keep_top_dir not in (True, False):
        raise ValueError("'keep_top_dir' must be True or False")
    if on_duplicate not in ('exception', 'ignore', 'overwrite'):
        raise ValueError("'on_duplicate' must be 'exception', 'ignore' or "
                         "'overwrite'")
    for entry in content:
        if _is_str(entry):
            entry = path.local(entry)
        if entry.isfile():
            _copy_file(tmpdir, entry, on_duplicate)
        elif entry.isdir():
            _copy_dir(tmpdir, entry, on_duplicate, keep_top_dir)
        else:
            raise ValueError(
                "entry '%s' is neither file nor dir. Possibly it doesn't "
                "exist." % entry
                )
    return tmpdir
