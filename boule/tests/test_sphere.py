# Copyright (c) 2019 The Boule Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Test the base Sphere class.
"""
import warnings

import numpy as np
import numpy.testing as npt
import pytest

from .. import Sphere


@pytest.fixture
def sphere():
    "A spherical ellipsoid"
    ellipsoid = Sphere(
        name="unit_sphere",
        radius=1.0,
        geocentric_grav_const=2.0,
        angular_velocity=1.3,
    )
    return ellipsoid


def test_check_radius():
    """
    Check if error is raised after invalid radius
    """
    with pytest.raises(ValueError):
        Sphere(
            name="zero_radius",
            radius=0,
            geocentric_grav_const=0,
            angular_velocity=0,
        )
    with pytest.raises(ValueError):
        Sphere(
            name="negative_radius",
            radius=-1,
            geocentric_grav_const=0,
            angular_velocity=0,
        )


def test_normal_gravity_computed_on_internal_point(sphere):
    """
    Check if warn is raised if height is negative
    """
    latitude = np.linspace(-90, 90, 100)
    with pytest.warns(UserWarning) as warn:
        sphere.normal_gravity(latitude, height=-10)
        assert len(warn) >= 1


def test_check_geocentric_grav_const():
    """
    Check if warn is raised after negative geocentric_grav_const
    """
    with warnings.catch_warnings(record=True) as warn:
        Sphere(
            name="negative_gm",
            radius=1,
            geocentric_grav_const=-1,
            angular_velocity=0,
        )
        assert len(warn) >= 1


@pytest.mark.parametrize("si_units", [False, True], ids=["mGal", "SI"])
def test_normal_gravity_pole_equator(sphere, si_units):
    """
    Compare normal gravity values at pole and equator
    """
    rtol = 1e-10
    height = 0
    gamma_pole = sphere.normal_gravity(90, height, si_units=si_units)
    gamma_eq = sphere.normal_gravity(0, height, si_units=si_units)
    gravitation_pole = sphere.normal_gravitation(height, si_units=si_units)
    centrifugal = sphere.angular_velocity**2 * (sphere.radius + height)
    if not si_units:
        centrifugal *= 1e5
    npt.assert_allclose(gamma_pole, gravitation_pole, rtol=rtol)
    npt.assert_allclose(
        gamma_eq,
        gravitation_pole - centrifugal,
        rtol=rtol,
    )


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
    heights = [1, 100, 1000]
    sphere = Sphere(
        name="sphere", radius=radius, geocentric_grav_const=0, angular_velocity=omega
    )
    # Check normal gravity on the equator
    # Expected value is positive because normal gravity is the norm of the
    # vector.
    for height in heights:
        expected_value = 1e5 * (omega**2) * (radius + height)
        npt.assert_allclose(
            expected_value,
            sphere.normal_gravity(latitude=0, height=height),
        )
    # Check normal gravity on the poles (must be equal to zero)
    for height in heights:
        assert sphere.normal_gravity(latitude=90, height=height) < 1e-15
        assert sphere.normal_gravity(latitude=-90, height=height) < 1e-15
    # Check normal gravity at 45 degrees latitude
    # Expected value is positive because normal gravity is the norm of the
    # vector.
    for height in heights:
        expected_value = 1e5 * (omega**2) * (radius + height) * np.sqrt(2) / 2
        npt.assert_allclose(
            expected_value,
            sphere.normal_gravity(latitude=45, height=height),
        )
