"""
Test the base Ellipsoid class.
"""
import pytest
import numpy as np
import numpy.testing as npt

from .. import Ellipsoid, WGS84


@pytest.fixture
def sphere():
    "A spherical ellipsoid"
    ellipsoid = Ellipsoid(
        name="unit_sphere",
        semimajor_axis=1.0,
        flattening=0,
        geocentric_grav_const=0,
        angular_velocity=0,
    )
    return ellipsoid


def test_geodetic_to_spherical_with_spherical_ellipsoid(sphere):
    "Test geodetic to geocentric conversion if ellipsoid is a sphere."
    rtol = 1e-10
    size = 5
    longitude = np.linspace(0, 180, size)
    latitude = np.linspace(-90, 90, size)
    height = np.linspace(-0.2, 0.2, size)
    sph_longitude, sph_latitude, radius = sphere.geodetic_to_spherical(
        longitude, latitude, height
    )
    npt.assert_allclose(sph_longitude, longitude, rtol=rtol)
    npt.assert_allclose(sph_latitude, latitude, rtol=rtol)
    npt.assert_allclose(radius, sphere.mean_radius + height, rtol=rtol)


def test_spherical_to_geodetic_with_spherical_ellipsoid(sphere):
    "Test spherical to geodetic conversion if ellipsoid is a sphere."
    rtol = 1e-10
    size = 5
    spherical_longitude = np.linspace(0, 180, size)
    spherical_latitude = np.linspace(-90, 90, size)
    radius = np.linspace(0.8, 1.2, size)
    longitude, latitude, height = sphere.spherical_to_geodetic(
        spherical_longitude, spherical_latitude, radius
    )
    npt.assert_allclose(spherical_longitude, longitude, rtol=rtol)
    npt.assert_allclose(spherical_latitude, latitude, rtol=rtol)
    npt.assert_allclose(radius, sphere.mean_radius + height, rtol=rtol)


def test_geodetic_to_spherical_on_equator():
    "Test geodetic to geocentric coordinates conversion on equator."
    rtol = 1e-10
    size = 5
    longitude = np.linspace(0, 180, size)
    height = np.linspace(-1e4, 1e4, size)
    latitude = np.zeros_like(size)
    ellipsoid = WGS84()
    sph_longitude, sph_latitude, radius = ellipsoid.geodetic_to_spherical(
        longitude, latitude, height
    )
    npt.assert_allclose(sph_longitude, longitude, rtol=rtol)
    npt.assert_allclose(sph_latitude, latitude, rtol=rtol)
    npt.assert_allclose(radius, height + ellipsoid.semimajor_axis, rtol=rtol)


def test_geodetic_to_spherical_on_poles():
    "Test geodetic to geocentric coordinates conversion on poles."
    rtol = 1e-10
    size = 5
    longitude = np.hstack([np.linspace(0, 180, size)] * 2)
    height = np.hstack([np.linspace(-1e4, 1e4, size)] * 2)
    latitude = np.array([90.0] * size + [-90.0] * size)
    ellipsoid = WGS84()
    sph_longitude, sph_latitude, radius = ellipsoid.geodetic_to_spherical(
        longitude, latitude, height
    )
    npt.assert_allclose(sph_longitude, longitude, rtol=rtol)
    npt.assert_allclose(sph_latitude, latitude, rtol=rtol)
    npt.assert_allclose(radius, height + ellipsoid.semiminor_axis, rtol=rtol)


def test_spherical_to_geodetic_on_equator():
    "Test spherical to geodetic coordinates conversion on equator."
    rtol = 1e-10
    size = 5
    spherical_latitude = np.zeros(size)
    ellipsoid = WGS84()
    spherical_longitude = np.linspace(0, 180, size)
    radius = np.linspace(-1e4, 1e4, size) + ellipsoid.semimajor_axis
    longitude, latitude, height = ellipsoid.spherical_to_geodetic(
        spherical_longitude, spherical_latitude, radius
    )
    npt.assert_allclose(spherical_longitude, longitude, rtol=rtol)
    npt.assert_allclose(spherical_latitude, latitude, rtol=rtol)
    npt.assert_allclose(radius, height + ellipsoid.semimajor_axis, rtol=rtol)


def test_spherical_to_geodetic_on_poles():
    "Test spherical to geodetic coordinates conversion on poles."
    rtol = 1e-10
    size = 5
    spherical_longitude = np.hstack([np.linspace(0, 180, size)] * 2)
    spherical_latitude = np.array([90.0] * size + [-90.0] * size)
    ellipsoid = WGS84()
    radius = np.hstack([np.linspace(-1e4, 1e4, size) + ellipsoid.semiminor_axis] * 2)
    longitude, latitude, height = ellipsoid.spherical_to_geodetic(
        spherical_longitude, spherical_latitude, radius
    )
    npt.assert_allclose(spherical_longitude, longitude, rtol=rtol)
    npt.assert_allclose(spherical_latitude, latitude, rtol=rtol)
    npt.assert_allclose(radius, height + ellipsoid.semiminor_axis, rtol=rtol)


def test_spherical_to_geodetic_identity():
    "Test if applying both conversions in series is the identity operator"
    rtol = 1e-10
    longitude = np.linspace(0, 350, 36)
    latitude = np.linspace(-90, 90, 19)
    height = np.linspace(-1e4, 1e4, 8)
    coordinates = np.meshgrid(longitude, latitude, height)
    ellipsoid = WGS84()
    spherical_coordinates = ellipsoid.geodetic_to_spherical(*coordinates)
    reconverted_coordinates = ellipsoid.spherical_to_geodetic(*spherical_coordinates)
    npt.assert_allclose(coordinates, reconverted_coordinates, rtol=rtol)
