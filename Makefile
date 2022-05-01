.PHONY: clean-pyc clean-build docs clean

help:
	@echo "clean        Remove all build, test, coverage and Python artifacts"
	@echo "clean-build  Remove build artifacts"
	@echo "clean-pyc    Remove Python file artifacts"
	@echo "clean-test   Remove test and coverage artifacts"
	@echo "lint         Check style with Flake8 and Pylint"
	@echo "test         Run tests quickly with Python 3.5"
	@echo "test-all     Run tests on every Python version with tox"
	@echo "coverage     Check code coverage quickly with Python 3"
	@echo "dist         Package"

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
	tox -e py35

test-all:
	tox

coverage:
	tox -e coverage
	xdg-open htmlcov/index.html

dist: clean
	python3 setup.py sdist
	python3 setup.py bdist_wheel
	ls -l dist
