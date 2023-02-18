.PHONY: clean-pyc clean-build docs clean

help:
	@echo "clean        Remove all build, test, coverage and Python artifacts"
	@echo "clean-build  Remove build artifacts"
	@echo "clean-pyc    Remove Python file artifacts"
	@echo "clean-test   Remove test and coverage artifacts"
	@echo "lint         Check style with Flake8 and Pylint"
	@echo "test         Run tests quickly with Python 3.11"
	@echo "test-all     Run tests on every Python version with tox"
	@echo "coverage     Check code coverage quickly with Python 3"
	@echo "dist         Package"
	@echo "README.rst   Generate README.rst from docs/readme"

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

all: lint test-all coverage dist readme

lint:
	tox -e lint

test: test-example | test-quick

test-quick:
	tox -e py311

test-all: test-example | test-all-env

test-all-env:
	tox

test-example:
	tox -e examples

coverage:
	tox -e coverage
	command -v xdg-open && xdg-open htmlcov/index.html || true

dist: readme | clean
	python3 setup.py sdist
	python3 setup.py bdist_wheel
	ls -l dist

readme:
	touch README.rst
	tox -e doc
