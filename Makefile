# Automation to help development. Provides rules to run nox commands. See the
# noxfile.py for the actual commands to build and test the project.
#
help:
	@echo "Commands:"
	@echo ""
	@echo "  format    run black to automatically format the code"
	@echo "  install   install in editable mode"
	@echo "  check     run code style and quality checks (black, flake8 and pylint)"
	@echo "  test      run the test suite (including doctests) and report coverage"
	@echo "  docs      build the documentation"
	@echo "  clean     clean up build and generated files"
	@echo ""

install:
	pip install --no-deps -e .

test:
	nox -s test

format:
	nox -s format

check:
	nox -s check

docs:
	nox -s docs

clean:
	nox -s clean
