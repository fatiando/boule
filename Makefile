# Build, package, test, and clean
PROJECT=boule
CHECK_STYLE=src/$(PROJECT) doc test
GITHUB_ACTIONS=.github/workflows

.PHONY: help build install test format check check-format check-style check-actions clean

help:
	@echo "Commands:"
	@echo ""
	@echo "  install   install in editable mode"
	@echo "  test      run the test suite (including doctests) and report coverage"
	@echo "  format    automatically format the code"
	@echo "  check     run code style and quality checks"
	@echo "  build     build source and wheel distributions"
	@echo "  clean     clean up build and generated files"
	@echo ""

build:
	python -m build .

install:
	python -m pip install --no-deps --editable .

test:
	pytest --cov --doctest-modules --verbose test src/$(PROJECT)

format:
	ruff check --select I --fix $(CHECK_STYLE) # fix isort errors
	ruff format $(CHECK_STYLE)
	burocrata --extension=py $(CHECK_STYLE)

check: check-format check-style check-actions

check-format:
	ruff format --check $(CHECK_STYLE)
	burocrata --check --extension=py $(CHECK_STYLE)

check-style:
	ruff check $(CHECK_STYLE)

check-actions:
	zizmor $(GITHUB_ACTIONS)

clean:
	find . -name "*.orig" -exec rm -v {} \;
	find . -name ".coverage.*" -exec rm -v {} \;
	find . -depth -name "__pycache__" -exec rm -v {} \;
	find . -depth -name "*.egg-info " -exec rm -v {} \;
	rm -rvf build dist MANIFEST .coverage .cache .pytest_cache src/$(PROJECT)/_version.py
