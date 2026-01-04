.PHONY: all clean clean-build clean-pyc clean-test lint test test-all coverage dist help

help:
	@echo "clean        Remove all build, test, coverage and Python artifacts"
	@echo "clean-build  Remove build artifacts"
	@echo "clean-pyc    Remove Python file artifacts"
	@echo "clean-test   Remove test and coverage artifacts"
	@echo "lint         Check formatting and run linter with ruff"
	@echo "format       Format code with ruff"
	@echo "test         Run tests with pytest"
	@echo "test-all     Run tests across all Python versions (3.8-3.13)"
	@echo "coverage     Check code coverage with pytest-cov"
	@echo "dist         Build package with uv"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache/
	rm -fr .ruff_cache/

all: lint test coverage dist

format:
	uv run ruff format .

lint:
	uv run ruff format --check .
	uv run ruff check .

test:
	uv run pytest tests/ -v

test-all:
	@echo "Testing with Python 3.8..."
	uv run --python 3.8 pytest tests/ -v
	@echo "Testing with Python 3.9..."
	uv run --python 3.9 pytest tests/ -v
	@echo "Testing with Python 3.10..."
	uv run --python 3.10 pytest tests/ -v
	@echo "Testing with Python 3.11..."
	uv run --python 3.11 pytest tests/ -v
	@echo "Testing with Python 3.12..."
	uv run --python 3.12 pytest tests/ -v
	@echo "Testing with Python 3.13..."
	uv run --python 3.13 pytest tests/ -v

coverage:
	uv run pytest --cov=pytest_datafiles --cov-report=html --cov-report=term tests/

dist: clean
	uv build
	ls -l dist
