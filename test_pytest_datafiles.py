pytest_plugins = ['pytester']


def test_copy_hosts(testdir):
    """
    Create a test that relies on a 'hosts' file being present and that checks
    if this file contains an entry 'localhost'.

    Verify that that test runs sucessfully.
    """
    testdir.makepyfile("""
    import pytest

    @pytest.mark.datafiles("/etc/hosts")
    def test_file_copied(datafiles):
        assert (datafiles / 'hosts').check(file=1)
        assert 'localhost' in (datafiles / 'hosts').read_text('utf-8')
    """)
    result = testdir.runpytest()
    assert result.ret == 0
    assert result.errlines == []
    result.stdout.fnmatch_lines([
        "*1 passed*"
        ])


def test_multiple_files(testdir):
    """
    Create a test that relies on several files being present.

    Verify that that test runs sucessfully.
    """
    testdir.makepyfile("""
    import pytest

    @pytest.mark.datafiles("/etc/hosts", "/etc/hostname")
    def test_two_files_copied(datafiles):
        assert (datafiles / 'hosts').check(file=1)
        assert (datafiles / 'hostname').check(file=1)
        assert len((datafiles).listdir()) == 2
    """)
    result = testdir.runpytest()
    assert result.ret == 0
    assert result.errlines == []
    result.stdout.fnmatch_lines([
        "*1 passed*"
        ])


def test_no_files(testdir):
    """
    Create a test that requires no files being copied before the test. Test
    two cases:
        1. datafiles marker is set but empty
        2. datafiles marker is not set

    Verify that those tests run sucessfully.
    """
    testdir.makepyfile("""
    import pytest

    @pytest.mark.datafiles
    def test_no_file1(datafiles):
        assert len((datafiles).listdir()) == 0

    def test_no_file2(datafiles):
        assert len((datafiles).listdir()) == 0
    """)
    result = testdir.runpytest()
    assert result.ret == 0
    assert result.errlines == []
    result.stdout.fnmatch_lines([
        "*2 passed*"
        ])
