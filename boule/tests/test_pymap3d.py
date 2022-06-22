# Copyright (c) 2019 The Boule Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Test the pymap3d integration.
"""
import numpy as np
import numpy.testing as npt
import pymap3d
import pymap3d.latitude
import pytest

from .. import MOON, VENUS, WGS84, Ellipsoid


@pytest.mark.parametrize(
    "ellipsoid,coordinates",
    [
        (WGS84, (42.014671, -82.006479, 276.9)),
        (MOON, (41.823366, -82.006479, 4631727)),
        (VENUS, (41.823366, -82.006479, 317000)),
    ],
    ids=["WGS84", "Moon", "Venus"],
)
def test_pymap3d_integration_different_ellipsoids(ellipsoid, coordinates):
    "Check that Boule Ellipsoids and Spheres work with pymap3d functions"
    # Test values come from the pymap3d tests. Values for the Moon, Mars, Venus
    # were modified because our definitions are slightly different.
    calculated_coordinates = pymap3d.ecef2geodetic(
        x=660e3, y=-4700e3, z=4247e3, ell=ellipsoid
    )
    npt.assert_allclose(coordinates[:2], calculated_coordinates[:2], rtol=0, atol=1e-6)
    npt.assert_allclose(coordinates[2], calculated_coordinates[2], rtol=0, atol=1)


def test_pymap3d_integration_axis_only():
    "Check that Boule works with pymap3d functions that only need the axis"
    ellipsoid = Ellipsoid(
        name="test",
        semimajor_axis=1.0,
        flattening=0.5,
        geocentric_grav_const=0,
        angular_velocity=0,
    )
    x, y, z = pymap3d.geodetic2ecef(lat=0, lon=0, alt=1, ell=ellipsoid)
    npt.assert_allclose([x, y, z], [2, 0, 0], rtol=0, atol=1e-10)
    x, y, z = pymap3d.geodetic2ecef(lat=90, lon=0, alt=2, ell=ellipsoid)
    npt.assert_allclose([x, y, z], [0, 0, 2.5], rtol=0, atol=1e-10)


def test_pymap3d_integration_eccentricity():
    "Check that Boule works with pymap3d functions that need the eccentricity"
    # Test values come from the pymap3d tests
    latitude = pymap3d.latitude.geodetic2authalic(np.array([0, 90, -90, 45]), ell=WGS84)
    true_latitude = np.array([0, 90, -90, 44.87170288])
    npt.assert_allclose(latitude, true_latitude, rtol=0, atol=1e-6)


def test_pymap3d_integration_thirdflattening():
    "Check that Boule works with pymap3d funcs that need the 3rd flattening"
    # These need the eccentricity
    latitude = pymap3d.latitude.geodetic2rectifying(
        np.array([0, 90, -90, 45]), ell=WGS84
    )
    true_latitude = np.array([0, 90, -90, 44.855682])
    npt.assert_allclose(latitude, true_latitude, rtol=0, atol=1e-6)
