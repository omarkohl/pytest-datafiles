
pytest-datafiles
****************

https://travis-ci.org/omarkohl/pytest-datafileshttps://coveralls.io/github/omarkohl/pytest-datafiles?branch=masterhttps://pypi.python.org/pypi/pytest-datafileshttps://codeclimate.com/github/omarkohl/pytest-datafiles

`pytest <https://docs.pytest.org/en/latest/contents.html>`_ plugin to
create a `tmp_path <https://docs.pytest.org/en/latest/tmp_path.html>`_
containing a preconfigured set of files and/or directories.

**Note about maintenance:** This project is maintained and bug reports
or pull requests will be addressed. There is little activity because
it simply works and no changes are required.


Features
========

This plugin allows you to specify one or several files/directories
that are copied to a temporary directory (`tmp_path
<https://docs.pytest.org/en/latest/tmp_path.html>`_) before the
execution of the test. This means the original files are not modified
and every test runs on its own version of the same files.

Files/directories can be specified either as *strings* or as
*pathlib.Path* objects.

To take advantage of the *datafiles* fixture in a test function, add
*datafiles* as one of the test function parameters (per usual with
`pytest <https://docs.pytest.org/en/latest/contents.html>`_ fixtures)
and decorate the test function with *@pytest.mark.datafiles(file1,
file2, dir1, dir2, …)*. See the examples below.

The *datafiles* variable in your test function is a pathlib.Path
object (`tmp_path <https://docs.pytest.org/en/latest/tmp_path.html>`_)
where the copied files are located. Under Linux systems this will most
likely be some subdirectory of */tmp/*.


Options
=======

The following options can be specified as keyword arguments (kwargs)
to the *@pytest.mark.datafiles* decorator function:

*  **keep_top_dir:** For all parameters that represent directories,
   keep that directory instead of only (recursively) copying its
   content. Possible values are *True* or *False*. *False* is the
   default value.

*  **on_duplicate:** Specify the action to take when duplicate
   files/directories are found. Possible values are: *exception*,
   *ignore* and *replace*. The default value is *exception*.

   *  *exception:* An exception is raised instead of copying the
      duplicate file/directory.

   *  *ignore:* The second (or subsequent) files/directories with the
      same name as the first one are simply ignored (i.e., the first
      file/directory with the duplicate name is kept).

   *  *replace:* The second (or subsequent) files/directories with the
      same name replace the previous ones (i.e., the last
      file/directory with the duplicate name is kept).

See below for some *examples*.


Installation
============

.. code:: bash

   pip install pytest-datafiles


Upgrade to 3.0
==============

Version 3 now uses `tmp_path
<https://docs.pytest.org/en/latest/tmp_path.html>`_, resulting in
*pathlib.Path* objects instead of *py.path*.

Your tests may need to be adjusted.

.. code:: python

   """Upgrade to v3."""
   import os

   import pytest
   import py


   @pytest.mark.datafiles('/tmp/big_files/film1.mp4')
   def test_convert_to_pypath(datafiles):
       """Convert `datafiles` to `py.path` in place.

       Changing the type back to py.path - should be avoided!

       Better to update the tests to make use of `pathlib`.
       """

       # changing the type back to py.path - should be avoided
       datafiles = py.path.local(str(datafiles))

       # code remains as before
       assert len(datafiles.listdir()) == 1
       assert (datafiles / 'film1.mp4').check(file=1)


   @pytest.mark.datafiles('/tmp/big_files/film1.mp4')
   def test_update_to_pathlib(datafiles):
       """Upgrade code to use `pathlib`.

       Some examples showing `pathlib` style.
       """

       # For demo purpose: this is the old-style
       pypath_datafiles = py.path.local(str(datafiles))

       # old style
       assert len(pypath_datafiles.listdir()) == 1
       assert (pypath_datafiles / 'film1.mp4').check(file=1)

       # new style  # pylint: disable=R0801
       assert len(list(datafiles.iterdir())) == 1
       assert (datafiles / 'film1.mp4').is_file()


   @pytest.mark.datafiles('/tmp/big_files/film1.mp4')
   def test_keep_using_str(datafiles):
       """Keep using plain `os`.

       Nothing changes.
       """

       path = str(datafiles)
       assert len(os.listdir(path)) == 1
       assert os.path.isfile(os.path.join(path, 'film1.mp4'))


Usage
=====

These examples can also be found in *tests/examples*.


Example 1
---------

One possible use case is when you are running tests on very big files
that are not included or packaged with your tests. For example, your
test files are large video files stored under */opt/big_files/* . You
don’t want your tests modifying the original files, but the files are
required by the tests. You can reference these data files in your test
method as follows:

.. code:: python

   """Example: Reference files anywhere """
   import os
   import pytest


   @pytest.mark.datafiles('/tmp/big_files/film1.mp4')
   def test_fast_forward(datafiles):
       """Work with a copy of the big file."""
       assert len(list(datafiles.iterdir())) == 1
       assert (datafiles / 'film1.mp4').is_file()
       # assert some_operation(datafiles / 'film1.mp4') == expected_result


   @pytest.mark.datafiles('/tmp/big_files/film1.mp4')
   def test_fast_forward_alternative(datafiles):
       """Work with a copy of the bigfile, using `str`."""
       path = str(datafiles)  # Convert from py.path object to path (str)
       assert len(os.listdir(path)) == 1
       assert os.path.isfile(os.path.join(path, 'film1.mp4'))
       # assert some_operation(os.path.join(path, 'film1.mp4')) == expected_result


Example 2
---------

Now for another use case: let’s say in the directory where your tests
are located, you place a directory named *test_files*. Here you have a
lot of images you want to run tests on. By using this plugin, you make
sure the original files under *test_files* are not modified by every
test.

.. code:: python

   """Example: make a subset of the files in a dir available."""
   from pathlib import Path

   import pytest

   # Dir containing 8 files
   FIXTURE_DIR = Path(__file__).parent.resolve() / 'test_files'


   @pytest.mark.datafiles(
       FIXTURE_DIR / 'img1.jpg',
       FIXTURE_DIR / 'img2.jpg',
       FIXTURE_DIR / 'img3.jpg',
   )
   def test_find_borders(datafiles):
       """Work with a copy of only 3 files."""
       for img in datafiles.iterdir():
           print(img)
           # assert process(img) == some_expected_value

           # and only the referenced files are available
           assert img.name != 'img4.jpg'

       assert len(list(datafiles.iterdir())) == 3


   @pytest.mark.datafiles(
       FIXTURE_DIR / 'img4.jpg',
       FIXTURE_DIR / 'img5.jpg',
   )
   def test_brightness(datafiles):
       """Work with a copy of only 2 files."""
       for img in datafiles.iterdir():
           print(img)
           # assert process(img) == some_expected_value

           # and only the referenced files are available
           assert img.name != 'img3.jpg'

       assert len(list(datafiles.iterdir())) == 2


   @pytest.mark.datafiles(FIXTURE_DIR)
   def test_resize(datafiles):
       """Work with a copy of all files."""
       for img in datafiles.iterdir():
           print(img)
           # assert process(img) == some_expected_value

       assert len(list(datafiles.iterdir())) == 8


Example 3
---------

If all (or many) of your tests rely on the same files it can be easier
to define one decorator beforehand and apply it to every test like
this example:

.. code:: python

   """Example: re-use file selection."""
   from pathlib import Path

   import pytest

   FIXTURE_DIR = Path(__file__).parent.resolve() / 'test_files'

   ALL_IMGS = pytest.mark.datafiles(
       FIXTURE_DIR / 'img1.jpg',
       FIXTURE_DIR / 'img2.jpg',
       FIXTURE_DIR / 'img3.jpg',
       FIXTURE_DIR / 'img4.jpg',
       FIXTURE_DIR / 'img5.jpg',
       FIXTURE_DIR / 'img6.jpg',
       FIXTURE_DIR / 'img7.jpg',
       FIXTURE_DIR / 'img8.jpg',
   )


   @ALL_IMGS
   def test_something1(datafiles):
       """Work with copy of all files."""
       for img in datafiles.iterdir():
           print(img)
           # assert process(img) == some_expected_value

       assert len(list(datafiles.iterdir())) == 8

       # we can do something destructive
       (datafiles / 'img3.jpg').unlink()
       assert len(list(datafiles.iterdir())) == 7


   @ALL_IMGS
   def test_something2(datafiles):
       """Work with copy of all files."""
       for img in datafiles.iterdir():
           print(img)
           # assert process(img) == some_expected_value

       assert len(list(datafiles.iterdir())) == 8

       # we can do something destructive
       (datafiles / 'img1.jpg').unlink()
       assert len(list(datafiles.iterdir())) == 7


Example 4
---------

Imagine you have 3 directories (*dir1*, *dir2*, *dir3*) each
containing the files (*fileA* and *fileB*).

This example clarifies the options **on_duplicate** and
**keep_top_dir**.

.. code:: python

   """Example: files with same names."""
   from pathlib import Path

   import pytest

   FIXTURE_DIR = Path(__file__).parent.resolve() / '_fixture_files'


   @pytest.mark.datafiles(
       FIXTURE_DIR / 'dir1',
       FIXTURE_DIR / 'dir2',
       FIXTURE_DIR / 'dir3',
       on_duplicate='ignore',
   )
   def test_dir_ignore(datafiles):
       """Use files from dir1 (first dir added)."""
       assert len(list(datafiles.iterdir())) == 2
       assert (datafiles / 'fileA').exists()
       assert (datafiles / 'fileA').read_text() == '1a\n'


   @pytest.mark.datafiles(
       FIXTURE_DIR / 'dir2',
       FIXTURE_DIR / 'dir1',
       FIXTURE_DIR / 'dir3',
       on_duplicate='ignore',
   )
   def test_dir_ignore2(datafiles):
       """Use files from dir2 (first dir added)."""
       assert len(list(datafiles.iterdir())) == 2
       assert (datafiles / 'fileA').exists()
       assert (datafiles / 'fileA').read_text() == '2a\n'


   @pytest.mark.datafiles(
       FIXTURE_DIR / 'dir1',
       FIXTURE_DIR / 'dir2',
       FIXTURE_DIR / 'dir3',
       on_duplicate='overwrite',
   )
   def test_dir_overwrite(datafiles):
       """Use files from dir3 (last dir added)."""
       assert len(list(datafiles.iterdir())) == 2
       assert (datafiles / 'fileA').exists()
       assert (datafiles / 'fileA').read_text() == '3a\n'


   @pytest.mark.datafiles(
       FIXTURE_DIR / 'dir1',
       FIXTURE_DIR / 'dir2',
       FIXTURE_DIR / 'dir3',
       # on_duplicate='exception' is the default
   )
   @pytest.mark.skip(
       reason='will raise an exception that cannot be caught in the test itself'
   )
   def test_dir_exception(datafiles):  # pylint: disable=W0613
       """Raise exception because of duplicate filename fileA."""
       assert False


   def test_dir_exception_generated(testdir):
       """Raise exception because of duplicate filename fileA."""
       testdir.makepyfile(f'''
           import pytest
           from pathlib import Path

           FIXTURE_DIR = Path('{FIXTURE_DIR}')

           @pytest.mark.datafiles(
               FIXTURE_DIR / 'dir1',
               FIXTURE_DIR / 'dir2',
               FIXTURE_DIR / 'dir3',
               # on_duplicate='exception' is the default
           )
           def test_exception(datafiles):
               assert True
       ''')
       result = testdir.runpytest('-s')
       result.stdout.fnmatch_lines([
           'E*ValueError: *already exists*',
       ])


   @pytest.mark.datafiles(
       FIXTURE_DIR / 'dir1',
       FIXTURE_DIR / 'dir2',
       FIXTURE_DIR / 'dir3',
       keep_top_dir=True,
   )
   def test_dir_keep_top_dir(datafiles):
       """Use all files."""
       # 3 subdirs
       assert len(list(datafiles.iterdir())) == 3
       # 3 subdirs with each 2 files: 3 + 3*2
       assert len(list(datafiles.glob('**/*'))) == 9
       assert (datafiles / 'dir3' / 'fileA').exists()
       assert (datafiles / 'dir3' / 'fileA').read_text() == '3a\n'


Example 5
---------

You can also use a str paths.

.. code:: python

   """Example: use `str` paths."""
   import os
   import pytest

   FIXTURE_DIR = os.path.join(
       os.path.dirname(os.path.realpath(__file__)),
       'test_files'
   )


   @pytest.mark.datafiles(
       os.path.join(FIXTURE_DIR, 'img1.jpg'),
       os.path.join(FIXTURE_DIR, 'img2.jpg'),
       os.path.join(FIXTURE_DIR, 'img3.jpg'),
   )
   def test_str(datafiles):
       """Work with `str`."""
       assert len(list(datafiles.iterdir())) == 3


Contributing
============

Contributions are very welcome. Tests can be run with `tox
<https://tox.readthedocs.org/en/latest/>`_. Please ensure the coverage
stays at least the same before you submit a pull request.

To create and upload a new package first update the version number and
then:

.. code:: bash

   pip3 install --user -U twine
   make clean
   make dist
   twine upload --repository-url https://test.pypi.org/legacy/ dist/*
   # Verify the package is usable
   virtualenv -p python3 test-venv
   test-venv/bin/pip install pytest
   test-venv/bin/pip install --index-url https://test.pypi.org/simple/ pytest-datafiles
   # Create some test_example.py (e.g. with one of the examples above)
   test-venv/bin/pytest test_example.py
   # Set the git tag for final release
   git tag -a 3.0
   git push --tags
   # Upload the package for final release
   twine upload dist/*

Finally create a release on GitHub and add the packages from dist/* to
it.

Of course this will only work if you have the necessary PyPI
credentials for this package.


License
=======

Distributed under the terms of the `MIT license
<http://opensource.org/licenses/MIT>`_, “pytest-datafiles” is free and
open source software.


Issues
======

If you encounter any problems, please `file an issue
<https://github.com/omarkohl/pytest-datafiles/issues>`_ along with a
detailed description.


Acknowledgements
================

Thanks to `@flub <https://github.com/flub>`_ for the idea to use
`pytest <https://docs.pytest.org/en/latest/contents.html>`_ marks to
solve the problem this plugin is trying to solve.

Some ideas to improve this project were taken from the `Cookiecutter
<https://github.com/audreyr/cookiecutter>`_ templates
`cookiecutter-pypackage
<https://github.com/audreyr/cookiecutter-pypackage>`_ and
`cookiecutter-pytest-plugin
<https://github.com/pytest-dev/cookiecutter-pytest-plugin>`_.
