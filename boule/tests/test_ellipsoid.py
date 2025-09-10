# Copyright (c) 2019 The Boule Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Test the base Ellipsoid class.
"""
import warnings

import numpy as np
import numpy.testing as npt
import pytest

from .. import GRS80, WGS84, Ellipsoid, Mars2009
from .utils import normal_gravity_surface

ELLIPSOIDS = [WGS84, GRS80, Mars2009]
ELLIPSOID_NAMES = [e.name for e in ELLIPSOIDS]


def test_check_flattening():
    """
    Check if error/warns is raised after invalid flattening
    """
    with pytest.raises(ValueError):
        Ellipsoid(
            name="negative_flattening",
            semimajor_axis=1.0,
            flattening=-1,
            geocentric_grav_const=0,
            angular_velocity=0,
        )
    with pytest.raises(ValueError):
        Ellipsoid(
            name="flattening_greater_than_one",
            semimajor_axis=1.0,
            flattening=1.5,
            geocentric_grav_const=0,
            angular_velocity=0,
        )
    with pytest.raises(ValueError):
        Ellipsoid(
            name="zero_flattening",
            semimajor_axis=1.0,
            flattening=0,
            geocentric_grav_const=0,
            angular_velocity=0,
        )
    with pytest.raises(ValueError):
        Ellipsoid(
            name="almost_zero_negative_flattening",
            semimajor_axis=1.0,
            flattening=-1e8,
            geocentric_grav_const=0,
            angular_velocity=0,
        )
    with warnings.catch_warnings(record=True) as warn:
        Ellipsoid(
            name="almost-zero-flattening",
            semimajor_axis=1,
            flattening=1e-8,
            geocentric_grav_const=1,
            angular_velocity=0,
        )
        assert len(warn) >= 1


def test_check_semimajor_axis():
    """
    Check if error is raised after invalid semimajor_axis
    """
    with pytest.raises(ValueError):
        Ellipsoid(
            name="zero_semimajor_axis",
            semimajor_axis=0,
            flattening=0.1,
            geocentric_grav_const=0,
            angular_velocity=0,
        )
    with pytest.raises(ValueError):
        Ellipsoid(
            name="negative_semimajor_axis",
            semimajor_axis=-1,
            flattening=0.1,
            geocentric_grav_const=0,
            angular_velocity=0,
        )


def test_check_geocentric_grav_const():
    """
    Check if warn is raised after negative geocentric_grav_const
    """
    with warnings.catch_warnings(record=True) as warn:
        Ellipsoid(
            name="negative_gm",
            semimajor_axis=1,
            flattening=0.1,
            geocentric_grav_const=-1,
            angular_velocity=0,
        )
        assert len(warn) >= 1


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_semiaxes(ellipsoid):
    """
    Check that the semimedium axis is equal to the semimajor axis and that
    the longitude of the semimajor axis is zero.
    """
    assert ellipsoid.semimedium_axis == ellipsoid.semimajor_axis
    assert ellipsoid.semimajor_axis_longitude == 0


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_geodetic_to_spherical_on_equator(ellipsoid):
    "Test geodetic to geocentric coordinates conversion on equator."
    rtol = 1e-10
    size = 5
    longitude = np.linspace(0, 180, size)
    height = np.linspace(-1e4, 1e4, size)
    latitude = np.zeros_like(size)
    sph_longitude, sph_latitude, radius = ellipsoid.geodetic_to_spherical(
        (longitude, latitude, height)
    )
    npt.assert_allclose(sph_longitude, longitude, rtol=rtol)
    npt.assert_allclose(sph_latitude, latitude, rtol=rtol)
    npt.assert_allclose(radius, height + ellipsoid.semimajor_axis, rtol=rtol)


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_geodetic_to_spherical_on_poles(ellipsoid):
    "Test geodetic to geocentric coordinates conversion on poles."
    rtol = 1e-10
    size = 5
    longitude = np.hstack([np.linspace(0, 180, size)] * 2)
    height = np.hstack([np.linspace(-1e4, 1e4, size)] * 2)
    latitude = np.array([90.0] * size + [-90.0] * size)
    sph_longitude, sph_latitude, radius = ellipsoid.geodetic_to_spherical(
        (longitude, latitude, height)
    )
    npt.assert_allclose(sph_longitude, longitude, rtol=rtol)
    npt.assert_allclose(sph_latitude, latitude, rtol=rtol)
    npt.assert_allclose(radius, height + ellipsoid.semiminor_axis, rtol=rtol)


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_spherical_to_geodetic_on_equator(ellipsoid):
    "Test spherical to geodetic coordinates conversion on equator."
    rtol = 1e-10
    size = 5
    spherical_latitude = np.zeros(size)
    spherical_longitude = np.linspace(0, 180, size)
    radius = np.linspace(-1e4, 1e4, size) + ellipsoid.semimajor_axis
    longitude, latitude, height = ellipsoid.spherical_to_geodetic(
        (spherical_longitude, spherical_latitude, radius)
    )
    npt.assert_allclose(spherical_longitude, longitude, rtol=rtol)
    npt.assert_allclose(spherical_latitude, latitude, rtol=rtol)
    npt.assert_allclose(radius, height + ellipsoid.semimajor_axis, rtol=rtol)


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_spherical_to_geodetic_on_poles(ellipsoid):
    "Test spherical to geodetic coordinates conversion on poles."
    rtol = 1e-10
    size = 5
    spherical_longitude = np.hstack([np.linspace(0, 180, size)] * 2)
    spherical_latitude = np.array([90.0] * size + [-90.0] * size)
    radius = np.hstack([np.linspace(-1e4, 1e4, size) + ellipsoid.semiminor_axis] * 2)
    longitude, latitude, height = ellipsoid.spherical_to_geodetic(
        (spherical_longitude, spherical_latitude, radius)
    )
    npt.assert_allclose(spherical_longitude, longitude, rtol=rtol)
    npt.assert_allclose(spherical_latitude, latitude, rtol=rtol)
    npt.assert_allclose(radius, height + ellipsoid.semiminor_axis, rtol=rtol)


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_geodetic_to_ellipsoidal_conversions(ellipsoid):
    """
    Test the geodetic to ellipsoidal-harmonic coordinate conversions by
    going from geodetic to ellipsoidal and back.
    """
    size = 5
    geodetic_latitude_in = np.linspace(-90, 90, size)
    height_in = np.zeros(size)
    longitude, reduced_latitude, u = ellipsoid.geodetic_to_ellipsoidal_harmonic(
        (None, geodetic_latitude_in, height_in)
    )
    longitude, geodetic_latitude_out, height_out = (
        ellipsoid.ellipsoidal_harmonic_to_geodetic((None, reduced_latitude, u))
    )
    npt.assert_allclose(geodetic_latitude_in, geodetic_latitude_out)
    npt.assert_allclose(height_in, height_out)

    rtol = 1e-5  # The conversion is not too accurate for large heights
    height_in = np.array(size * [1000])
    longitude, reduced_latitude, u = ellipsoid.geodetic_to_ellipsoidal_harmonic(
        (None, geodetic_latitude_in, height_in)
    )
    longitude, geodetic_latitude_out, height_out = (
        ellipsoid.ellipsoidal_harmonic_to_geodetic((None, reduced_latitude, u))
    )
    npt.assert_allclose(geodetic_latitude_in, geodetic_latitude_out, rtol=rtol)
    npt.assert_allclose(height_in, height_out, rtol=rtol)


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_spherical_to_geodetic_identity(ellipsoid):
    "Test if applying both conversions in series is the identity operator"
    rtol = 1e-10
    longitude = np.linspace(0, 350, 36)
    latitude = np.linspace(-90, 90, 19)
    height = np.linspace(-1e4, 1e4, 8)
    coordinates = np.meshgrid(longitude, latitude, height)
    spherical_coordinates = ellipsoid.geodetic_to_spherical(coordinates)
    reconverted_coordinates = ellipsoid.spherical_to_geodetic(spherical_coordinates)
    npt.assert_allclose(coordinates, reconverted_coordinates, rtol=rtol)


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_normal_gravity_pole_equator(ellipsoid):
    "Compare normal gravity values at pole and equator"
    rtol = 1e-10
    height = 0
    # Convert gamma to mGal
    gamma_pole = ellipsoid.gravity_pole * 1e5
    gamma_eq = ellipsoid.gravity_equator * 1e5
    npt.assert_allclose(
        gamma_pole, ellipsoid.normal_gravity((None, -90, height)), rtol=rtol
    )
    npt.assert_allclose(
        gamma_pole, ellipsoid.normal_gravity((None, 90, height)), rtol=rtol
    )
    npt.assert_allclose(
        gamma_eq, ellipsoid.normal_gravity((None, 0, height)), rtol=rtol
    )


@pytest.mark.parametrize("si_units", [False, True], ids=["mGal", "SI"])
@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_normal_gravity_arrays(ellipsoid, si_units):
    "Compare normal gravity passing arrays as arguments instead of floats"
    rtol = 1e-10
    heights = np.zeros(3)
    latitudes = np.array([-90, 90, 0])
    gammas = np.array(
        [ellipsoid.gravity_pole, ellipsoid.gravity_pole, ellipsoid.gravity_equator]
    )
    # Convert gammas to mGal
    if not si_units:
        gammas *= 1e5
    npt.assert_allclose(
        gammas,
        ellipsoid.normal_gravity((None, latitudes, heights), si_units=si_units),
        rtol=rtol,
    )


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_normal_gravity_non_zero_height(ellipsoid):
    "Check consistency of normal gravity above and below the ellipsoid."
    # Convert gamma to mGal
    gamma_pole = ellipsoid.gravity_pole * 1e5
    gamma_eq = ellipsoid.gravity_equator * 1e5
    assert gamma_pole > ellipsoid.normal_gravity((None, 90, 1000))
    assert gamma_pole > ellipsoid.normal_gravity((None, -90, 1000))
    assert gamma_eq > ellipsoid.normal_gravity((None, 0, 1000))
    assert gamma_pole < ellipsoid.normal_gravity((None, 90, -1000))
    assert gamma_pole < ellipsoid.normal_gravity((None, -90, -1000))
    assert gamma_eq < ellipsoid.normal_gravity((None, 0, -1000))


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_prime_vertical_radius(ellipsoid):
    r"""
    Check prime vertical radius on equator, poles and 45 degrees

    The prime vertical radius can be also expressed in terms of the semi-major
    and semi-minor axis:

    .. math:

        N(\phi) = \frac{a^2}{\sqrt{a^2 \cos^2 \phi + b^2 \sin^2 \phi}}

    """
    # Compute prime vertical radius on the equator and the poles
    latitudes = np.array([0, 90, -90, 45])
    prime_vertical_radii = ellipsoid.prime_vertical_radius(
        np.sin(np.radians(latitudes))
    )
    # Computed expected values
    prime_vertical_radius_equator = ellipsoid.semimajor_axis
    prime_vertical_radius_pole = ellipsoid.semimajor_axis**2 / ellipsoid.semiminor_axis
    prime_vertical_radius_45 = ellipsoid.semimajor_axis**2 / np.sqrt(
        0.5 * ellipsoid.semimajor_axis**2 + 0.5 * ellipsoid.semiminor_axis**2
    )
    expected_pvr = np.array(
        [
            prime_vertical_radius_equator,
            prime_vertical_radius_pole,
            prime_vertical_radius_pole,
            prime_vertical_radius_45,
        ]
    )
    # Compare calculated vs expected values
    npt.assert_allclose(prime_vertical_radii, expected_pvr)


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_geocentric_radius(ellipsoid):
    "Check against geocentric coordinate conversion results"
    latitude = np.linspace(-80, 80, 100)
    longitude = np.linspace(-180, 180, latitude.size)
    height = np.zeros(latitude.size)
    radius_conversion = ellipsoid.geodetic_to_spherical((longitude, latitude, height))[
        2
    ]
    npt.assert_allclose(radius_conversion, ellipsoid.geocentric_radius(latitude))


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_geocentric_radius_pole_equator(ellipsoid):
    "Check against values at the pole and equator"
    latitude = np.array([-90, 90, 0])
    radius_true = np.array(
        [ellipsoid.semiminor_axis, ellipsoid.semiminor_axis, ellipsoid.semimajor_axis]
    )
    npt.assert_allclose(radius_true, ellipsoid.geocentric_radius(latitude))


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_geocentric_radius_geocentric(ellipsoid):
    "Check against coordinate conversion results with geocentric latitude"
    latitude = np.linspace(-80, 80, 100)
    longitude = np.linspace(-180, 180, latitude.size)
    height = np.zeros(latitude.size)
    latitude_spherical, radius_conversion = ellipsoid.geodetic_to_spherical(
        (longitude, latitude, height)
    )[1:]
    npt.assert_allclose(
        radius_conversion,
        ellipsoid.geocentric_radius(latitude_spherical, geodetic=False),
    )


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_geocentric_radius_geocentric_pole_equator(ellipsoid):
    "Check against values at the pole and equator with geocentric latitude"
    latitude = np.array([-90, 90, 0])
    radius_true = np.array(
        [ellipsoid.semiminor_axis, ellipsoid.semiminor_axis, ellipsoid.semimajor_axis]
    )
    npt.assert_allclose(
        radius_true, ellipsoid.geocentric_radius(latitude, geodetic=False)
    )


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_normal_gravity_against_somigliana(ellipsoid):
    """
    Check if normal gravity on the surface satisfies Somigliana equation
    """
    latitude = np.linspace(-90, 90, 181)
    # Somigliana equation applies only to ellipsoids that are their own
    # equipotential gravity surface. Spheres (with zero flattening) aren't.
    if ellipsoid.flattening != 0:
        npt.assert_allclose(
            ellipsoid.normal_gravity((None, latitude, 0)),
            normal_gravity_surface(latitude, ellipsoid),
        )


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_normal_gravity_computed_on_internal_point(ellipsoid):
    """
    Check if warn is raised if height is negative for normal_gravity,
    normal_gravity_potential, and normal_gravitational_potential.
    """
    latitude = np.linspace(-90, 90, 100)
    with warnings.catch_warnings(record=True) as warn:
        ellipsoid.normal_gravity((None, latitude, -10))
        assert len(warn) >= 1
    with warnings.catch_warnings(record=True) as warn:
        ellipsoid.normal_gravity_potential((None, latitude, -10))
        assert len(warn) >= 1
    with warnings.catch_warnings(record=True) as warn:
        ellipsoid.normal_gravitational_potential((None, latitude, -10))
        assert len(warn) >= 1


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_normal_gravity_gravitational_centrifugal_potential(ellipsoid):
    """
    Test that the normal gravity potential is equal to the sum of the normal
    gravitational potential and centrifugal potential.
    """
    size = 5
    latitude = np.array([np.linspace(-90, 90, size)] * 2)
    height = np.array([[0] * size, [1000] * size])
    big_u = ellipsoid.normal_gravity_potential((None, latitude, height))
    big_v = ellipsoid.normal_gravitational_potential((None, latitude, height))
    big_phi = ellipsoid.centrifugal_potential((None, latitude, height))
    npt.assert_allclose(big_u, big_v + big_phi)


def test_emm_wgs84():
    "The _emm property should be equal this value for WGS84"
    npt.assert_allclose(WGS84._emm, 0.00344978650684)
