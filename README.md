# pytest-datafiles

[![PyPI version](https://img.shields.io/pypi/v/pytest-datafiles.svg)](https://pypi.python.org/pypi/pytest-datafiles)
[![Code Climate](https://codeclimate.com/github/omarkohl/pytest-datafiles/badges/gpa.svg)](https://codeclimate.com/github/omarkohl/pytest-datafiles)

[pytest](https://docs.pytest.org/en/latest/contents.html) plugin to create a [tmp_path](https://docs.pytest.org/en/latest/how-to/tmp_path.html) containing a preconfigured set of files and/or directories.

**Note about maintenance:** This project is maintained and bug reports or pull requests will be addressed. There is little activity because it simply works and no changes are required.

## Features

This plugin allows you to specify one or several files/directories that are copied to a temporary directory ([tmp_path](https://docs.pytest.org/en/latest/how-to/tmp_path.html)) before the execution of the test. This means the original files are not modified and every test runs on its own version of the same files.

Files/directories can be specified either as *strings* or as *pathlib.Path* objects.

To take advantage of the *datafiles* fixture in a test function, add *datafiles* as one of the test function parameters (per usual with [pytest](https://docs.pytest.org/en/latest/contents.html) fixtures) and decorate the test function with *@pytest.mark.datafiles(file1, file2, dir1, dir2, ...)*. See the examples below.

The *datafiles* variable in your test function is a pathlib.Path object ([tmp_path](https://docs.pytest.org/en/latest/how-to/tmp_path.html)) where the copied files are located. Under Linux systems this will most likely be some subdirectory of */tmp/*.

## Options

The following options can be specified as keyword arguments (kwargs) to the *@pytest.mark.datafiles* decorator function:

- **keep_top_dir:** For all parameters that represent directories, keep that directory instead of only (recursively) copying its content. Possible values are *True* or *False*. *False* is the default value.
- **on_duplicate:** Specify the action to take when duplicate files/directories are found. Possible values are: *exception*, *ignore* and *replace*. The default value is *exception*.
  - *exception:* An exception is raised instead of copying the duplicate file/directory.
  - *ignore:* The second (or subsequent) files/directories with the same name as the first one are simply ignored (i.e., the first file/directory with the duplicate name is kept).
  - *replace:* The second (or subsequent) files/directories with the same name replace the previous ones (i.e., the last file/directory with the duplicate name is kept).

See below for some *examples*.

## Installation

```bash
pip install pytest-datafiles
```

## Upgrade to 3.0

Version 3 now uses [tmp_path](https://docs.pytest.org/en/latest/how-to/tmp_path.html), resulting in `pathlib.Path` objects instead of `py.path`.

Your tests may need to be adjusted. In `examples/example_upgradev3.py` you see some possible variations.

## Usage

The full code with more details for the examples can be found in `examples/`.

### Example 1

One possible use case is when you are running tests on very big files that are not included or packaged with your tests. For example, your test files are large video files stored under */opt/big_files/*. You don't want your tests modifying the original files, but the files are required by the tests. You can reference these data files in your test method as follows:

```python
# more details in `examples/example_1.py`

@pytest.mark.datafiles('/opt/big_files/film1.mp4')
def test_fast_forward(datafiles):
    # ...
```

### Example 2

Now for another use case: let's say in the directory where your tests are located, you place a directory named *test_files*. Here you have a lot of images you want to run tests on. By using this plugin, you make sure the original files under *test_files* are not modified by every test.

```python
# more details in `examples/example_2.py`

@pytest.mark.datafiles(
    FIXTURE_DIR / 'img1.jpg',
    FIXTURE_DIR / 'img2.jpg',
    FIXTURE_DIR / 'img3.jpg',
)
def test_find_borders(datafiles):
    # ...
```

### Example 3

If all (or many) of your tests rely on the same files it can be easier to define one decorator beforehand and apply it to every test like this example:

```python
# more details in `examples/example_3.py`

ALL_IMGS = pytest.mark.datafiles(
    FIXTURE_DIR / 'img1.jpg',
    FIXTURE_DIR / 'img2.jpg',
    FIXTURE_DIR / 'img3.jpg',
)

@ALL_IMGS
def test_something1(datafiles):
    # ...
```

### Example 4

Imagine you have 3 directories (*dir1*, *dir2*, *dir3*) each containing the files (*fileA* and *fileB*).

This example clarifies the options **on_duplicate** and **keep_top_dir**.

### Example 5

You can also use a str paths.

```python
# more details in `examples/example_5.py`

@pytest.mark.datafiles(
    os.path.join(FIXTURE_DIR, 'img1.jpg'),
    os.path.join(FIXTURE_DIR, 'img2.jpg'),
    os.path.join(FIXTURE_DIR, 'img3.jpg'),
)
def test_str(datafiles):
    # ...
```

## Contributing

Contributions are very welcome. Tests can be run with `make test`. Please ensure the coverage stays at least the same before you submit a pull request.

## Releasing

To create and upload a new package, update the version number in `pyproject.toml` and `CHANGELOG.md`, then:

```bash
# Run tests and linting
make test
make lint

# Build the distribution
make clean
make dist

# Optional: Test on TestPyPI first
uv publish --publish-url https://test.pypi.org/legacy/

# Verify the package is usable
uv venv test-venv --python 3.11
source test-venv/bin/activate
uv pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pytest-datafiles
pytest examples/example_2.py
deactivate

# Create git tag (using jj)
jj tag set 3.0.1 -r @-
jj git push
git push --tags

# Upload to PyPI
uv publish

# Create GitHub release
gh release create 3.0.1 \
  --title "pytest-datafiles 3.0.1" \
  --notes-from-tag \
  dist/*
```

**Authentication:** Set the `UV_PUBLISH_TOKEN` environment variable with your PyPI API token, or `uv publish` will prompt for credentials.

Of course this will only work if you have the necessary PyPI credentials for this package.

## License

Distributed under the terms of the [MIT license](http://opensource.org/licenses/MIT), "pytest-datafiles" is free and open source software.

## Issues

If you encounter any problems, please [file an issue](https://github.com/omarkohl/pytest-datafiles/issues) along with a detailed description.

## Acknowledgements

Thanks to [@flub](https://github.com/flub) for the idea to use [pytest](https://docs.pytest.org/en/latest/contents.html) marks to solve the problem this plugin is trying to solve.

Some ideas to improve this project were taken from the [Cookiecutter](https://github.com/audreyr/cookiecutter) templates [cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) and [cookiecutter-pytest-plugin](https://github.com/pytest-dev/cookiecutter-pytest-plugin).
