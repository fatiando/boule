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

    The ellipsoid is triaxial and spins around it's largest moment of inertia. It is defined by
    five parameters (semi-major axis, semi-medium axis, semi-minor axis,  geocentric gravitational
    constant, and angular velocity) and offers other derived quantities.

    **All attributes of this class are read-only and cannot be changed after
    instantiation.**

    All parameters are in SI units.

    .. note::

        Use :class:`boule.Sphere` if you desire zero flattening because there
        are singularities for this particular case in the normal gravity
        calculations.

        Use :class:`boule.Ellipsoid` if you wish to implement an oblate spheroid

    Parameters
    ----------
    name : str
        A short name for the ellipsoid, for example ``'WGS84'``.
    semimajor_axis : float
        The semi-major axis of the ellipsoid (equatorial radius), usually
        represented by "a" [meters].
    semimedium_axis : float
        The semi-medium axis of the ellipsoid (equatorial radius), usually
        represented by "b" [meters].
    semimajor_axis : float
        The semi-minor axis of the ellipsoid (equatorial radius), usually
        represented by "c" [meters].
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

    @semimajor_axis.validator
    def _check_semimajor_axis(
        self, semimajor_axis, value
    ):  # pylint: disable=no-self-use,unused-argument
        """
        Check if semimajor_axis is positive
        """
        if not value > 0:
            raise ValueError(
                f"Invalid semi-major axis '{value}'. Should be greater than zero."
            )
        """
        Check if semimajor axis is the largest of the 3 axes.
        """
        if self.semiminor_axis > value:
            raise ValueError(
                f"Invalid semi-minor / semi-major axis combination. The semimajor axis must be larger than the semi-medium axis.                 Semi-major axis was '{value}' and the semi-minor axis was '{self.semiminor_axis}'"
            )
        if self.semimedium_axis > value:
            raise ValueError(
                f"Invalid semi-medium / semi-major axis combination. The semimajor axis must be larger than the semi-medium axis. Semi-major axis was '{value}' and the semi-medium axis was '{self.semimedium_axis}'"
            )

    @semimedium_axis.validator
    def _check_semimedium_axis(
        self, semimedium_axis, value
    ):  # pylint: disable=no-self-use,unused-argument
        """
        Check if semimedium_axis is positive
        """
        if not value > 0:
            raise ValueError(
                f"Invalid semi-medium axis '{value}'. Should be greater than zero."
            )
        """
        Check if semimedium axis is the middle of the 3 axes.
        """
        if self.semiminor_axis > value:
            raise ValueError(
                f"Invalid semi-minor / semi-medium axis combination. The semimedium axis must be larger than the semi-minor axis.                 Semi-medium axis was '{value}' and the semi-minor axis was '{self.semiminor_axis}'"
            )

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
    def a(self):
        "The semimajor axis length [meters]"
        return self.semimajor_axis

    @property
    def b(self):
        "The semimedium axis length [meters]"
        return self.semimedium_axis

    @property
    def c(self):
        "The semiminor axis length [meters]"
        return self.semiminor_axis

    @property
    def omega(self):
        "The angular_velocity [rad s^-1]"
        return self.angular_velocity

    @property
    def GM(self):
        "The Geocentric Gravitational Constant [m^3 s^-2]"
        return self.geocentric_grav_const

    @property
    def mean_radius(self):
        """
        The arithmetic mean radius :math:`R_1=(a+b+c)/3` [meters]
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
            4
            * np.pi
            / 3
            * (self.semimajor_axis * self.semimedium_axis * self.semiminor_axis)
        )

    @property
    def gravity_pole(self):
        "The norm of the gravity vector on the ellipsoid at the poles [m/s²]"
        raise NotImplementedError



    def geocentric_radius(self, latitude, geodetic=True):
        r"""
        Distance from the center of the ellipsoid to its surface.
        """
        raise NotImplementedError

    def prime_vertical_radius(self, sinlat):
        r"""
        Calculate the prime vertical radius for a given geodetic latitude
        """
        raise NotImplementedError

    def geodetic_to_spherical(self, longitude, latitude, height):
        """
        Convert from geodetic to geocentric spherical coordinates.
        """
        raise NotImplementedError

    def spherical_to_geodetic(self, longitude, spherical_latitude, radius):
        """
        Convert from geocentric spherical to geodetic coordinates.
        """
        raise NotImplementedError

    def normal_gravity(self, latitude, height):
        """
        Calculate normal gravity at any latitude and height.
        """
        raise NotImplementedError
