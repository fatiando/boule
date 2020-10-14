"""
Configuration for setting up virtual environments to run tests, build
documentation, and check code style.

Use 'nox -l' to see a list of all sessions available and 'nox -s SESSION_NAME'
to run a session. Use '-rs' instead of '-s' to avoid creating new virtual
environments all the time.
"""
from pathlib import Path
import shutil

import nox


PACKAGE = "boule"
PYTHON_VERSIONS = ["3.8", "3.7", "3.6"]
DOCS = Path("doc")
REQUIREMENTS = {
    "run": "requirements.txt",
    "test": str(Path("env") / "requirements-test.txt"),
    "docs": str(Path("env") / "requirements-docs.txt"),
}

PYLINT_FILES = [PACKAGE, "setup.py"]
FLAKE8_FILES = [PACKAGE, "setup.py", str(DOCS / "conf.py")]
BLACK_FILES = [PACKAGE, "setup.py", str(DOCS / "conf.py"), "tutorials", "noxfile.py"]

# Use absolute paths for pytest otherwise it struggles to pick up coverage info
PYTEST_ARGS = [
    f"--cov-config={Path('.coveragerc').resolve()}",
    "--cov-report=term-missing",
    f"--cov={PACKAGE}",
    "--doctest-modules",
    '--doctest-glob="*.rst"',
    "-v",
    "--pyargs",
]
RST_FILES = [str(p.resolve()) for p in Path("doc").glob("**/*.rst")]


# Configure Nox
nox.options.sessions = ("black_check", "flake8", "pylint", "test")


@nox.session()
def black_check(session):
    """
    Check code style using black
    """
    session.install("black")
    list_packages(session)
    session.run("black", "--check", *BLACK_FILES)


@nox.session()
def flake8(session):
    """
    Check code style using flake8
    """
    session.install("flake8")
    list_packages(session)
    session.run("flake8", *FLAKE8_FILES)


@nox.session()
def pylint(session):
    """
    Check code style using pylint
    """
    session.install("pylint==2.4.*")
    list_packages(session)
    session.run("pylint", *PYLINT_FILES)


@nox.session()
def format(session):
    """
    Run black to format the code
    """
    session.install("black")
    session.run("black", *BLACK_FILES)


def build_and_install(session):
    """
    Build source and wheel packages for the project and install them
    """
    if Path("dist").exists():
        shutil.rmtree("dist")
    session.install("wheel")
    session.run("python", "setup.py", "sdist", "bdist_wheel", silent=True)
    wheel = [str(p) for p in Path("dist").glob("*.whl")]
    assert len(wheel) == 1, f"More than 1 wheel present: {wheel}"
    session.install("--no-deps", wheel[0])
    # session.install("--no-deps", "-e", ".")


@nox.session(python=PYTHON_VERSIONS)
def test(session):
    """
    Run the tests and measure coverage (using pip)
    """
    session.install("-r", REQUIREMENTS["test"], "-r", REQUIREMENTS["run"])
    build_and_install(session)
    list_packages(session)
    run_pytest(session)


@nox.session(venv_backend="conda", python=PYTHON_VERSIONS)
def test_conda(session):
    """
    Run the tests and measure coverage (using conda)
    """
    session.conda_install("--file", REQUIREMENTS["test"], "--file", REQUIREMENTS["run"])
    build_and_install(session)
    list_packages(session, package_manager="conda")
    run_pytest(session)


@nox.session()
def docs(session):
    """
    Build the documentation
    """
    session.install("-r", REQUIREMENTS["docs"], "-r", REQUIREMENTS["run"])
    list_packages(session)
    build_and_install(session)
    # Generate the API reference
    session.run(
        "sphinx-autogen",
        "-i",
        "-t",
        str(DOCS / "_templates"),
        "-o",
        str(DOCS / "api" / "generated"),
        str(DOCS / "api" / "index.rst"),
    )
    # Build the HTML pages
    session.run(
        "sphinx-build",
        "-d",
        str(DOCS / "_build" / "doctrees"),
        "doc",
        str(DOCS / "_build" / "html"),
    )


@nox.session
def clean(session):
    """
    Remove all files generated by the build process
    """
    files = [
        Path("build"),
        Path("dist"),
        Path("MANIFEST"),
        Path(".coverage"),
        Path(".pytest_cache"),
        Path("__pycache__"),
        DOCS / "_build",
        DOCS / "api" / "generated",
        DOCS / "gallery",
        DOCS / "tutorials",
    ]
    files.extend(Path(PACKAGE).glob("**/*.pyc"))
    files.extend(Path(".").glob(".coverage.*"))
    files.extend(Path(PACKAGE).glob("**/__pycache__"))
    files.extend(Path(".").glob("*.egg-info"))
    files.extend(Path(".").glob("**/.ipynb_checkpoints"))
    for f in files:
        if f.exists():
            session.log(f"removing: {f}")
            if f.is_dir():
                shutil.rmtree(f)
            else:
                f.unlink()


# UTILITY FUNCTIONS
###############################################################################


def list_packages(session, package_manager="pip"):
    """
    List installed packages in the virtual environment.

    If the argument 'list-packages' is passed to the nox session, will list the
    installed packages in the virtual environment (using the package manager
    specified).

    Example: 'nox -s test-3.7 -- list-packages'
    """
    if package_manager not in {"pip", "conda"}:
        raise ValueError(f"Invalid package manager '{package_manager}'")
    if session.posargs and "list-packages" in session.posargs:
        if package_manager == "pip":
            session.run("pip", "freeze")
        elif package_manager == "conda":
            session.run("conda", "list")


def run_pytest(session):
    """
    Run tests with pytest in a separate folder.
    """
    tmpdir = session.create_tmp()
    session.cd(tmpdir)
    session.run("pytest", *PYTEST_ARGS, PACKAGE, *RST_FILES)
    session.run("coverage", "xml", "-o", ".coverage.xml")
    # Copy the coverage information back so it can be reported
    for f in Path(".").glob(".coverage*"):
        shutil.copy(f, Path(__file__).parent)
