import pytest


@pytest.mark.datafiles("/etc/hosts")
def test_copy_hosts(datafiles):
    """
    Verify that a 'hosts' file containing an entry 'localhost' has been copied
    """
    assert (datafiles / 'hosts').check(file=1)
    assert 'localhost' in (datafiles / 'hosts').read_text('utf-8')


@pytest.mark.datafiles("/etc/hosts", "/etc/hostname")
def test_multiple_files(datafiles):
    """
    Verify multiple files are found
    """
    assert (datafiles / 'hosts').check(file=1)
    assert (datafiles / 'hostname').check(file=1)
    assert len((datafiles).listdir()) == 2


@pytest.mark.datafiles
def test_no_files1(datafiles):
    """
    Verify if datafiles marker is set but empty the directory is empty
    """
    assert len((datafiles).listdir()) == 0


def test_no_files2(datafiles):
    """
    Verify if datafiles marker is not set the directory is empty
    """
    assert len((datafiles).listdir()) == 0
