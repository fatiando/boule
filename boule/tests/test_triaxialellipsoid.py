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
