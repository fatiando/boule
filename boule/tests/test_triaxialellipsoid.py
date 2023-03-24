# Copyright (c) 2019 The Boule Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Test the base TriaxialEllipsoid class.
"""
import warnings

import numpy as np
import numpy.testing as npt
import pytest

from .. import TriaxialEllipsoid


@pytest.fixture
def triaxialellipsoid():
    "A triaxial ellipsoid"
    triaxial_ellipsoid = TriaxialEllipsoid(
        name="Base triaxial Ellipsoid",
        semimajor_axis=4,
        semimedium_axis=2,
        semiminor_axis=1,
        geocentric_grav_const=2.0,
        angular_velocity=1.3,
    )
    return triaxial_ellipsoid


def test_check_semimajor():
    """
    Check if error is raised after invalid semimajor axis
    """
    with pytest.raises(ValueError):
        TriaxialEllipsoid(
            name="zero_semimajor_axis",
            semimajor_axis=0,
            semimedium_axis=2,
            semiminor_axis=1,
            geocentric_grav_const=0,
            angular_velocity=0,
        )
    with pytest.raises(ValueError):
        TriaxialEllipsoid(
            name="negative_semimajor_axis",
            semimajor_axis=-4,
            semimedium_axis=2,
            semiminor_axis=1,
            geocentric_grav_const=0,
            angular_velocity=0,
        )


def test_check_semimedium():
    """
    Check if error is raised after invalid semimedium axis
    """
    with pytest.raises(ValueError):
        TriaxialEllipsoid(
            name="zero_semimedium_axis",
            semimajor_axis=4,
            semimedium_axis=0,
            semiminor_axis=1,
            geocentric_grav_const=0,
            angular_velocity=0,
        )
    with pytest.raises(ValueError):
        TriaxialEllipsoid(
            name="negative_semimedium_axis",
            semimajor_axis=4,
            semimedium_axis=-2,
            semiminor_axis=1,
            geocentric_grav_const=0,
            angular_velocity=0,
        )


def test_check_semiminor():
    """
    Check if error is raised after invalid semiminor axis
    """
    with pytest.raises(ValueError):
        TriaxialEllipsoid(
            name="zero_semiminor_axis",
            semimajor_axis=4,
            semimedium_axis=2,
            semiminor_axis=0,
            geocentric_grav_const=0,
            angular_velocity=0,
        )
    with pytest.raises(ValueError):
        TriaxialEllipsoid(
            name="negative_semiminor_axis",
            semimajor_axis=4,
            semimedium_axis=2,
            semiminor_axis=-1,
            geocentric_grav_const=0,
            angular_velocity=0,
        )


def test_check_semimajor_is_largest():
    """
    Check if error is raised after invalid semimajor is not the
    largest axis length
    """
    with pytest.raises(ValueError):
        TriaxialEllipsoid(
            name="largest_axis_is_semiminor_axis",
            semimajor_axis=1,
            semimedium_axis=2,
            semiminor_axis=4,
            geocentric_grav_const=0,
            angular_velocity=0,
        )
    with pytest.raises(ValueError):
        TriaxialEllipsoid(
            name="largest_axis_is_semimedium_axis",
            semimajor_axis=2,
            semimedium_axis=4,
            semiminor_axis=1,
            geocentric_grav_const=0,
            angular_velocity=0,
        )


def test_check_semiminor_is_smallest():
    """
    Check if error is raised after invalid semiminor is not the
    smallest axis length
    """
    with pytest.raises(ValueError):
        TriaxialEllipsoid(
            name="largest_axis_is_semiminor_axis",
            semimajor_axis=1,
            semimedium_axis=2,
            semiminor_axis=4,
            geocentric_grav_const=0,
            angular_velocity=0,
        )
    with pytest.raises(ValueError):
        TriaxialEllipsoid(
            name="medium_larger",
            semimajor_axis=4,
            semimedium_axis=1,
            semiminor_axis=2,
            geocentric_grav_const=0,
            angular_velocity=0,
        )


def test_check_semimedium_larger_than_semiminor():
    """
    Check if error is raised if semiminor axis length is larger than
    semimedium axis length
    """
    with pytest.raises(ValueError):
        TriaxialEllipsoid(
            name="smallest_axis_is_semimedium_axis",
            semimajor_axis=4,
            semimedium_axis=1,
            semiminor_axis=2,
            geocentric_grav_const=0,
            angular_velocity=0,
        )


def test_check_geocentric_grav_const():
    """
    Check if warn is raised after negative geocentric_grav_const
    """
    with warnings.catch_warnings(record=True) as warn:
        TriaxialEllipsoid(
            name="negative_gm",
            semimajor_axis=4,
            semimedium_axis=2,
            semiminor_axis=1,
            geocentric_grav_const=-1,
            angular_velocity=0,
        )
        assert len(warn) >= 1


def test_volume_gt_minorsphere(triaxialellipsoid):
    """
    Check that the volume is larger than a sphere of semiminor axis radius
    """
    assert (
        triaxialellipsoid.volume > 4 * np.pi / 3 * triaxialellipsoid.semiminor_axis**3
    )


def test_volume_lt_majorsphere(triaxialellipsoid):
    """
    Check that the volume is lesser than a sphere of semimajor axis radius
    """
    assert (
        triaxialellipsoid.volume < 4 * np.pi / 3 * triaxialellipsoid.semimajor_axis**3
    )


def test_geocentric_radius_poles(triaxialellipsoid):
    """
    Check against values at the poles
    """
    latitude = np.array([-90.0, -90.0, 90.0, 90.0])
    longitude = np.array([0.0, 90.0, 0.0, 90.0])
    radius_true = np.full(latitude.shape, triaxialellipsoid.semiminor_axis)
    npt.assert_allclose(
        radius_true, triaxialellipsoid.geocentric_radius(longitude, latitude)
    )


def test_geocentric_radius_equator(triaxialellipsoid):
    """
    Check against values at the equator
    """
    latitude = np.zeros(4)
    longitude = np.array([0.0, 90.0, 180.0, 270.0])
    radius_true = np.array(
        [
            triaxialellipsoid.semimajor_axis,
            triaxialellipsoid.semimedium_axis,
            triaxialellipsoid.semimajor_axis,
            triaxialellipsoid.semimedium_axis,
        ]
    )
    npt.assert_allclose(
        radius_true, triaxialellipsoid.geocentric_radius(longitude, latitude)
    )


def test_geocentric_radius_semimajor_axis_longitude(triaxialellipsoid):
    """
    Check against non-zero longitude of the semi-major axis
    """
    latitude = np.zeros(4)
    longitude = np.array([0.0, 90.0, 180.0, 270.0])
    radius_true = np.array(
        [
            triaxialellipsoid.semimedium_axis,
            triaxialellipsoid.semimajor_axis,
            triaxialellipsoid.semimedium_axis,
            triaxialellipsoid.semimajor_axis,
        ]
    )
    npt.assert_allclose(
        radius_true, triaxialellipsoid.geocentric_radius(longitude, latitude, 90.0)
    )


def test_geocentric_radius_biaxialellipsoid(triaxialellipsoid):
    """
    Check against values of a reference biaxial ellipsoid
    """
    # Get the defining parameters of "triaxialellipsoid"
    a = triaxialellipsoid.semimajor_axis
    c = triaxialellipsoid.semiminor_axis
    GM = triaxialellipsoid.geocentric_grav_const
    omega = triaxialellipsoid.angular_velocity

    # Instantiate an "Ellipsoid" class using the following defining parameters
    # of "triaxialellipsoid": semimajor axis "a", semiminor axis "c",
    # geocentric gravitational constant "GM" and angular velocity "omega"
    from .. import Ellipsoid

    biaxialellipsoid_ref = Ellipsoid("biaxell_ref", a, (a - c) / a, GM, omega)

    # Instantiate a "TriaxialEllipsoid" class such that it in fact represents
    # "biaxialellipsoid_ref"
    biaxialellipsoid = TriaxialEllipsoid("biaxell", a, a, c, GM, omega)

    latitude = np.arange(-90.0, 90.0, 1.0)
    longitude = np.linspace(0.0, 360.0, num=latitude.size, endpoint=False)

    # Compute the reference geocentric radii using the reference biaxial
    # ellipsoid
    radius_true = biaxialellipsoid_ref.geocentric_radius(latitude, geodetic=False)
    npt.assert_allclose(
        radius_true, biaxialellipsoid.geocentric_radius(longitude, latitude)
    )
