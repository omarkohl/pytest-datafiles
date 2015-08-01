================
pytest-datafiles
================

.. image:: https://img.shields.io/travis/omarkohl/pytest-datafiles.svg
        :target: https://travis-ci.org/omarkohl/pytest-datafiles

.. image:: https://img.shields.io/pypi/v/pytest-datafiles.svg
	:target: https://pypi.python.org/pypi/pytest-datafiles


`pytest`_ plugin to create a `tmpdir`_ containing a preconfigured set of
files and/or directories.


Features
--------

This plugin allows you to specify one or several files that will be copied
to a temporary directory (`tmpdir`_) before the execution of the test.
This means the original files are not modified and every test runs on its
own version of the same files.

Files can be specified either as *strings* or as *py.path* objects.

The test function that wants to take advantage of this *datafiles* fixture
needs to use *datafiles* as one of its parameters (as usual with `pytest`_
fixtures) and needs to be decorated with *@pytest.mark.datafiles(file1,
file2, ...)*. See examples below.

The *datafiles* variable in your test function is a py.path object
(`tmpdir`_) where the copied files are located. Under Linux systems this
will most likely be some subdirectory of */tmp/*.

Currently only files not directories are supported but this will change in
future releases.


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

    import pytest

    @pytest.mark.datafiles('/opt/big_files/film1.mp4')
    def test_fast_forward(datafiles):
        assert len(datafiles.listdir()) == 1
        assert (datafiles / 'film1.mp4').check(file=1)
        # assert some_operation(datafiles / 'film1.mp4') == expected_result

Example 2
~~~~~~~~~

Another use case is: In the directory where your tests are located you
placed a directory named *test_files*. Here you placed a lot of
images you want to run tests on. By using this plugin you make sure the
original files under *test_files* are not modified by every test.

.. code-block:: python

    import os
    import py
    import pytest

    FIXTURE_DIR = py.path.local(
        os.path.dirname(
            os.path.realpath(__file__)
            )
        ) / 'test_files'

    @pytest.mark.datafiles(
        FIXTURE_DIR / 'img1.jpg',
        FIXTURE_DIR / 'img2.jpg',
        FIXTURE_DIR / 'img3.jpg',
        )
    def test_find_borders(datafiles):
        for img in datafiles.listdir():
            print(img)
            #assert process(img) == some_expected_value

    @pytest.mark.datafiles(
        FIXTURE_DIR / 'img4.jpg',
        FIXTURE_DIR / 'img5.jpg',
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
        for img in datafiles.listdir():
            print(img)
            #assert process(img) == some_expected_value

    @ALL_IMGS
    def test_something2(datafiles):
        for img in datafiles.listdir():
            print(img)
            #assert process(img) == some_expected_value


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
