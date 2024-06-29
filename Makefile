#Makefile

# Avoid create extra files (used as automization for a python app)
.PHONY: install virtualenv ipython clean test watch

# @ => don´t show command on the screen
install:
	@echo "Installind Dundie into Dev Environment"
	@.venv/bin/python -m pip install -e '.[dev]'

virtualenv:
	@.venv/bin/python -m pip -m venv .venv

ipython:
	@.venv/bin/ipython

test:
	@.venv/bin/pytest -vv -s

testci:
	@.venv/bin/pytest -v --junitxml=test-results.xml

watch:
# @.venv/bin/ptw --  -vv -s  tests/ integration/
	@ls **/*.py | entr pytest

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
	@rm -rf docs/_buildclean:
	@fin
