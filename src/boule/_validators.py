# Copyright (c) 2019 The Boule Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Attrs validator functions for ellipsoid parameters.
"""

from warnings import warn


def validate_flattening(instance, attribute, value):  # noqa: ARG001
    """
    Check if flattening is valid.
    """
    if value < 0 or value >= 1:
        message = (
            f"Invalid flattening '{value}'. "
            "Should be greater than zero and lower than 1."
        )
        raise ValueError(message)
    if value == 0:
        message = (
            "Flattening equal to zero will lead to errors in normal gravity. "
            "Use boule.Sphere for representing ellipsoids with zero flattening."
        )
        raise ValueError(message)
    if value < 1e-7:
        message = (
            f"Flattening is too close to zero ('{value}'). "
            "This may lead to inaccurate results and division by zero errors. "
            "Use boule.Sphere for representing ellipsoids with zero flattening."
        )
        warn(message, stacklevel=2)


def validate_semiaxis(instance, attribute, value):
    """
    Check if the 3 semiaxis are > 0 and in the right order.
    """
    if not value > 0:
        message = f"Invalid {attribute} = '{value}'. Should be greater than zero."
        raise ValueError(message)
    if (
        not instance.semimajor_axis
        >= instance.semimedium_axis
        >= instance.semiminor_axis
    ):
        message = (
            "Invalid triaxial ellipsoid axis: "
            f"major={instance.semimajor_axis} "
            f"medium={instance.semimedium_axis} "
            f"minor={instance.semiminor_axis}. "
            "Must be major > medium > minor."
        )
        raise ValueError(message)


def warn_negative(instance, attribute, value):  # noqa: ARG001
    """
    Warn if the given attribute is negative.
    """
    if value < 0:
        message = f"Attribute {attribute} is negative: '{value}'"
        warn(message, stacklevel=2)


def check_coordinate_system(
    coordinate_system,
    *,
    valid=("geodetic", "spherical", "cartesian", "ellipsoidal harmonic"),
):
    """
    Make sure the coordinate system is valid.

    Parameters
    ----------
    coordinate_system : str
        A string specifying the coordinate system to use.
    valid : list of str
        List of valid values for the coordinate system.

    Raises
    ------
    ValueError
        If the coordinate system is not in the valid list.
    """
    if coordinate_system not in valid:
        message = (
            f"Invalid coordinate system '{coordinate_system}'. Must be one of {valid}."
        )
        raise ValueError(message)
