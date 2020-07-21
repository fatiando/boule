"""
Test the base Sphere class.
"""
import numpy as np
import numpy.testing as npt

from .. import Sphere


def test_sphere_flattening():
    """
    Check if flattening property is equal to zero
    """
    sphere = Sphere(
        name="sphere", radius=1, geocentric_grav_const=1, angular_velocity=0
    )
    assert sphere.flattening == 0


def test_normal_gravity_no_rotation():
    """
    Check normal gravity without rotation
    """
    gm = 3
    radius = 1
    sphere = Sphere(
        name="sphere", radius=radius, geocentric_grav_const=gm, angular_velocity=0
    )
    # Create a set of points a different latitudes and same height
    for h in [1, 2, 3, 4]:
        latitude = np.linspace(-90, 90, 19)
        height = h * np.ones_like(latitude)
        # Check if normal gravity is equal on every point (rotational symmetry)
        expected_gravity = gm / (radius + h) ** 2
        npt.assert_allclose(expected_gravity, sphere.normal_gravity(latitude, height))


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
        expected_value = -(omega ** 2) * (radius + height)
        npt.assert_allclose(
            expected_value, sphere.normal_gravity(latitude=0, height=height),
        )
    # Check normal gravity on the poles (must be equal to zero)
    for height in [1, 2, 3, 4]:
        assert sphere.normal_gravity(latitude=90, height=height) < 1e-15
        assert sphere.normal_gravity(latitude=-90, height=height) < 1e-15
    # Check normal gravity at 45 degrees latitude
    for height in [1, 2, 3, 4]:
        expected_value = -(omega ** 2) * (radius + height) * np.sqrt(2) / 2
        npt.assert_allclose(
            expected_value, sphere.normal_gravity(latitude=45, height=height),
        )
