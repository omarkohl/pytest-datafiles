.PHONY: clean-pyc clean-build docs clean

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with Flake8 and Pylint"
	@echo "test - run tests quickly with Python 3.4"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with Python 3.4"
	@echo "dist - package"

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

lint:
	tox -e lint

test:
	tox -e py34

test-all:
	tox

coverage:
	tox -e coverage
	xdg-open htmlcov/index.html

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

