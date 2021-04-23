PYTEST_OPTS ?= -v --durations=10
PYTEST_SRC ?= tests/
PYTEST_MAX_FAIL ?= 1
PYTEST_FAIL_OPTS ?= --maxfail=$(PYTEST_MAX_FAIL) --no-cov-on-fail
PYTEST_RUN_OPTS ?= $(PYTEST_FAIL_OPTS)

GIT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD 2>/dev/null)
GIT_BRANCH_CLEAN := $(shell echo $(GIT_BRANCH) | sed -e "s/[^[:alnum:]]/-/g")

CLI_BRANCH ?= $(GIT_BRANCH)
CLI_VERSION ?= "1.0.4"
IMAGE_BASENAME := tapis-cli
DOCKER_ORG ?= tacc
PUBLIC_DOCKER_IMAGE ?= $(DOCKER_ORG)/$(IMAGE_BASENAME):latest

DOCKERFILE ?= Dockerfile
DOCKER_BUILD_ARGS ?= --force-rm --build-arg CLI_BRANCH=$(CLI_BRANCH) --build-arg CLI_VERSION=$(CLI_VERSION)
DOCKER_MOUNT_AUTHCACHE ?= -v $(HOME)/.agave:/root/.agave
PUBLIC_DOCKER_MOUNT ?= -v $(CURDIR):/work
PUBLIC_DOCKER_CLI ?= docker run --rm -it $(PUBLIC_DOCKER_MOUNT) $(DOCKER_MOUNT_AUTHCACHE)

.PHONY: tests
tests:
	python -m pytest $(PYTEST_RUN_OPTS) $(PYTEST_OPTS) $(PYTEST_SRC)

.PHONY: format format-code format-tests
format: format-code format-tests

format-code:
	yapf --parallel --recursive --style pep8 -i tapis_cli

format-tests:
	yapf --parallel --recursive --style pep8 -i tests

.PHONY: docs docs/requirements.txt

docs: docs-clean docs-autodoc docs-text docs/requirements.txt

docs/requirements.txt:
	cat requirements.txt > docs/requirements.txt
	cat requirements-dev.txt >> docs/requirements.txt

docs-text:
	cd docs && make html && make man

docs-autodoc:
	cd docs && sphinx-apidoc --maxdepth 1 -M -f -o source ../tapis_cli

docs-clean:
	cd docs && make clean

issues:
	python scripts/github-create-issues.py

image: public-image-py3

public-image-py3:
	docker build $(DOCKER_BUILD_ARGS) --build-arg CLI_VERSION=$(CLI_VERSION) -f $(DOCKERFILE) -t $(PUBLIC_DOCKER_IMAGE) .

interactive:
	$(PUBLIC_DOCKER_CLI) $(PUBLIC_DOCKER_IMAGE) bash

image-release: image
	docker push $(PUBLIC_DOCKER_IMAGE)

locc:
	python scripts/locc.py -recurse tapis_cli

pypi-release: clean
	# Tag
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*

clean:
	rm -rf tapis_cli.egg-info build dist .cache
	rm -rf tests/__pycache__/
	rm -rf tests/*.pyc
	rm -rf .pytest_cache/
	rm -rf build/*
	rm -rf dist/*
