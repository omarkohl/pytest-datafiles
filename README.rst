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


`pytest`_ plugin to create a `tmp_path`_ containing a preconfigured set of
files and/or directories.

**Note about maintenance:** This project is maintained and bug reports or pull
requests will be addressed. There is little activity because it simply works and
no changes are required.

Features
--------

This plugin allows you to specify one or several files/directories that are
copied to a temporary directory (`tmp_path`_) before the execution of the test.
This means the original files are not modified and every test runs on its own
version of the same files.

Files/directories can be specified either as *strings* or as *pathlib.Path* objects.

To take advantage of the *datafiles* fixture in a test function, add
*datafiles* as one of the test function parameters (per usual with `pytest`_
fixtures) and decorate the test function with *@pytest.mark.datafiles(file1,
file2, dir1, dir2, ...)*. See the examples below.

The *datafiles* variable in your test function is a pathlib.Path object
(`tmp_path`_) where the copied files are located. Under Linux systems this
will most likely be some subdirectory of */tmp/*.


Options
-------

The following options can be specified as keyword arguments (kwargs) to the
*@pytest.mark.datafiles* decorator function:

- **keep_top_dir:** For all parameters that represent directories, keep that
  directory instead of only (recursively) copying its content. Possible values
  are *True* or *False*. *False* is the default value.
- **on_duplicate:** Specify the action to take when duplicate files/directories
  are found. Possible values are: *exception*, *ignore* and *replace*. The
  default value is *exception*.

  - *exception:* An exception is raised instead of copying the duplicate
    file/directory.
  - *ignore:* The second (or subsequent) files/directories with the same name
    as the first one are simply ignored (i.e., the first file/directory with the
    duplicate name is kept).
  - *replace:* The second (or subsequent) files/directories with the same name
    replace the previous ones (i.e., the last file/directory with the duplicate
    name is kept).

See below for some *examples*.


Installation
------------

.. code-block:: bash

    pip install pytest-datafiles


Upgrade to 3.0
--------------

Version 3 now uses `tmp_path`_, resulting in `pathlib.Path` objects
instead of `py.path`.

Your tests may need to be adjusted. In `examples/example_upgradev3.py` you see some possible
variations.


Usage
-----

The full code with more details for the examples can be found in `examples/`.

Example 1
~~~~~~~~~

One possible use case is when you are running tests on very big files that are
not included or packaged with your tests. For example, your test files are
large video files stored under */opt/big_files/* . You don't want your tests modifying
the original files, but the files are required by the tests. You can reference these
data files in your test method as follows:

.. code-block:: python

    # more details in `examples/example_1.py`

    @pytest.mark.datafiles('/opt/big_files/film1.mp4')
    def test_fast_forward(datafiles):
        # ...


Example 2
~~~~~~~~~

Now for another use case: let's say in the directory where your tests are located, you
place a directory named *test_files*. Here you have a lot of images you want to run tests
on. By using this plugin, you make sure the original files under *test_files* are not
modified by every test.

.. code-block:: python

    # more details in `examples/example_2.py`

    @pytest.mark.datafiles(
        FIXTURE_DIR / 'img1.jpg',
        FIXTURE_DIR / 'img2.jpg',
        FIXTURE_DIR / 'img3.jpg',
    )
    def test_find_borders(datafiles):
        # ...


Example 3
~~~~~~~~~

If all (or many) of your tests rely on the same files it can be easier to
define one decorator beforehand and apply it to every test like this example:

.. code-block:: python

    # more details in `examples/example_3.py`

    ALL_IMGS = pytest.mark.datafiles(
        FIXTURE_DIR / 'img1.jpg',
        FIXTURE_DIR / 'img2.jpg',
        FIXTURE_DIR / 'img3.jpg',
    )

    @ALL_IMGS
    def test_something1(datafiles):
        # ...


Example 4
~~~~~~~~~

Imagine you have 3 directories (*dir1*, *dir2*, *dir3*) each containing the files
(*fileA* and *fileB*).

This example clarifies the options **on_duplicate** and **keep_top_dir**.


Example 5
~~~~~~~~~

You can also use a str paths.

.. code-block:: python

    # more details in `examples/example_5.py`

    @pytest.mark.datafiles(
        os.path.join(FIXTURE_DIR, 'img1.jpg'),
        os.path.join(FIXTURE_DIR, 'img2.jpg'),
        os.path.join(FIXTURE_DIR, 'img3.jpg'),
    )
    def test_str(datafiles):
        # ...


Contributing
------------

Contributions are very welcome. Tests can be run with `tox`_. Please
ensure the coverage stays at least the same before you submit a pull
request.

To create and upload a new package first update the version number and then:

.. code-block:: bash

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

Finally create a release on GitHub and add the packages from dist/* to it.

Of course this will only work if you have the necessary PyPI credentials for
this package.


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


.. _`pytest`: https://docs.pytest.org/en/latest/contents.html
.. _`tmp_path`: https://docs.pytest.org/en/latest/tmp_path.html
.. _`tox`: https://tox.readthedocs.org/en/latest/
.. _`MIT License`: http://opensource.org/licenses/MIT
.. _`file an issue`: https://github.com/omarkohl/pytest-datafiles/issues
.. _`@flub`: https://github.com/flub
.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
