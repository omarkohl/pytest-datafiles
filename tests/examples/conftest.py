# pylint: skip-file
import shutil
from pathlib import Path

import pytest


def first_not_existing_parent(path: Path) -> Path:
    parent = path.parent
    if parent.exists():
        return path
    return first_not_existing_parent(parent)


@pytest.fixture(scope="session")
def example_1():
    file = Path('/tmp/big_files/film1.mp4')
    path = first_not_existing_parent(file)
    print(f'found {path}')

    file.parent.mkdir(parents=True, exist_ok=True)
    file.touch()
    yield 1
    file.unlink()
    if path.is_dir():
        shutil.rmtree(path)


@pytest.fixture(autouse=True)
def setup_examples(example_1):
    pass
