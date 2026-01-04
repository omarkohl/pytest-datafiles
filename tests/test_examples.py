"""
Tests for the examples.
"""

import shutil
from pathlib import Path

import pytest
from _pytest.config import ExitCode
from _pytest.pytester import Pytester

EXAMPLE_DIR = Path(__file__).parent.parent.resolve() / "examples"


@pytest.fixture
def example_files(pytester: Pytester):
    """Get all examples and dependencies into the testing env."""
    shutil.copytree(EXAMPLE_DIR, pytester.path, dirs_exist_ok=True)
    return pytester


@pytest.mark.parametrize(
    ("example", "expected"),
    [
        ("example_1", ExitCode.TESTS_FAILED),
        ("example_2", ExitCode.OK),
        ("example_3", ExitCode.OK),
        ("example_4", ExitCode.TESTS_FAILED),
        ("example_5", ExitCode.OK),
        ("example_upgradev3", ExitCode.OK),
    ],
)
def test_examples(example_files, example, expected):  # pylint: disable=W0621
    """
    Smoke test all provided examples.

    For those with expected failures, additional tests have been
    created to validate the correctness of the failure.
    """
    result = example_files.runpytest(f"{example}.py")
    assert result.ret == expected


def test_example_1_ok(example_files):  # pylint: disable=W0621
    """
    Example 1 is referring to a file in '/opt'.

    For the smoke test, just use a local existing file.
    """
    target_file = example_files.path / "film1.mp4"
    target_file.write_text("dummy")

    example = (
        (example_files.path / "example_1.py")
        .read_text()
        .replace("/opt/big_files/film1.mp4", str(target_file))
    )

    new_example = example_files.makepyfile(example)
    result = example_files.runpytest(new_example)
    assert result.ret == ExitCode.OK


def test_example_4_ok(example_files):  # pylint: disable=W0621
    """
    Example 4 contains an expected failure during test setup, that cannot
    be captured in a nice way without disturbing the example.
    """
    result = example_files.runpytest("example_4.py")

    assert result.ret == ExitCode.TESTS_FAILED
    result.assert_outcomes(passed=4, errors=1)

    result.stdout.fnmatch_lines(
        [
            "*ERROR at setup of test_dir_exception*",
            "E*ValueError: *already exists*",
        ]
    )
