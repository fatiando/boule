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


# Don't let ellipsoid parameters be changed to avoid messing up calculations
# accidentally.
@attr.s(frozen=True)
class Sphere:
    r"""
    A rotating sphere (zero-flattening ellipsoid).

    The ellipsoid is defined by three parameters: radius, geocentric
    gravitational constant, and angular velocity. The internal density
    structure can be either homogeneous or vary radially (e.g. in homogeneous
    concentric spherical shells). The gravity potential of the sphere is not
    constant on its surface because of the latitude-dependent centrifugal
    potential.

    **This class is read-only:** Input parameters and attributes cannot be
    changed after instantiation.

    **Units:** All input parameters and derived attributes are in SI units.

    Parameters
    ----------
    name : str
        A short name for the sphere, for example ``"Moon"``.
    radius : float
        The radius of the sphere.
        Definition: :math:`R`.
        Units: :math:`m`.
    geocentric_grav_const : float
        The geocentric gravitational constant. The product of the mass of the
        sphere :math:`M` and the gravitational constant :math:`G`.
        Definition: :math:`GM`. Units:
        :math:`m^3.s^{-2}`.
    angular_velocity : float
        The angular velocity of the rotating sphere.
        Definition: :math:`\omega`.
        Units: :math:`\\rad.s^{-1}`.
    long_name : str or None
        A long name for the sphere, for example ``"Moon Reference System"``
        (optional).
    reference : str or None
        Citation for the sphere parameter values (optional).


    .. caution::

        Must be used instead of :class:`boule.Ellipsoid` with zero flattening
        for gravity calculations because it is impossible for a rotating sphere
        to have constant gravity (gravitational + centrifugal) potential on its
        surface. So the underlying ellipsoid gravity calculations don't apply
        and are in fact singular when the flattening is zero.

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

    The sphere defines semi-axis, flattening, and some eccentricities similar
    to :class:`~bould.Ellipsoid` for compatibility with the coordinate
    conversion functions of pymap3d:

    >>> print(sphere.semiminor_axis)
    1
    >>> print(sphere.semimajor_axis)
    1
    >>> print(sphere.first_eccentricity)
    0
    >>> print(sphere.eccentricity)
    0
    >>> print(sphere.flattening)
    0
    >>> print(sphere.thirdflattening)
    0

    """

    name = attr.ib()
    radius = attr.ib()
    geocentric_grav_const = attr.ib()
    angular_velocity = attr.ib()
    long_name = attr.ib(default=None)
    reference = attr.ib(default=None)

    @radius.validator
    def _check_radius(self, radius, value):
        "Check if the radius is positive."
        if not value > 0:
            raise ValueError(f"Invalid radius '{value}'. Should be greater than zero.")

    @geocentric_grav_const.validator
    def _check_geocentric_grav_const(self, geocentric_grav_const, value):
        "Warn if geocentric_grav_const is negative."
        if value < 0:
            warn(f"The geocentric gravitational constant is negative: '{value}'")

    @property
    def semiminor_axis(self):
        """
        The semiminor axis of the sphere is equal to its radius. Added for
        compatibility with pymap3d.
        Definition: :math:`b = R`.
        Units: :math:`m`.
        """
        return self.radius

    @property
    def semimajor_axis(self):
        """
        The semimajor axis of the sphere is equal to its radius. Added for
        compatibility with pymap3d.
        Definition: :math:`a = R`.
        Units: :math:`m`.
        """
        return self.radius

    @property
    def flattening(self):
        r"""
        The flattening of the sphere is equal to zero. Added for compatibility
        with pymap3d.
        Definition: :math:`f = \dfrac{a - b}{a}`.
        Units: adimensional.
        """
        return 0

    @property
    def thirdflattening(self):
        r"""
        The third flattening of the sphere is equal to zero. Added for
        compatibility with pymap3d
        Definition: :math:`f^{\prime\prime}= \dfrac{a -b}{a + b}`.
        Units: adimensional.
        """
        return 0

    @property
    def eccentricity(self):
        "Alias for the first eccentricity."
        return self.first_eccentricity

    @property
    def first_eccentricity(self):
        r"""
        The (first) eccentricity of the sphere is equal to zero. Added for
        compatibility with pymap3d.
        Definition: :math:`e = \dfrac{\sqrt{a^2 - b^2}}{a} = \sqrt{2f - f^2}`.
        Units: adimensional.
        """
        return 0

    def normal_gravity(self, latitude, height, si_units=False):
        r"""
        Normal gravity of the sphere at the given latitude and height.

        Computes the magnitude of the gradient of the gravity potential
        (gravitational + centrifugal; see [HofmannWellenhofMoritz2006]_)
        generated by the sphere at the given spherical latitude :math:`\theta`
        and height above the surface of the sphere :math:`h`:

        .. math::

            \gamma(\theta, h) = \|\vec{\nabla}U(\theta, h)\|

        in which :math:`U = V + \Phi` is the gravity potential of the sphere,
        :math:`V` is the gravitational potential of the sphere, and
        :math:`\Phi` is the centrifugal potential.

        .. caution::

            The current implementation is only valid for heights on or above
            the surface of the sphere.

        Parameters
        ----------
        latitude : float or array
            The spherical latitude where the normal gravity will be computed
            (in degrees).
        height : float or array
            The height above the surface of the sphere of the computation point
            (in meters).
        si_units : bool
            Return the value in mGal (False, default) or m/s² (True)

        Returns
        -------
        gamma : float or array
            The normal gravity in mGal or m/s².

        Examples
        --------

        Normal gravity can be calculated at any spherical latitude and height
        above the sphere:

        >>> sphere = Sphere(
        ...     name="Moon",
        ...     long_name="That's no moon",
        ...     radius=1,
        ...     geocentric_grav_const=2,
        ...     angular_velocity=0.5,
        ... )
        >>> gamma_equator = sphere.normal_gravity(latitude=0, height=0)
        >>> print(f"{gamma_equator:.2f} mGal")
        175000.00 mGal
        >>> gamma_pole = sphere.normal_gravity(latitude=90, height=0)
        >>> print(f"{gamma_pole:.2f} mGal")
        200000.00 mGal

        Notes
        -----

        The gradient of the gravity potential is the sum of the gravitational
        :math:`\vec{g}` and centrifugal :math:`\vec{f}` accelerations for a
        rotating sphere:

        .. math::

            \vec{\nabla}U(\theta, h) = \vec{g}(\theta, h)
                + \vec{f}(\theta, h)

        The radial and latitudinal components of the two acceleration vectors
        are:

        .. math::

            g_r = -\dfrac{GM}{(R + h)^2}

        .. math::

            g_\theta = 0

        and

        .. math::

            f_r = \omega^2 (R + h) \cos^2 \theta

        .. math::

            f_\theta = \omega^2 (R + h) \cos\theta\sin\theta

        in which :math:`R` is the sphere radius, :math:`G` is the gravitational
        constant, :math:`M` is the mass of the sphere, and :math:`\omega` is
        the angular velocity.

        The norm of the combined gravitational and centrifugal accelerations
        is:

        .. math::

            \gamma(\theta, h) = \sqrt{
                \left( \dfrac{GM}{(R + h)^2} \right)^2
                + \left( \omega^2 (R + h) - 2\dfrac{GM}{(R + h)^2} \right)
                \omega^2 (R + h) \cos^2 \theta
            }

        It's worth noting that a sphere under rotation is not in hydrostatic
        equilibrium. Therefore unlike the oblate ellipsoid, it is not it's own
        equipotential gravity surface (as is the case for the ellipsoid), the
        gravity potential is not constant at the surface, and  the normal
        gravity vector is not normal to the surface of the sphere.

        """
        if np.any(height < 0):
            warn(
                "Formulas used are valid for points outside the sphere. "
                "Height must be greater than or equal to zero."
            )

        radial_distance = self.radius + height
        gravity_acceleration = self.geocentric_grav_const / (radial_distance) ** 2
        gamma = np.sqrt(
            gravity_acceleration**2
            + (self.angular_velocity**2 * radial_distance - 2 * gravity_acceleration)
            * self.angular_velocity**2
            * radial_distance
            # Use cos^2 = (1 - sin^2) for more accurate results on the pole
            * (1 - np.sin(np.radians(latitude)) ** 2)
        )

        # Convert gamma from SI to mGal
        if not si_units:
            gamma *= 1e5

        return gamma

    def normal_gravitation(self, height, si_units=False):
        r"""
        Calculate normal gravitation at any height.

        Computes the magnitude of the gradient of the gravitational potential
        generated by the sphere at the given height :math:`h`:

        .. math::

            \gamma(h) = \|\vec{\nabla}V(h)\| = \dfrac{GM}{(R + h)^2}

        in which :math:`R` is the sphere radius, :math:`G` is the gravitational
        constant, and :math:`M` is the mass of the sphere.

        .. caution::

            These expressions are only valid for heights on or above the
            surface of the sphere.

        Parameters
        ----------
        height : float or array
            The height above the surface of the sphere of the computation point
            (in meters).
        si_units : bool
            Return the value in mGal (False, default) or m/s² (True)

        Returns
        -------
        gamma : float or array
            The normal gravitation in mGal.

        Examples
        --------

        Normal gravitation can be calculated at any point. However as this is a
        sphere, only the height is used in the calculation.

        >>> sphere = Sphere(
        ...     name="Moon",
        ...     long_name="That's no moon",
        ...     radius=1,
        ...     geocentric_grav_const=2,
        ...     angular_velocity=0.5,
        ... )
        >>> g = sphere.normal_gravitation(height=1)
        >>> print(f"{g:.2f} mGal")
        50000.00 mGal

        """
        radial_distance = self.radius + height
        gamma = self.geocentric_grav_const / (radial_distance) ** 2

        # Convert gamma from SI to mGal
        if not si_units:
            gamma *= 1e5

        return gamma
