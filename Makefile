PACKAGE := typepy
DOCS_DIR := docs
DOCS_BUILD_DIR := $(DOCS_DIR)/_build


.PHONY: build
build:
	@make clean
	@tox -e build
	ls -lh dist/*

.PHONY: check
check:
	@tox -e lint

.PHONY: clean
clean:
	@tox -e clean

.PHONY: docs
docs:
	@tox -e docs

.PHONY: fmt
fmt:
	@tox -e fmt

.PHONY: readme
readme:
	tox -e readme

.PHONY: release
release:
	@python setup.py release --sign
	@make clean
	pip check

.PHONY: setup
setup:
	@pip install --upgrade -e .[test] releasecmd tox
	pip check
