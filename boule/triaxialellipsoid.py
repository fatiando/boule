# Copyright (c) 2019 The Boule Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Module for defining and setting the reference ellipsoid.
"""
from warnings import warn
import attr
import numpy as np


# Don't let ellipsoid parameters be changed to avoid messing up calculations
# accidentally.
@attr.s(frozen=True)
class TriaxialEllipsoid:
    """
    Reference triaxial ellipsoid.

    The ellipsoid is triaxial and spins around it's largest moment of inertia.
    It is defined by five parameters (semi-major axis, semi-medium axis,
    semi-minor axis,  geocentric gravitational constant, and angular velocity)
    and offers other derived quantities.

    **All attributes of this class are read-only and cannot be changed after
    instantiation.**

    All parameters are in SI units.

    .. note::

        Use :class:`boule.Sphere` if you desire zero flattening or
        :class:`boule.Ellipsoid` for oblate ellipsoids. Some calculations would
        not work by setting the axis to the same value.

    .. warning::

        Gravity calculations have not been implemented yet for triaxial
        ellipsoids.

    Parameters
    ----------
    name : str
        A short name for the ellipsoid, for example ``'WGS84'``.
    semimajor_axis : float
        The semi-major axis of the ellipsoid, usually represented by "a"
        [meters].
    semimedium_axis : float
        The semi-medium axis of the ellipsoid, usually represented by "b"
        [meters].
    semimajor_axis : float
        The semi-minor axis of the ellipsoid, usually represented by "c"
        [meters].
    geocentric_grav_const : float
        The geocentric gravitational constant (GM) [m^3 s^-2].
    angular_velocity : float
        The angular velocity of the rotating ellipsoid (omega) [rad s^-1].
    long_name : str or None
        A long name for the ellipsoid, for example ``"World Geodetic System
        1984"`` (optional).
    reference : str or None
        Citation for the ellipsoid parameter values (optional).

    Examples
    --------

    We can define an ellipsoid by setting the 5 key numerical parameters:

    >>> ellipsoid = TriaxialEllipsoid(
    ...     name="Watermelon",
    ...     long_name="Large Watermelon",
    ...     semimajor_axis=4,
    ...     semimedium_axis=2,
    ...     semiminor_axis=1,
    ...     geocentric_grav_const=1,
    ...     angular_velocity=0,
    ... )
    >>> print(ellipsoid) # doctest: +ELLIPSIS
    TriaxialEllipsoid(name='Watermelon', ...)
    >>> print(ellipsoid.long_name)
    Large Watermelon

    The class defines several derived attributes based on the input parameters:

    >>> print("{:.2f}".format(ellipsoid.semimajor_axis))
    4.00
    >>> print("{:.2f}".format(ellipsoid.semimedium_axis))
    2.00
    >>> print("{:.2f}".format(ellipsoid.semiminor_axis))
    1.00
    >>> print("{:.2f}".format(ellipsoid.mean_radius))
    2.33
    >>> print("{:.2f}".format(ellipsoid.volume))
    33.51

    """

    name = attr.ib()
    semimajor_axis = attr.ib()
    semimedium_axis = attr.ib()
    semiminor_axis = attr.ib()
    geocentric_grav_const = attr.ib()
    angular_velocity = attr.ib()
    long_name = attr.ib(default=None)
    reference = attr.ib(default=None)

    def _raise_invalid_axis(self):
        """
        Raise a ValueError informing that the axis are invalid.
        """
        raise ValueError(
            "Invalid triaxial ellipsoid axis: "
            f"major={self.semimajor_axis} "
            f"medium={self.semimedium_axis} "
            f"minor={self.semiminor_axis}. "
            "Must be major > medium > minor."
        )

    @semimajor_axis.validator
    def _check_semimajor_axis(
        self, semimajor_axis, value
    ):  # pylint: disable=no-self-use,unused-argument
        """
        Check if semimajor_axis is positive and is the largest of the radii
        """
        if not value > 0:
            raise ValueError(
                f"Invalid semi-major axis '{value}'. Should be greater than zero."
            )
        if self.semimedium_axis > value:
            self._raise_invalid_axis()

    @semimedium_axis.validator
    def _check_semimedium_axis(
        self, semimedium_axis, value
    ):  # pylint: disable=no-self-use,unused-argument
        """
        Check if semimedium_axis is positive and larger than the semi-minor axis
        """
        if not value > 0:
            raise ValueError(
                f"Invalid semi-medium axis '{value}'. Should be greater than zero."
            )
        # Check if semimedium axis is the middle of the 3 axes.
        if self.semiminor_axis > value:
            self._raise_invalid_axis()

    @semiminor_axis.validator
    def _check_semiminor_axis(
        self, semiminor_axis, value
    ):  # pylint: disable=no-self-use,unused-argument
        """
        Check if semiminor_axis is positive
        """
        if not value > 0:
            raise ValueError(
                f"Invalid semi-minor axis '{value}'. Should be greater than zero."
            )
        # Don't need to check here because if the two checks for major and
        # medium pass it means that this is the smallest.

    @geocentric_grav_const.validator
    def _check_geocentric_grav_const(
        self, geocentric_grav_const, value
    ):  # pylint: disable=no-self-use,unused-argument
        """
        Warn if geocentric_grav_const is negative
        """
        if value < 0:
            warn(f"The geocentric gravitational constant is negative: '{value}'")

    @property
    def mean_radius(self):
        """
        The arithmetic mean radius :math:`R=(a+b+c)/3` [meters]
        """
        return (
            1 / 3 * (self.semimajor_axis + self.semimedium_axis + self.semiminor_axis)
        )

    @property
    def volume(self):
        """
        The volume of a triaxial ellipsoid :math: `V = /frac{4}{3} pi a b c ` [meters^3]
        """
        return (
            (4 / 3 * np.pi)
            * self.semimajor_axis
            * self.semimedium_axis
            * self.semiminor_axis
        )
