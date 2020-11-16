# Copyright (c) 2019 The Boule Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
# pylint: disable=missing-docstring,import-outside-toplevel
# Import functions/classes to make the public API
from . import version
from .ellipsoid import Ellipsoid
from .realizations import WGS84, GRS80, MARS, VENUS, MOON, MERCURY


ELLIPSOIDS = [WGS84, GRS80, MARS, VENUS, MOON, MERCURY]

# Get the version number through setuptools-scm
__version__ = version.version


def test(doctest=True, verbose=True):
    """
    Run the test suite.

    Uses `py.test <http://pytest.org/>`__ to discover and run the tests.

    Parameters
    ----------

    doctest : bool
        If ``True``, will run the doctests as well (code examples that start
        with a ``>>>`` in the docs).
    verbose : bool
        If ``True``, will print extra information during the test run.

    Raises
    ------

    AssertionError
        If pytest returns a non-zero error code indicating that some tests have
        failed.

    """
    import pytest

    package = __name__
    args = []
    if verbose:
        args.append("-vv")
    if doctest:
        args.append("--doctest-modules")
    args.append("--pyargs")
    args.append(package)
    status = pytest.main(args)
    assert status == 0, "Some tests have failed."
