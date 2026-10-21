# Copyright (c) 2019 The Boule Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Test the HomogeneousEllipsoid class.
"""

import numpy as np
import numpy.testing as npt
import pytest

from boule import Callisto2024, Charon2024, HomogeneousEllipsoid, Moon2015, Pluto2024


@pytest.mark.parametrize(
    "sphere",
    [Moon2015, Callisto2024, Pluto2024, Charon2024],
)
@pytest.mark.parametrize("si_units", [True, False])
@pytest.mark.parametrize("longitude", [None, 0, 123])
def test_homogeneous_ellipsoid_vs_sphere_gravitation(sphere, si_units, longitude):
    "Check calculations against a sphere model"
    ellipsoid = HomogeneousEllipsoid(
        name="test",
        semimajor_axis=sphere.radius,
        flattening=1e-10,
        density=sphere.mass / sphere.volume,
        angular_velocity=sphere.angular_velocity,
    )
    npt.assert_allclose(sphere.mass, ellipsoid.mass)
    coordinates = (longitude, np.linspace(-90, 90, 181), np.linspace(0, 1000e3, 181))
    npt.assert_allclose(
        sphere.normal_gravitation(coordinates, si_units=si_units),
        ellipsoid.normal_gravitation(coordinates, si_units=si_units),
        rtol=1e-4,
    )


@pytest.mark.parametrize(
    "sphere",
    [Moon2015, Callisto2024, Pluto2024, Charon2024],
)
@pytest.mark.parametrize("si_units", [True, False])
@pytest.mark.parametrize("longitude", [None, 0, 123])
def test_homogeneous_ellipsoid_vs_sphere_gravity(sphere, si_units, longitude):
    "Check calculations against a sphere model"
    ellipsoid = HomogeneousEllipsoid(
        name="test",
        semimajor_axis=sphere.radius,
        flattening=1e-10,
        density=sphere.mass / sphere.volume,
        angular_velocity=sphere.angular_velocity,
    )
    npt.assert_allclose(sphere.mass, ellipsoid.mass)
    coordinates = (longitude, np.linspace(-90, 90, 181), np.linspace(0, 1000e3, 181))
    npt.assert_allclose(
        sphere.normal_gravity(coordinates, si_units=si_units),
        ellipsoid.normal_gravity(coordinates, si_units=si_units),
        rtol=1e-4,
    )


def test_homogeneous_ellipsoid_str():
    "Make sure the str repr is corrent when some things are missing"
    ellipsoid = HomogeneousEllipsoid(
        name="bla",
        long_name="blabla",
        semimajor_axis=1,
        flattening=0.5,
        density=1,
        angular_velocity=2,
    )
    assert str(ellipsoid) == (
        "bla - blabla\n"
        "Homogeneous oblate ellipsoid:\n"
        "  • Semimajor axis: 1 m\n"
        "  • Flattening: 0.5\n"
        "  • Density: 1 kg/m³\n"
        "  • Angular velocity: 2 rad/s"
    )
    ellipsoid = HomogeneousEllipsoid(
        name="bla",
        long_name="blabla",
        semimajor_axis=1,
        flattening=0.5,
        density=1,
        angular_velocity=2,
        reference="Someone smart",
        comments="A great ellipsoid",
    )
    assert str(ellipsoid) == (
        "bla - blabla\n"
        "Homogeneous oblate ellipsoid:\n"
        "  • Semimajor axis: 1 m\n"
        "  • Flattening: 0.5\n"
        "  • Density: 1 kg/m³\n"
        "  • Angular velocity: 2 rad/s\n"
        "Source:\n"
        "  Someone smart\n"
        "Comments:\n"
        "  A great ellipsoid"
    )
