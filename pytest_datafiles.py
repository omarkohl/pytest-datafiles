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
        'on_duplicate': 'exception', # ignore, overwrite
        }
    options.update(request.keywords.get('datafiles').kwargs)
    on_duplicate = options['on_duplicate']
    keep_top_dir = options['keep_top_dir']
    assert keep_top_dir in (True, False), "'keep_top_dir' must be True or False"
    assert on_duplicate in ('exception', 'ignore', 'overwrite'), \
        "'on_duplicate' must be 'exception', 'ignore' or 'overwrite'"
    for entry in content:
        if _is_str(entry):
            entry = path.local(entry)
        basename = entry.basename
        if entry.isfile() or (entry.isdir() and keep_top_dir):
            if on_duplicate == 'overwrite' or not (tmpdir / basename).exists():
                if entry.isdir():
                    entry.copy(tmpdir / basename)
                else:
                    entry.copy(tmpdir)
            elif on_duplicate == 'exception':
                raise ValueError(
                    "'%s' already exists (entry %s)" % (basename, entry)
                    )
            # on_duplicate == 'ignore': do nothing with entry
        elif entry.isdir():
            # Regular directory (no keep_top_dir). Need to check every file for duplicates
            if on_duplicate == 'overwrite':
                entry.copy(tmpdir)
                continue
            for e2 in entry.listdir():
                if not (tmpdir / e2.basename).exists():
                    e2.copy(tmpdir / e2.basename)
                    continue
                if on_duplicate == 'exception':
                    raise ValueError(
                        "'%s' already exists (entry %s)" % ((tmpdir / e2.basename), e2)
                        )
                # on_duplicate == 'ignore': do nothing with e2
        else:
            raise ValueError(
                "entry '%s' is neither file nor dir. Possibly it doesn't " \
                "exist." % entry
                )
    return tmpdir
