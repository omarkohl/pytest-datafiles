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
    for entry in content:
        if _is_str(entry):
            entry = path.local(entry)
        entry.copy(tmpdir)
    return tmpdir
