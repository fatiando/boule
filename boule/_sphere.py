# Copyright (c) 2019 The Boule Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Define the reference sphere (ellipsoid with 0 flattening).
"""
import textwrap
from warnings import warn

import attr
import numpy as np

from ._constants import G


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
    comments : str or None
        Additional comments regarding the ellipsoid (optional).

    Notes
    -----

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
    ...     long_name="Moon Spheroid",
    ...     radius=1737151,
    ...     geocentric_grav_const=4902800070000.0,
    ...     angular_velocity=2.6617073e-06,
    ...     reference="Wieczorek (2015)",
    ...     comments="This is the same as the boule Moon2015 spheroid."
    ... )
    >>> print(sphere) # doctest: +ELLIPSIS
    Moon - Moon Spheroid
    Spheroid:
      • Radius: 1737151 m
      • GM: 4902800070000.0 m³/s²
      • Angular velocity: 2.6617073e-06 rad/s
    Source:
      Wieczorek (2015)
    Comments:
      This is the same as the boule Moon2015 spheroid.

    >>> print(sphere.long_name)
    Moon Spheroid

    The sphere defines semi-axess, flattening, and some eccentricities similar
    to :class:`~bould.Ellipsoid` for compatibility:

    >>> print(sphere.semiminor_axis)
    1737151
    >>> print(sphere.semimajor_axis)
    1737151
    >>> print(sphere.first_eccentricity)
    0
    >>> print(sphere.eccentricity)
    0
    >>> print(sphere.flattening)
    0
    >>> print(sphere.thirdflattening)
    0
    >>> print(sphere.mean_radius)
    1737151
    >>> print(sphere.semiaxes_mean_radius)
    1737151
    >>> print(f"{sphere.volume_equivalent_radius:.1f} m")
    1737151.0 m
    >>> print(f"{sphere.volume:.12e} m³")
    2.195843181718e+19 m³
    >>> print(f"{sphere.area:.12e} m²")
    3.792145613798e+13 m²
    >>> print(sphere.area_equivalent_radius)
    1737151
    >>> print(f"{sphere.mass:.12e} kg")
    7.345789176393e+22 kg
    >>> print(f"{sphere.mean_density:.0f} kg/m³")
    3345 kg/m³
    >>> print(f"{sphere.reference_normal_gravitational_potential:.3f} m²/s²")
    2822322.337 m²/s²

    """

    name = attr.ib()
    radius = attr.ib()
    geocentric_grav_const = attr.ib()
    angular_velocity = attr.ib()
    long_name = attr.ib(default=None)
    reference = attr.ib(default=None)
    comments = attr.ib(default=None)

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
        The semiminor axis of the sphere is equal to its radius.
        Units: :math:`m`.
        """
        return self.radius

    @property
    def semimedium_axis(self):
        """
        The semimedium axis of the sphere is equal to its radius.
        Units: :math:`m`.
        """
        return self.radius

    @property
    def semimajor_axis(self):
        """
        The semimajor axis of the sphere is equal to its radius.
        Units: :math:`m`.
        """
        return self.radius

    @property
    def semimajor_axis_longitude(self):
        r"""
        The semimajor axis longitude of the sphere is equal to zero.
        Definition: :math:`\lambda_a = 0`.
        Units: :math:`m`.
        """
        return 0

    @property
    def flattening(self):
        r"""
        The flattening of the sphere is equal to zero.
        Definition: :math:`f = \dfrac{a - b}{a}`.
        Units: adimensional.
        """
        return 0

    @property
    def thirdflattening(self):
        r"""
        The third flattening of the sphere is equal to zero.
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
        The (first) eccentricity of the sphere is equal to zero.
        Definition: :math:`e = \dfrac{\sqrt{a^2 - b^2}}{a} = \sqrt{2f - f^2}`.
        Units: adimensional.
        """
        return 0

    @property
    def area(self):
        r"""
        The area of the sphere.
        Definition: :math:`A = 4 \pi r^2`.
        Units: :math:`m^2`.
        """
        return 4 * np.pi * self.radius**2

    @property
    def mean_radius(self):
        """
        The mean radius of the ellipsoid is equal to its radius.
        Definition: :math:`R_0 = R`.
        Units: :math:`m`.
        """
        return self.radius

    @property
    def semiaxes_mean_radius(self):
        """
        The arithmetic mean radius of the ellipsoid semi-axes is equal to its
        radius.
        Definition: :math:`R_1 = R`.
        Units: :math:`m`.
        """
        return self.radius

    @property
    def volume(self):
        r"""
        The volume of the sphere.
        Definition: :math:`V = \dfrac{4}{3} \pi r^3`.
        Units: :math:`m^3`.
        """
        return (4 / 3 * np.pi) * self.radius**3

    @property
    def area_equivalent_radius(self):
        """
        The area equivalent radius of the sphere is equal to its radius.
        Definition: :math:`R_2 = R`.
        Units: :math:`m`.
        """
        return self.radius

    @property
    def mass(self):
        r"""
        The mass of the sphere.
        Definition: :math:`M = GM / G`.
        Units: :math:`kg`.
        """
        return self.geocentric_grav_const / G

    @property
    def mean_density(self):
        r"""
        The mean density of the sphere.
        Definition: :math:`\rho = M / V`.
        Units: :math:`kg / m^3`.
        """
        return self.mass / self.volume

    @property
    def volume_equivalent_radius(self):
        r"""
        The volume equivalent radius of the sphere is equal to its radius.
        Definition: :math:`R_3 = R`.
        Units: :math:`m`.
        """
        return self.radius

    @property
    def reference_normal_gravitational_potential(self):
        r"""
        The normal gravitational potential on the surface of the sphere.
        Definition: :math:`U_0 = \dfrac{GM}{R}`.
        Units: :math:`m^2 / s^2`.
        """
        return self.geocentric_grav_const / self.radius

    def __str__(self):
        s = self.name + " - " + self.long_name + "\n"
        s += "Spheroid:\n"
        s += f"  • Radius: {self.radius} m\n"
        s += f"  • GM: {self.geocentric_grav_const} m³/s²\n"
        s += f"  • Angular velocity: {self.angular_velocity} rad/s"
        if self.reference is not None:
            s += "\nSource:"
            for ref in self.reference.splitlines():
                s += "\n" + textwrap.fill(
                    ref, width=72, initial_indent=2 * " ", subsequent_indent=4 * " "
                )
        if self.comments is not None:
            s += "\nComments:\n"
            s += textwrap.fill(
                self.comments,
                width=72,
                initial_indent=2 * " ",
                subsequent_indent=2 * " ",
            )
        return s

    def normal_gravity(self, coordinates, si_units=False):
        r"""
        Normal gravity of the sphere.

        Computes the magnitude of the gradient of the :term:`gravity potential`
        generated by the sphere at the given points.

        .. note::

            Unlike the :class:`boule.Ellipsoid`, the :term:`gravitational
            potential` of the sphere assumes a homogeneous density
            distribution. There is no requirement that the gravity potential at
            the surface of the sphere be constant, like for the ellipsoid. This
            is because the ellipsoid equations have a singularity when the
            flattening tends to zero.

        .. caution::

            These expressions are only valid for heights on or above the
            surface of the sphere.

        Parameters
        ----------
        coordinates : tuple = (longitude, latitude_spherical, height)
            Longitude, latitude, and height coordinates of the computation
            points in a geocentric spherical coordinate system. The height is
            measured from the surface of the sphere. Each element can be
            a single number or an array. The shape of the arrays must be
            compatible. Longitude and latitude must be in degrees and height in
            meters. Since longitude is not used in computations (the field is
            symmetric with longitude), it can be assigned ``None``.
        si_units : bool
            Return the value in mGal (False, default) or m/s² (True).

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
        >>> gamma_equator = sphere.normal_gravity((None, 0, 0))
        >>> print(f"{gamma_equator:.2f} mGal")
        175000.00 mGal
        >>> gamma_pole = sphere.normal_gravity((None, 90, 0))
        >>> print(f"{gamma_pole:.2f} mGal")
        200000.00 mGal

        Notes
        -----
        Computes the magnitude of the gradient of the :term:`gravity potential`
        (gravitational + centrifugal) generated by the sphere at the given
        spherical latitude :math:`\theta` and height above the surface of the
        sphere :math:`h`:

        .. math::

            \gamma(\theta, h) = \|\vec{\nabla}U(\theta, h)\|

        in which :math:`U = V + \Phi` is the gravity potential of the sphere,
        :math:`V` is the gravitational potential of the sphere, and
        :math:`\Phi` is the centrifugal potential.

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
        equilibrium. Therefore, unlike the oblate ellipsoid, the gravity
        potential is not constant at the surface, and the normal gravity vector
        is not normal to the surface of the sphere.
        """
        latitude, height = coordinates[1:]
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

    def normal_gravitation(self, coordinates, si_units=False):
        r"""
        Normal gravitation of the sphere.

        Computes the magnitude of the gradient of the :term:`gravitational
        potential` generated by the sphere at the points. Assumes a homogeneous
        internal density distribution for the sphere.

        .. caution::

            These expressions are only valid for heights on or above the
            surface of the sphere.

        Parameters
        ----------
        coordinates : tuple = (longitude, latitude_spherical, height)
            Longitude, latitude, and height coordinates of the computation
            points in a geocentric spherical coordinate system. The height is
            measured from the surface of the sphere. Each element can be
            a single number or an array. The shape of the arrays must be
            compatible. Longitude and latitude must be in degrees and height in
            meters. Since longitude and latitude are not used in computations
            (the field is symmetric), they can be assigned ``None``.
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
        >>> g = sphere.normal_gravitation((None, None, 1))
        >>> print(f"{g:.2f} mGal")
        50000.00 mGal

        Notes
        -----
        Computes the magnitude of the gradient of the :term:`gravitational
        potential` generated by the sphere at the given height :math:`h`:

        .. math::

            \gamma(h) = \|\vec{\nabla}V(h)\| = \dfrac{GM}{(R + h)^2}

        in which :math:`R` is the sphere radius, :math:`G` is the gravitational
        constant, and :math:`M` is the mass of the sphere.
        """
        height = coordinates[2]
        radial_distance = self.radius + height
        gamma = self.geocentric_grav_const / (radial_distance) ** 2

        # Convert gamma from SI to mGal
        if not si_units:
            gamma *= 1e5

        return gamma

    def normal_gravity_potential(self, coordinates):
        r"""
        Normal gravity potential of the sphere.

        Computes the normal :term:`gravity potential` (gravitational
        + centrifugal) generated by the sphere at the given points. Assumes
        a homogeneous internal density distribution for the sphere.

        .. caution::

            These expressions are only valid for heights on or above the
            surface of the sphere.

        Parameters
        ----------
        coordinates : tuple = (longitude, latitude_spherical, height)
            Longitude, latitude, and height coordinates of the computation
            points in a geocentric spherical coordinate system. The height is
            measured from the surface of the sphere. Each element can be
            a single number or an array. The shape of the arrays must be
            compatible. Longitude and latitude must be in degrees and height in
            meters. Since longitude is not used in computations (the field is
            symmetric with longitude), it can be assigned ``None``.

        Returns
        -------
        U : float or array
            The normal gravity potential in m²/s².

        Notes
        -----
        Computes the normal gravity potential (gravitational + centrifugal)
        generated by the sphere at the given spherical latitude :math:`\theta`
        and height above the surface of the sphere :math:`h`:

        .. math::

            U(\theta, h) = V(h) + \Phi(\theta, h) = \dfrac{GM}{(R + h)}
            + \dfrac{1}{2} \omega^2 \left(R + h\right)^2 \cos^2(\theta)

        in which :math:`U = V + \Phi` is the gravity potential of the sphere,
        :math:`V` is the gravitational potential of the sphere, and
        :math:`\Phi` is the centrifugal potential.

        A sphere under rotation is not in hydrostatic equilibrium. Therefore,
        unlike the oblate ellipsoid, the :term:`gravity potential` is not
        constant at the surface, and the normal gravity vector is not normal to
        the surface of the sphere.
        """
        latitude, height = coordinates[1:]
        if np.any(height < 0):
            warn(
                "Formulas used are valid for points outside the sphere. "
                "Height must be greater than or equal to zero."
            )

        radial_distance = self.radius + height
        big_u = self.geocentric_grav_const / radial_distance
        big_phi = (
            0.5
            * (
                self.angular_velocity
                * (self.radius + height)
                * np.cos(np.radians(latitude))
            )
            ** 2
        )

        return big_u + big_phi

    def normal_gravitational_potential(self, coordinates):
        r"""
        Normal gravitational potential of the sphere.

        Computes the normal :term:`gravitational potential` generated by the
        sphere at the given points. Assumes a homogeneous internal density
        distribution for the sphere.

        .. caution::

            These expressions are only valid for heights on or above the
            surface of the sphere.

        Parameters
        ----------
        coordinates : tuple = (longitude, latitude_spherical, height)
            Longitude, latitude, and height coordinates of the computation
            points in a geocentric spherical coordinate system. The height is
            measured from the surface of the sphere. Each element can be
            a single number or an array. The shape of the arrays must be
            compatible. Longitude and latitude must be in degrees and height in
            meters. Since longitude and latitude are not used in computations
            (the field is symmetric), they can be assigned ``None``.

        Returns
        -------
        V : float or array
            The normal gravitational potential in m²/s².

        Notes
        -----
        Computes the normal :term:`gravitational potential` generated by the
        sphere at the given height above the surface of the sphere :math:`h`:

        .. math::

            V(h) = \dfrac{GM}{(R + h)}

        in which :math:`R` is the sphere radius and :math:`GM` is the
        geocentric gravitational constant of the sphere.
        """
        height = coordinates[2]
        if np.any(height < 0):
            warn(
                "Formulas used are valid for points outside the sphere. "
                "Height must be greater than or equal to zero."
            )
        radial_distance = self.radius + height
        return self.geocentric_grav_const / radial_distance

    def centrifugal_potential(self, coordinates):
        r"""
        Centrifugal potential of the rotating sphere.

        Calculate the centrifugal potential due to the rotation of the
        sphere about its z-axis at the given points.

        Parameters
        ----------
        coordinates : tuple = (longitude, latitude_spherical, height)
            Longitude, latitude, and height coordinates of the computation
            points in a geocentric spherical coordinate system. The height is
            measured from the surface of the sphere. Each element can be
            a single number or an array. The shape of the arrays must be
            compatible. Longitude and latitude must be in degrees and height in
            meters. Since longitude is not used in computations (the field is
            symmetric with longitude), it can be assigned ``None``.

        Returns
        -------
        Phi : float or array
            The centrifugal potential in m²/s².

        Notes
        -----
        The centrifugal potential :math:`\Phi` at latitude :math:`\theta` and
        height above the sphere :math:`h` is

        .. math::

            \Phi(\theta, h) = \dfrac{1}{2}
                \omega^2 \left(R + h\right)^2 \cos^2(\theta)

        in which :math:`R` is the sphere radius and :math:`\omega` is the
        angular velocity.
        """
        latitude, height = coordinates[1:]
        coslat = np.cos(np.radians(latitude))
        result = 0.5 * (self.angular_velocity * (self.radius + height) * coslat) ** 2
        return result
