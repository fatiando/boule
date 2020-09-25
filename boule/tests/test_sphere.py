# pylint: disable=redefined-outer-name
"""
Test the base Sphere class.
"""
import pytest
import numpy as np
import numpy.testing as npt

from .. import Sphere


@pytest.fixture
def sphere():
    "A spherical ellipsoid"
    ellipsoid = Sphere(
        name="unit_sphere", radius=1.0, geocentric_grav_const=2.0, angular_velocity=1.3,
    )
    return ellipsoid


def test_sphere_flattening(sphere):
    """
    Check if flattening property is equal to zero
    """
    assert sphere.flattening == 0


def test_sphere_semimajor_axis(sphere):
    """
    Check if semimajor_axis is equal to the radius
    """
    npt.assert_allclose(sphere.semimajor_axis, sphere.radius)


def test_geodetic_to_spherical(sphere):
    "Test geodetic to geocentric conversion on spherical ellipsoid."
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
    npt.assert_allclose(radius, sphere.radius + height, rtol=rtol)


def test_spherical_to_geodetic(sphere):
    "Test spherical to geodetic conversion on spherical ellipsoid."
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
    npt.assert_allclose(radius, sphere.radius + height, rtol=rtol)


def test_ellipsoidal_properties(sphere):
    """
    Check inherited properties from Ellipsoid
    """
    npt.assert_allclose(sphere.semiminor_axis, sphere.radius)
    npt.assert_allclose(sphere.linear_eccentricity, 0)
    npt.assert_allclose(sphere.first_eccentricity, 0)
    npt.assert_allclose(sphere.second_eccentricity, 0)
    npt.assert_allclose(sphere.mean_radius, sphere.radius)
    npt.assert_allclose(
        sphere.emm,
        sphere.angular_velocity ** 2
        * sphere.radius ** 3
        / sphere.geocentric_grav_const,
    )


def test_prime_vertical_radius(sphere):
    """
    Check prime vertical radius
    """
    latitudes = np.linspace(-90, 90, 18)
    npt.assert_allclose(
        sphere.prime_vertical_radius(np.sin(np.radians(latitudes))), sphere.radius
    )


def test_geocentric_radius(sphere):
    """
    Check geocentric radius
    """
    latitudes = np.linspace(-90, 90, 18)
    for geodetic in (True, False):
        npt.assert_allclose(
            sphere.geocentric_radius(latitudes, geodetic=geodetic), sphere.radius
        )


def test_normal_gravity_pole_equator(sphere):
    """
    Compare normal gravity values at pole and equator
    """
    rtol = 1e-10
    height = 0
    # Convert gamma to mGal
    gamma_pole = sphere.gravity_pole * 1e5
    gamma_eq = sphere.gravity_equator * 1e5
    npt.assert_allclose(gamma_pole, sphere.normal_gravity(-90, height), rtol=rtol)
    npt.assert_allclose(gamma_pole, sphere.normal_gravity(90, height), rtol=rtol)
    npt.assert_allclose(gamma_eq, sphere.normal_gravity(0, height), rtol=rtol)


def test_normal_gravity_no_rotation():
    """
    Check normal gravity without rotation
    """
    gm_constant = 3
    radius = 1
    sphere = Sphere(
        name="sphere",
        radius=radius,
        geocentric_grav_const=gm_constant,
        angular_velocity=0,
    )
    # Create a set of points a different latitudes and same height
    for height in [1, 2, 3, 4]:
        latitudes = np.linspace(-90, 90, 19)
        heights = height * np.ones_like(latitudes)
        # Check if normal gravity is equal on every point (rotational symmetry)
        expected_gravity = 1e5 * gm_constant / (radius + height) ** 2
        npt.assert_allclose(expected_gravity, sphere.normal_gravity(latitudes, heights))


def test_normal_gravity_only_rotation():
    """
    Check normal gravity only with rotation (no gravitational attraction)
    """
    radius = 1
    omega = 2
    sphere = Sphere(
        name="sphere", radius=radius, geocentric_grav_const=0, angular_velocity=omega
    )
    # Check normal gravity on the equator
    for height in [1, 2, 3, 4]:
        expected_value = 1e5 * (omega ** 2) * (radius + height)
        npt.assert_allclose(
            expected_value, sphere.normal_gravity(latitude=0, height=height),
        )
    # Check normal gravity on the poles (must be equal to zero)
    for height in [1, 2, 3, 4]:
        assert sphere.normal_gravity(latitude=90, height=height) < 1e-15
        assert sphere.normal_gravity(latitude=-90, height=height) < 1e-15
    # Check normal gravity at 45 degrees latitude
    for height in [1, 2, 3, 4]:
        expected_value = 1e5 * (omega ** 2) * (radius + height) * np.sqrt(2) / 2
        npt.assert_allclose(
            expected_value, sphere.normal_gravity(latitude=45, height=height),
        )
