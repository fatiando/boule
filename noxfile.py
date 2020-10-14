"""
Configuration for setting up virtual environments to run tests, build
documentation, and check code style.
"""
from glob import glob

import nox


PACKAGE = "boule"
PYTHON_VERSIONS = ["3.8", "3.7", "3.6"]
PYLINT_FILES = [PACKAGE, "setup.py"]
FLAKE8_FILES = [PACKAGE, "setup.py", "doc/conf.py"]
BLACK_FILES = [PACKAGE, "setup.py", "doc/conf.py", "tutorials"]
PYTEST_ARGS = [
    "--cov-config=.coveragerc",
    "--cov-report=term-missing",
    f"--cov={PACKAGE}",
    "--doctest-modules",
    '--doctest-glob="*.rst"',
    "-v",
    "--pyargs",
]
RST_FILES = glob("doc/**/*.rst")


# Configure Nox
nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = ("black_check", "flake8", "pylint", "test")


@nox.session(python=["3.7"])
def format(session):
    """
    Run black to format the code
    """
    session.install("black")
    session.run("black", *BLACK_FILES)


@nox.session(python=["3.7"])
def black_check(session):
    """
    Check code style using black
    """
    session.install("black")
    session.run("black", "--check", *BLACK_FILES)


@nox.session(python=["3.7"])
def flake8(session):
    """
    Check code style using flake8
    """
    session.install("flake8")
    session.run("flake8", *FLAKE8_FILES)


@nox.session(python=["3.7"])
def pylint(session):
    """
    Check code style using pylint
    """
    session.install("pylint==2.4.*")
    session.run("pylint", *PYLINT_FILES)


@nox.session(python=["3.7"])
def docs(session):
    """
    Build the documentation pages
    """
    session.install("-r", "env/requirements-docs.txt", "-r", "requirements.txt")
    # Install the package
    session.install("--no-deps", "-e", ".")
    # Generate the API reference
    session.run(
        "sphinx-autogen",
        "-i",
        "-t",
        "doc/_templates",
        "-o",
        "doc/api/generated",
        "doc/api/index.rst",
    )
    # Build the HTML pages
    session.run("sphinx-build", "-d", "doc/_build/doctrees", "doc", "doc/_build")


@nox.session(python=PYTHON_VERSIONS)
def test(session):
    """
    Run the test and measure coverage (using pip)
    """
    session.install("-r", "env/requirements-test.txt", "-r", "requirements.txt")
    # Install the package
    session.install("--no-deps", "-e", ".")
    session.run("pytest", *PYTEST_ARGS, PACKAGE, *RST_FILES)


@nox.session(venv_backend="conda", python=PYTHON_VERSIONS)
def test_conda(session):
    """
    Run the tests and measure coverage (using conda)
    """
    session.conda_install(
        "--file", "env/requirements-test.txt", "--file", "requirements.txt"
    )
    # Install the package
    session.install("--no-deps", "-e", ".")
    session.run("pytest", *PYTEST_ARGS, PACKAGE, *RST_FILES)
