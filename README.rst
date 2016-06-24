================
pytest-datafiles
================

.. image:: https://img.shields.io/travis/omarkohl/pytest-datafiles.svg
        :target: https://travis-ci.org/omarkohl/pytest-datafiles


.. image:: https://coveralls.io/repos/omarkohl/pytest-datafiles/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/omarkohl/pytest-datafiles?branch=master


.. image:: https://img.shields.io/pypi/v/pytest-datafiles.svg
	:target: https://pypi.python.org/pypi/pytest-datafiles


.. image:: https://codeclimate.com/github/omarkohl/pytest-datafiles/badges/gpa.svg
   :target: https://codeclimate.com/github/omarkohl/pytest-datafiles
   :alt: Code Climate


`pytest`_ plugin to create a `tmpdir`_ containing a preconfigured set of
files and/or directories.

**Note about maintenance:** This project is maintained and bug reports or pull
requests will be adressed. There is little activity because it simply works and
no changes are required.

Features
--------

This plugin allows you to specify one or several files/directories that will be
copied to a temporary directory (`tmpdir`_) before the execution of the test.
This means the original files are not modified and every test runs on its own
version of the same files.

Files/directories can be specified either as *strings* or as *py.path* objects.

The test function that wants to take advantage of this *datafiles* fixture
needs to use *datafiles* as one of its parameters (as usual with `pytest`_
fixtures) and needs to be decorated with *@pytest.mark.datafiles(file1,
file2, dir1, dir2, ...)*. See examples below.

The *datafiles* variable in your test function is a py.path object
(`tmpdir`_) where the copied files are located. Under Linux systems this
will most likely be some subdirectory of */tmp/*.


Options
-------

Following options can be specified as keyword arguments (kwargs) to the
*@pytest.mark.datafiles* decorator function:

- **keep_top_dir:** For all parameters that represent directories keep that
  directory instead of only (recursively) copying its content. Possible values
  are *True* and *False*. *False* is the default value.
- **on_duplicate:** Specify the action to take when duplicate files/directories
  are found. Possible values are: *exception*, *ignore* and *replace*. The
  default value is *exception*.

  - *exception:* An exception is raised instead of copying the duplicate
    file/directory.
  - *ignore:* The second (or subsequent) files/directories with the same name
    as the first one are simply ignored (i.e. the first file/directory with the
    duplicate name is kept).
  - *replace:* The second (or subsequent) files/directories with the same name
    replace the previous ones (i.e. the last file/directory with the duplicate
    name is kept).

See below for some *examples*.


Installation
------------

.. code-block:: bash

    pip install pytest-datafiles


Usage
-----

Example 1
~~~~~~~~~

One possible use case would be: You are running tests on very big files
that are not included/packaged with your tests. For instance big video
files stored under */opt/big_files/* . You don't want your tests modifying
the original files but the files are required by the tests.

.. code-block:: python

    import os
    import pytest

    @pytest.mark.datafiles('/opt/big_files/film1.mp4')
    def test_fast_forward(datafiles):
        path = str(datafiles)  # Convert from py.path object to path (str)
        assert len(os.listdir(path)) == 1
        assert os.path.isfile(os.path.join(path, 'film1.mp4'))
        #assert some_operation(os.path.join(path, 'film1.mp4')) == expected_result

        # Using py.path syntax
        assert len(datafiles.listdir()) == 1
        assert (datafiles / 'film1.mp4').check(file=1)

Example 2
~~~~~~~~~

Another use case is: In the directory where your tests are located you
placed a directory named *test_files*. Here you placed a lot of
images you want to run tests on. By using this plugin you make sure the
original files under *test_files* are not modified by every test.

.. code-block:: python

    import os
    import pytest

    FIXTURE_DIR = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'test_files',
        )

    @pytest.mark.datafiles(
        os.path.join(FIXTURE_DIR, 'img1.jpg'),
        os.path.join(FIXTURE_DIR, 'img2.jpg'),
        os.path.join(FIXTURE_DIR, 'img3.jpg'),
        )
    def test_find_borders(datafiles):
        for img in datafiles.listdir():
            print(img)
            #assert process(img) == some_expected_value

    @pytest.mark.datafiles(
        os.path.join(FIXTURE_DIR, 'img4.jpg'),
        os.path.join(FIXTURE_DIR, 'img5.jpg'),
        )
    def test_brightness(datafiles):
        for img in datafiles.listdir():
            print(img)
            #assert process(img) == some_expected_value

Example 3
~~~~~~~~~

If all (or many) of your tests rely on the same files it can be easier to
define one decorator beforehand and apply it to every test.

.. code-block:: python

    import os
    import pytest

    FIXTURE_DIR = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'test_files',
        )

    ALL_IMGS = pytest.mark.datafiles(
        os.path.join(FIXTURE_DIR, 'img1.jpg'),
        os.path.join(FIXTURE_DIR, 'img2.jpg'),
        os.path.join(FIXTURE_DIR, 'img3.jpg'),
        os.path.join(FIXTURE_DIR, 'img4.jpg'),
        os.path.join(FIXTURE_DIR, 'img5.jpg'),
        os.path.join(FIXTURE_DIR, 'img6.jpg'),
        os.path.join(FIXTURE_DIR, 'img7.jpg'),
        os.path.join(FIXTURE_DIR, 'img8.jpg'),
        )

    @ALL_IMGS
    def test_something1(datafiles):
        for img in datafiles.listdir():
            print(img)
            #assert process(img) == some_expected_value

    @ALL_IMGS
    def test_something2(datafiles):
        for img in datafiles.listdir():
            print(img)
            #assert process(img) == some_expected_value

Example 4
~~~~~~~~~

Imagine you have 3 directories (*dir1*, *dir2*, *dir3*) each containing the
files (*fileA* and *fileB*).

This example might help to clarify the options **on_duplicate** and
**keep_top_dir**.

.. code-block:: python

    import os
    import pytest

    FIXTURE_DIR = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '_fixture_files',
        )

    @pytest.mark.datafiles(
        os.path.join(FIXTURE_DIR, 'dir1'),
        os.path.join(FIXTURE_DIR, 'dir2'),
        os.path.join(FIXTURE_DIR, 'dir3'),
        on_duplicate='ignore',
        )
    def test_dir_ignore(datafiles):
        # datafiles.listdir() will list fileA and fileB originally from dir1
        pass

    @pytest.mark.datafiles(
        os.path.join(FIXTURE_DIR, 'dir1'),
        os.path.join(FIXTURE_DIR, 'dir2'),
        os.path.join(FIXTURE_DIR, 'dir3'),
        on_duplicate='replace',
        )
    def test_dir_replace(datafiles):
        # datafiles.listdir() will list fileA and fileB originally from dir3
        pass

    @pytest.mark.datafiles(
        os.path.join(FIXTURE_DIR, 'dir1'),
        os.path.join(FIXTURE_DIR, 'dir2'),
        os.path.join(FIXTURE_DIR, 'dir3'),
        # on_duplicate='exception' is the default and does not need to be
        # specified
        )
    def test_dir_exception(datafiles):
        # An exception will be raised because of duplicate filename fileA
        pass

    @pytest.mark.datafiles(
        os.path.join(FIXTURE_DIR, 'dir1'),
        os.path.join(FIXTURE_DIR, 'dir2'),
        os.path.join(FIXTURE_DIR, 'dir3'),
        keep_top_dir=True,
        )
    def test_dir_keep_top_dir(datafiles):
        # datafiles.listdir() will list dir1, dir2 and dir3 (each containing
        # fileA and fileB)
        pass

Example 5
~~~~~~~~~

You can also use py.path object instead of str paths.

.. code-block:: python

    import os
    import py
    import pytest

    _dir = os.path.dirname(os.path.realpath(__file__))
    FIXTURE_DIR = py.path.local(_dir) / 'test_files'

    @pytest.mark.datafiles(
        FIXTURE_DIR / 'img1.jpg',
        FIXTURE_DIR / 'img2.jpg',
        FIXTURE_DIR / 'img3.jpg',
        )
    def test_fast_forward(datafiles):
        assert len(datafiles.listdir()) == 3


Contributing
------------

Contributions are very welcome. Tests can be run with `tox`_, please
ensure the coverage at least stays the same before you submit a pull
request.


License
-------

Distributed under the terms of the `MIT license`_, "pytest-datafiles" is
free and open source software.


Issues
------

If you encounter any problems, please `file an issue`_ along with a
detailed description.


Acknowledgements
----------------

Thanks to `@flub`_ for the idea to use `pytest`_ marks to solve the
problem this plugin is trying to solve.

Some ideas to improve this project were taken from the `Cookiecutter`_
templates `cookiecutter-pypackage`_ and `cookiecutter-pytest-plugin`_.


.. _`pytest`: https://pytest.org/latest/contents.html
.. _`tmpdir`: https://pytest.org/latest/tmpdir.html
.. _`tox`: https://tox.readthedocs.org/en/latest/
.. _`MIT License`: http://opensource.org/licenses/MIT
.. _`file an issue`: https://github.com/omarkohl/pytest-datafiles/issues
.. _`@flub`: https://github.com/flub
.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
