#Makefile

# Avoid create extra files (used as automization for a python app)
.PHONY: install uninstall virtualenv ipython lint fmt-check fmt-apply test testci watch docs \
	docs-serve clean build twine-upload

# @ => don´t show command on the screen
install:
	@echo "Installing Dundie into Dev Environment..."
	@.venv/bin/python -m pip install -e '.[dev, test]'

uninstall:
	@.venv/bin/python -m pip uninstall dundie

virtualenv:
	@.venv/bin/python -m pip -m venv .venv

ipython:
	@.venv/bin/ipython

lint:
	@.venv/bin/pflake8

fmt-check:
	@.venv/bin/isort --check --diff dundie tests integration
	@.venv/bin/black --check --diff dundie tests integration

fmt-apply:
	@.venv/bin/isort dundie tests integration
	@.venv/bin/black dundie tests integration

test:
# @.venv/bin/pytest -vv -s --forked
	@.venv/bin/pytest -s --forked --cov=dundie
	@.venv/bin/coverage xml
	@.venv/bin/coverage html

testci:
	@.venv/bin/pytest -vv --forked --junitxml=test-result.xml

watch:
# @.venv/bin/ptw --  -vv -s  tests/ integration/
	@ls **/*.py | entr pytest --forked --cov=dundie
	@.venv/bin/coverage xml
	@.venv/bin/coverage html

docs:
	@mkdocs build --clean

docs-serve:
	@mkdocs serve

build:
	@python setup.py sdist bdist_wheel

publish-testpypi:
	@twine upload --repository testpypi dist/*

publish-pypi:
	@twine upload dist/*

clean:            ## Clean unused/temporary files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build
