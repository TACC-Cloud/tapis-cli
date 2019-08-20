PYTEST_OPTS ?= -v --durations=10
PYTEST_SRC ?= tests/
PYTEST_MAX_FAIL ?= 1
PYTEST_FAIL_OPTS ?= --maxfail=$(PYTEST_MAX_FAIL)
PYTEST_RUN_OPTS ?= $(PYTEST_FAIL_OPTS)

.PHONY: tests
tests:
	python -m pytest $(PYTEST_RUN_OPTS) $(PYTEST_OPTS) $(PYTEST_SRC)

.PHONY: format format-code format-tests
format: format-code format-tests

format-code:
	yapf --recursive --style pep8 -i tapis_cli

format-tests:
	yapf --recursive --style pep8 -i tests

.PHONY: docs
docs: docs-clean docs-autodoc docs-text

docs-text:
	cd docs && make html && make man

docs-autodoc:
# 	cd docs && sphinx-apidoc --maxdepth 1 -M -H "API Reference" -f -o source ../tapis_cli

docs-clean:
	cd docs && make clean
