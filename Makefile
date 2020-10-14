# Build, package, test, and clean
PROJECT=boule

help:
	@echo "Commands:"
	@echo ""
	@echo "  install   install in editable mode"
	@echo "  test      run the test suite (including doctests) and report coverage"
	@echo "  format    run black to automatically format the code"
	@echo "  check     run code style and quality checks (black and flake8)"
	@echo "  lint      run pylint for a deeper (and slower) quality check"
	@echo "  clean     clean up build and generated files"
	@echo ""

install:
	pip install --no-deps -e .

test:
	nox -s test

format:
	nox -s format

check: black-check flake8

black-check:
	nox -s black_check

flake8:
	nox -s flake8

lint:
	nox -s pylint

docs:
	nox -s docs

clean:
	find $(PROJECT) -name "*.pyc" -exec rm -v {} \;
	find . -name ".coverage.*" -exec rm -v {} \;
	rm -rvf build dist MANIFEST *.egg-info __pycache__ .coverage .cache .pytest_cache
	rm -rf doc/_build/
	rm -rf doc/api/generated
	rm -rf doc/gallery
	rm -rf doc/tutorials
	rm -rf doc/sample_data
	rm -rf doc/.ipynb_checkpoints
