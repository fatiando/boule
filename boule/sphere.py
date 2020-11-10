# Copyright (c) 2019 The Boule Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Define the reference sphere (ellipsoid with 0 flattening).
"""
from warnings import warn

import attr
import numpy as np

from .ellipsoid import Ellipsoid


# Don't let ellipsoid parameters be changed to avoid messing up calculations
# accidentally.
@attr.s(frozen=True)
class Sphere(Ellipsoid):
    """
    Reference sphere (zero flattening ellipsoids)

    Represents a rotating reference ellipsoid with zero flattening. It is
    defined by three parameters (radius, geocentric gravitational constant, and
    angular velocity) and offers other derived quantities.

    **All attributes of this class are read-only and cannot be changed after
    instantiation.**

    All parameters are in SI units.

    .. note::

        Must be used instead of :class:`boule.Ellipsoid` to account for
        singularities due to zero flattening (and thus zero eccentricity) in
        normal gravity calculations.

    Parameters
    ----------
    name : str
        A short name for the sphere, for example ``'Moon'``.
    radius : float
        The radius of the sphere [meters].
    geocentric_grav_const : float
        The geocentric gravitational constant (GM) [m^3 s^-2].
    angular_velocity : float
        The angular velocity of the rotating sphere (omega) [rad s^-1].
    long_name : str or None
        A long name for the sphere, for example ``"Moon Reference System"``
        (optional).
    reference : str or None
        Citation for the sphere parameter values (optional).

    Examples
    --------

    We can define a sphere by specifying the 3 key numerical parameters:

    >>> sphere = Sphere(
    ...     name="Moon",
    ...     long_name="That's no moon",
    ...     radius=1,
    ...     geocentric_grav_const=2,
    ...     angular_velocity=0.5,
    ... )
    >>> print(sphere) # doctest: +ELLIPSIS
    Sphere(name='Moon', ...)
    >>> print(sphere.long_name)
    That's no moon

    The class defines several derived attributes based on the input parameters:

    >>> print("{:.2f}".format(sphere.semimajor_axis))
    1.00
    >>> print("{:.2f}".format(sphere.semiminor_axis))
    1.00
    >>> print("{:.2f}".format(sphere.mean_radius))
    1.00
    >>> print("{:.2f}".format(sphere.gravity_equator))
    1.75
    >>> print("{:.2f}".format(sphere.gravity_pole))
    2.00

    Normal gravity (the magnitude of the gravity potential) can be calculated
    at any latitude and height. **Note that this method returns values in mGal
    instead of m/s².**

    >>> print("{:.2f}".format(sphere.normal_gravity(latitude=0, height=0)))
    175000.00
    >>> print("{:.2f}".format(sphere.normal_gravity(latitude=90, height=0)))
    200000.00

    The flag si_units will return the Normal gravity in m/s².

    >>> print("{:.2f}".format(sphere.normal_gravity(latitude=0, height=0, si_units=True)))
    1.75
    >>> print("{:.2f}".format(sphere.normal_gravity(latitude=90, height=0, si_units=True)))
    2.00

    The flattening and eccentricities will all be zero:

    >>> print("{:.2f}".format(sphere.flattening))
    0.00
    >>> print("{:.2f}".format(sphere.linear_eccentricity))
    0.00
    >>> print("{:.2f}".format(sphere.first_eccentricity))
    0.00
    >>> print("{:.2f}".format(sphere.second_eccentricity))
    0.00

    """

    name = attr.ib()
    radius = attr.ib()
    geocentric_grav_const = attr.ib()
    angular_velocity = attr.ib()
    long_name = attr.ib(default=None)
    reference = attr.ib(default=None)
    # semimajor_axis and flattening shouldn't be defined on initialization:
    #   - semimajor_axis will be equal to radius
    #   - flattening will be equal to zero
    semimajor_axis = attr.ib(init=False, repr=False)
    flattening = attr.ib(init=False, default=0, repr=False)

    @semimajor_axis.default
    def _set_semimajor_axis(self):
        "The semimajor axis should be the radius"
        return self.radius

    @radius.validator
    def _check_radius(
        self, radius, value
    ):  # pylint: disable=no-self-use,unused-argument
        """
        Check if the radius is positive
        """
        if not value > 0:
            raise ValueError(f"Invalid radius '{value}'. Should be greater than zero.")

    @geocentric_grav_const.validator
    def _check_geocentric_grav_const(
        self, geocentric_grav_const, value
    ):  # pylint: disable=no-self-use,unused-argument
        """
        Warn if geocentric_grav_const is negative
        """
        if value < 0:
            warn(f"The geocentric gravitational constant is negative: '{value}'")

    def normal_gravity(self, latitude, height, si_units=False):
        r"""
        Calculate normal gravity at any latitude and height

        Computes the magnitude of the gradient of the gravity potential
        (gravitational + centrifugal; see [Heiskanen-Moritz]_) generated by the
        sphere at the given latitude :math:`\theta` and height :math:`h`:

        .. math::

            \gamma(\theta, h) =
            \sqrt{\left( \frac{GM}{(R + h)^2} \right)^2
            + \left(\omega^2 (R + h) - 2\frac{GM}{(R + h)^2} \right)
            \omega^2 (R + h) \cos^2 \theta}

        in which :math:`R` is the sphere radius, :math:`G` is the gravitational
        constant, :math:`M` is the mass of the sphere, and :math:`\omega` is
        the angular velocity.

        .. note::

            A sphere under rotation is not in hydrostatic equilibrium.
            Therefore, it is not it's own equipotential gravity surface (as is
            the case for the ellipsoid) and the normal gravity vector is not
            normal to the surface of the sphere.

        Parameters
        ----------
        latitude : float or array
            The latitude where the normal gravity will be computed (in
            degrees). For a reference sphere there is no difference between
            geodetic and spherical latitudes.
        height : float or array
            The height (above the surface of the sphere) of the computation
            point (in meters).
        si_units : bool
            Return the value in mGal (False, default) or SI units (True)

        Returns
        -------
        gamma : float or array
            The normal gravity in mGal.

        """
        radial_distance = self.radius + height
        gravity_acceleration = self.geocentric_grav_const / (radial_distance) ** 2
        gamma = np.sqrt(
            gravity_acceleration ** 2
            + (self.angular_velocity ** 2 * radial_distance - 2 * gravity_acceleration)
            * self.angular_velocity ** 2
            * radial_distance
            # replace cos^2 with (1 - sin^2) for more accurate results on the pole
            * (1 - np.sin(np.radians(latitude)) ** 2)
        )
        if si_units:
            return gamma
        # Convert gamma from SI to mGal
        return gamma * 1e5

    @property
    def gravity_equator(self):
        """
        The norm of the gravity vector at the equator on the sphere [m/s²]

        Overrides the inherited method from :class:`boule.Ellipsoid` to avoid
        singularities due to zero flattening.
        """
        return (
            self.geocentric_grav_const / self.radius ** 2
            - self.radius * self.angular_velocity ** 2
        )

    @property
    def gravity_pole(self):
        """
        The norm of the gravity vector at the poles on the sphere [m/s²]

        Overrides the inherited method from :class:`boule.Ellipsoid` to avoid
        singularities due to zero flattening.
        """
        return self.geocentric_grav_const / self.radius ** 2
