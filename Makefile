# Build, package, test, and clean
PROJECT=boule

help:
	@echo "Commands:"
	@echo ""
	@echo "  format    run black to automatically format the code"
	@echo "  install   install in editable mode"
	@echo "  check     run code style and quality checks (black and flake8)"
	@echo "  lint      run pylint for a deeper (and slower) quality check"
	@echo "  test      run the test suite (including doctests) and report coverage"
	@echo "  docs      build the documentation"
	@echo "  serve     serve the documentation at http://localhost:8000"
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

serve: docs
	cd doc/_build/html && python -m http.server 8000

clean:
	find $(PROJECT) -name "*.pyc" -exec rm -v {} \;
	find . -name ".coverage.*" -exec rm -v {} \;
	rm -rvf build dist \
		MANIFEST \
		*.egg-info \
		__pycache__ \
		.coverage \
		.cache \
		.pytest_cache \
		doc/_build/ \
		doc/api/generated \
		doc/gallery \
		doc/tutorials \
		doc/sample_data \
		doc/.ipynb_checkpoints
