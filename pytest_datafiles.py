import py
import pytest

def _is_str(s):
    """
    Check if 's' is a string (both Python 2 and 3)
    """
    try:
        return isinstance(s, basestring)
    except NameError:
        return isinstance(s, str)

@pytest.fixture
def datafiles(request, tmpdir):
    if 'datafiles' not in request.keywords:
        return tmpdir
    content = request.keywords.get('datafiles').args
    for entry in content:
        if _is_str(entry):
            entry = py.path.local(entry)
        entry.copy(tmpdir)
    return tmpdir
