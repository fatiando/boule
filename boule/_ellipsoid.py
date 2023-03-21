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
class Ellipsoid:
    r"""
    A rotating oblate ellipsoid.

    The ellipsoid is defined by four parameters: semimajor axis, flattening,
    geocentric gravitational constant, and angular velocity. It spins around
    it's semiminor axis and has constant gravity potential at its surface. The
    internal density structure of the ellipsoid is unspecified but must be such
    that the constant potential condition is satisfied.

    **This class is read-only:** Input parameters and attributes cannot be
    changed after instantiation.

    **Units:** All input parameters and derived attributes are in SI units.

    Parameters
    ----------
    name : str
        A short name for the ellipsoid, for example ``"WGS84"``.
    semimajor_axis : float
        The semimajor axis of the ellipsoid. The equatorial (large) radius.
        Definition: :math:`a`.
        Units: :math:`m`.
    flattening : float
        The (first) flattening of the ellipsoid.
        Definition: :math:`f = (a - b)/a`.
        Units: adimensional.
    geocentric_grav_const : float
        The geocentric gravitational constant. The product of the mass of the
        ellipsoid :math:`M` and the gravitational constant :math:`G`.
        Definition: :math:`GM`. Units:
        :math:`m^3.s^{-2}`.
    angular_velocity : float
        The angular velocity of the rotating ellipsoid.
        Definition: :math:`\omega`.
        Units: :math:`\\rad.s^{-1}`.
    long_name : str or None
        A long name for the ellipsoid, for example ``"World Geodetic System
        1984"`` (optional).
    reference : str or None
        Citation for the ellipsoid parameter values (optional).


    .. caution::

        Use :class:`boule.Sphere` if you desire zero flattening because there
        are singularities for this particular case in the normal gravity
        calculations.

    Examples
    --------

    We can define an ellipsoid by setting the 4 key numerical parameters and
    some metadata about where they came from:

    >>> ellipsoid = Ellipsoid(
    ...     name="WGS84",
    ...     long_name="World Geodetic System 1984",
    ...     semimajor_axis=6378137,
    ...     flattening=1 / 298.257223563,
    ...     geocentric_grav_const=3986004.418e8,
    ...     angular_velocity=7292115e-11,
    ...     reference=(
    ...         "Hofmann-Wellenhof, B., & Moritz, H. (2006). Physical Geodesy "
    ...         "(2nd, corr. ed. 2006 edition ed.). Wien ; New York: Springer."
    ...     ),
    ... )
    >>> print(ellipsoid) # doctest: +ELLIPSIS
    Ellipsoid(name='WGS84', ...)
    >>> print(ellipsoid.long_name)
    World Geodetic System 1984

    The class then defines several derived attributes based on the input
    parameters:

    >>> print(f"{ellipsoid.semiminor_axis:.4f} m")
    6356752.3142 m
    >>> print(f"{ellipsoid.linear_eccentricity:.8f} m")
    521854.00842339 m
    >>> print(f"{ellipsoid.first_eccentricity:.13e}")
    8.1819190842621e-02
    >>> print(f"{ellipsoid.second_eccentricity:.13e}")
    8.2094437949696e-02
    >>> print(f"{ellipsoid.mean_radius:.4f} m")
    6371008.7714 m
    >>> print(f"{ellipsoid.volume * 1e-9:.5e} km³")
    1.08321e+12 km³
    >>> print(f"{ellipsoid.gravity_equator:.10f} m/s²")
    9.7803253359 m/s²
    >>> print(f"{ellipsoid.gravity_pole:.10f} m/s²")
    9.8321849379 m/s²

    Use the class methods for calculating normal gravity and other geometric
    quantities.
    """

    name = attr.ib()
    semimajor_axis = attr.ib()
    flattening = attr.ib()
    geocentric_grav_const = attr.ib()
    angular_velocity = attr.ib()
    long_name = attr.ib(default=None)
    reference = attr.ib(default=None)

    @flattening.validator
    def _check_flattening(self, flattening, value):
        "Check if flattening is valid"
        if value < 0 or value >= 1:
            raise ValueError(
                f"Invalid flattening '{value}'. "
                "Should be greater than zero and lower than 1."
            )
        if value == 0:
            raise ValueError(
                "Flattening equal to zero will lead to errors in normal gravity. "
                "Use boule.Sphere for representing ellipsoids with zero flattening."
            )
        if value < 1e-7:
            warn(
                f"Flattening is too close to zero ('{value}'). "
                "This may lead to inaccurate results and division by zero errors. "
                "Use boule.Sphere for representing ellipsoids with zero flattening."
            )

    @semimajor_axis.validator
    def _check_semimajor_axis(self, semimajor_axis, value):
        "Check if semimajor_axis is valid"
        if not value > 0:
            raise ValueError(
                f"Invalid semi-major axis '{value}'. Should be greater than zero."
            )

    @geocentric_grav_const.validator
    def _check_geocentric_grav_const(self, geocentric_grav_const, value):
        "Warn if geocentric_grav_const is negative"
        if value < 0:
            warn(f"The geocentric gravitational constant is negative: '{value}'")

    @property
    def semiminor_axis(self):
        """
        The semiminor (small/polar) axis of the ellipsoid.
        Definition: :math:`b = a (1 - f)`.
        Units: :math:`m`.
        """
        return self.semimajor_axis * (1 - self.flattening)

    @property
    def thirdflattening(self):
        r"""
        The third flattening of the ellipsoid (used in geodetic calculations).
        Definition: :math:`f^{\prime\prime}= \dfrac{a -b}{a + b}`.
        Units: adimensional.
        """
        return (self.semimajor_axis - self.semiminor_axis) / (
            self.semimajor_axis + self.semiminor_axis
        )

    @property
    def linear_eccentricity(self):
        r"""
        The linear eccentricity of the ellipsoid. The distance between the
        ellipsoid's center and one of its foci.
        Definition: :math:`c = \sqrt{a^2 - b^2}`.
        Units: :math:`m`.
        """
        return np.sqrt(self.semimajor_axis**2 - self.semiminor_axis**2)

    @property
    def eccentricity(self):
        "Alias for the first eccentricity."
        return self.first_eccentricity

    @property
    def first_eccentricity(self):
        r"""
        The (first) eccentricity of the ellipsoid. The ratio between the linear
        eccentricity and the semimajor axis.
        Definition: :math:`e = \dfrac{\sqrt{a^2 - b^2}}{a} = \sqrt{2f - f^2}`.
        Units: adimensional.
        """
        return np.sqrt(2 * self.flattening - self.flattening**2)

    @property
    def second_eccentricity(self):
        r"""
        The second eccentricity of the ellipsoid. The ratio between the linear
        eccentricity and the semiminor axis.
        Definition: :math:`e^\prime = \dfrac{\sqrt{a^2 - b^2}}{b}
        = \dfrac{\sqrt{2f - f^2}}{1 - f}`.
        Units: adimensional.
        """
        return self.first_eccentricity / (1 - self.flattening)

    @property
    def mean_radius(self):
        """
        The arithmetic mean radius of the ellipsoid [Moritz1988]_.
        Definition: :math:`R_1 = (2a + b)/3`.
        Units: :math:`m`.
        """
        return 1 / 3 * (2 * self.semimajor_axis + self.semiminor_axis)

    @property
    def volume(self):
        r"""
        The volume bounded by the ellipsoid.
        Definition: :math:`V = \dfrac{4}{3} \pi a^2 c`.
        Units: :math:`m^3`.
        """
        return (4 / 3 * np.pi) * self.semimajor_axis**2 * self.semiminor_axis

    @property
    def _emm(self):
        "Auxiliary quantity used to calculate gravity at the pole and equator"
        return (
            self.angular_velocity**2
            * self.semimajor_axis**2
            * self.semiminor_axis
            / self.geocentric_grav_const
        )

    @property
    def gravity_equator(self):
        """
        The norm of the gravity acceleration vector (gravitational +
        centrifugal accelerations) at the equator on the surface of the
        ellipsoid. Units: :math:`m/s^2`.
        """
        ratio = self.semiminor_axis / self.linear_eccentricity
        arctan = np.arctan2(self.linear_eccentricity, self.semiminor_axis)
        aux = (
            self.second_eccentricity
            * (3 * (1 + ratio**2) * (1 - ratio * arctan) - 1)
            / (3 * ((1 + 3 * ratio**2) * arctan - 3 * ratio))
        )
        axis_mul = self.semimajor_axis * self.semiminor_axis
        result = (
            self.geocentric_grav_const * (1 - self._emm - self._emm * aux) / axis_mul
        )
        return result

    @property
    def gravity_pole(self):
        """
        The norm of the gravity acceleration vector (gravitational +
        centrifugal accelerations) at the poles on the surface of the
        ellipsoid. Units: :math:`m/s^2`.
        """
        ratio = self.semiminor_axis / self.linear_eccentricity
        arctan = np.arctan2(self.linear_eccentricity, self.semiminor_axis)
        aux = (
            self.second_eccentricity
            * (3 * (1 + ratio**2) * (1 - ratio * arctan) - 1)
            / (1.5 * ((1 + 3 * ratio**2) * arctan - 3 * ratio))
        )
        result = (
            self.geocentric_grav_const
            * (1 + self._emm * aux)
            / self.semimajor_axis**2
        )
        return result

    def geocentric_radius(self, latitude, geodetic=True):
        r"""
        Radial distance from the center of the ellipsoid to its surface.

        Can be calculated from either geocentric geodetic or geocentric
        spherical latitudes.

        Parameters
        ----------
        latitude : float or array
            Latitude coordinates on geodetic coordinate system in degrees.
        geodetic : bool
            If True (default), will assume that latitudes are geodetic
            latitudes. Otherwise, will assume that they are geocentric
            spherical latitudes.

        Returns
        -------
        geocentric_radius : float or array
            The geocentric radius for the given latitude(s) in the same units
            as the ellipsoid axis.


        .. tip::

            No elevation is taken into account. If you need the geocentric
            radius at a height other than zero, use
            ``pymap3d.geodetic2spherical`` instead.

        Notes
        ------

        The geocentric surface radius :math:`R` is a function of the geocentric
        geodetic latitude :math:`\phi` and the semimajor and semiminor axis,
        :math:`a` and :math:`b` [1]_:

        .. math::

            R(\phi) = \sqrt{
                \dfrac{
                    (a^2\cos\phi)^2 + (b^2\sin\phi)^2
                }{
                    (a\cos\phi)^2 + (b\sin\phi)^2
                }
            }

        Alternatively, the geocentric surface radius can also be calculated
        using the geocentric spherical latitude :math:`\theta` by passing
        ``geodetic=False``:

        .. math::

            R(\theta) = \sqrt{
                \dfrac{
                    1
                }{
                    (\frac{\cos\theta}{a})^2 + (\frac{\sin\theta}{b})^2
                }
            }

        This can be useful if you already have the geocentric spherical
        latitudes and need the geocentric radius of the ellipsoid (for example,
        in spherical harmonic synthesis). In these cases, the coordinate
        conversion route is not possible since we need the radial coordinates
        to do that in the first place.

        References
        ----------

        .. [1] See https://en.wikipedia.org/wiki/Earth_radius#Geocentric_radius

        """
        latitude_rad = np.radians(latitude)
        coslat, sinlat = np.cos(latitude_rad), np.sin(latitude_rad)
        # Avoid doing this in favour of having the user do the conversions when
        # possible. It's not the case here, so we made an exception.
        if geodetic:
            radius = np.sqrt(
                (
                    (self.semimajor_axis**2 * coslat) ** 2
                    + (self.semiminor_axis**2 * sinlat) ** 2
                )
                / (
                    (self.semimajor_axis * coslat) ** 2
                    + (self.semiminor_axis * sinlat) ** 2
                )
            )
        else:
            radius = np.sqrt(
                1
                / (
                    (coslat / self.semimajor_axis) ** 2
                    + (sinlat / self.semiminor_axis) ** 2
                )
            )
        return radius

    def prime_vertical_radius(self, sinlat):
        r"""
        The prime vertical radius of curvature for a given geodetic latitude.

        .. note::

            This function receives the sine of the latitude as input to avoid
            repeated computations of trigonometric functions in
            methods/functions that rely on it.

        Parameters
        ----------
        sinlat : float or array-like
            Sine of the geocentric geodetic latitude.

        Returns
        -------
        prime_vertical_radius : float or array-like
            Prime vertical radius given in the same units as the semi-major
            axis

        Notes
        -----

        The prime vertical radius of curvature :math:`N` is defined as [2]_:

        .. math::

            N(\phi) = \frac{a}{\sqrt{1 - e^2 \sin^2(\phi)}}

        Where :math:`a` is the semimajor axis and :math:`e` is the first
        eccentricity.

        References
        ----------

        .. [2] See https://en.wikipedia.org/wiki/Earth_radius#Prime_vertical

        """
        return self.semimajor_axis / np.sqrt(
            1 - self.first_eccentricity**2 * sinlat**2
        )

    def geodetic_to_spherical(self, longitude, latitude, height):
        """
        Convert from geodetic to geocentric spherical coordinates.

        The geodetic datum is defined by this ellipsoid. The coordinates are
        converted following [Vermeille2002]_.

        Parameters
        ----------
        longitude : array
            Longitude coordinates on geodetic coordinate system in degrees.
        latitude : array
            Latitude coordinates on geodetic coordinate system in degrees.
        height : array
            Ellipsoidal heights in meters.

        Returns
        -------
        longitude : array
            Longitude coordinates on geocentric spherical coordinate system in
            degrees.
            The longitude coordinates are not modified during this conversion.
        spherical_latitude : array
            Converted latitude coordinates on geocentric spherical coordinate
            system in degrees.
        radius : array
            Converted spherical radius coordinates in meters.
        """
        sinlat = np.sin(np.radians(latitude))
        coslat = np.sqrt(1 - sinlat**2)
        prime_radius = self.prime_vertical_radius(sinlat)
        # Instead of computing X and Y, we only compute the projection on the
        # XY plane: xy_projection = sqrt( X**2 + Y**2 )
        xy_projection = (height + prime_radius) * coslat
        z_cartesian = (height + (1 - self.eccentricity**2) * prime_radius) * sinlat
        radius = np.hypot(xy_projection, z_cartesian)
        spherical_latitude = np.degrees(np.arcsin(z_cartesian / radius))
        return longitude, spherical_latitude, radius

    def spherical_to_geodetic(self, longitude, spherical_latitude, radius):
        """
        Convert from geocentric spherical to geodetic coordinates.

        The geodetic datum is defined by this ellipsoid. The coordinates are
        converted following [Vermeille2002]_.

        Parameters
        ----------
        longitude : array
            Longitude coordinates on geocentric spherical coordinate system in
            degrees.
        spherical_latitude : array
            Latitude coordinates on geocentric spherical coordinate system in
            degrees.
        radius : array
            Spherical radius coordinates in meters.

        Returns
        -------
        longitude : array
            Longitude coordinates on geodetic coordinate system in degrees.
            The longitude coordinates are not modified during this conversion.
        latitude : array
            Converted latitude coordinates on geodetic coordinate system in
            degrees.
        height : array
            Converted ellipsoidal height coordinates in meters.
        """
        sinlat = np.sin(np.radians(spherical_latitude))
        coslat = np.sqrt(1 - sinlat**2)
        big_z = radius * sinlat
        p_0 = radius**2 * coslat**2 / self.semimajor_axis**2
        q_0 = (1 - self.eccentricity**2) / self.semimajor_axis**2 * big_z**2
        r_0 = (p_0 + q_0 - self.eccentricity**4) / 6
        s_0 = self.eccentricity**4 * p_0 * q_0 / 4 / r_0**3
        t_0 = np.cbrt(1 + s_0 + np.sqrt(2 * s_0 + s_0**2))
        u_0 = r_0 * (1 + t_0 + 1 / t_0)
        v_0 = np.sqrt(u_0**2 + q_0 * self.eccentricity**4)
        w_0 = self.eccentricity**2 * (u_0 + v_0 - q_0) / 2 / v_0
        k = np.sqrt(u_0 + v_0 + w_0**2) - w_0
        big_d = k * radius * coslat / (k + self.eccentricity**2)
        hypot_dz = np.hypot(big_d, big_z)
        latitude = np.degrees(2 * np.arctan2(big_z, (big_d + hypot_dz)))
        height = (k + self.eccentricity**2 - 1) / k * hypot_dz
        return longitude, latitude, height

    def normal_gravity(self, latitude, height, si_units=False):
        r"""
        Normal gravity of the ellipsoid at the given latitude and height.

        Computes the magnitude of the gradient of the gravity potential
        (gravitational + centrifugal; see [HofmannWellenhofMoritz2006]_)
        generated by the ellipsoid at the given geodetic latitude :math:`\phi`
        and height above the ellipsoid :math:`h` (geometric height).

        .. math::

            \gamma(\phi, h) = \|\vec{\nabla}U(\phi, h)\|

        in which :math:`U = V + \Phi` is the gravity potential of the
        ellipsoid, :math:`V` is the gravitational potential of the ellipsoid,
        and :math:`\Phi` is the centrifugal potential.

        Assumes that the internal density distribution of the ellipsoid is such
        that the gravity potential is constant at its surface.

        Based on closed-form expressions by [Lakshmanan1991]_ and corrected by
        [LiGotze2001]_ which don't require the free-air correction.

        .. caution::

            These expressions are only valid for heights on or above the
            surface of the ellipsoid.

        Parameters
        ----------
        latitude : float or array
            The geodetic latitude where the normal gravity will be computed (in
            degrees).
        height : float or array
            The ellipsoidal (geometric) height of computation the point (in
            meters).
        si_units : bool
            Return the value in mGal (False, default) or m/s² (True)

        Returns
        -------
        gamma : float or array
            The normal gravity in mGal or m/s².

        """
        # Warn if height is negative
        if np.any(height < 0):
            warn(
                "Formulas used are valid for points outside the ellipsoid."
                "Height must be greater than or equal to zero."
            )

        # Pre-compute to avoid repeated calculations
        sinlat = np.sin(np.radians(latitude))
        coslat = np.sqrt(1 - sinlat**2)

        # The terms below follow the variable names from Li and Goetze (2001).
        # The prime terms (*_p) refer to quantities on an ellipsoid passing
        # through the computation point.

        # The reduced latitude of the projection of the point on the ellipsoid
        beta = np.arctan2(self.semiminor_axis * sinlat, self.semimajor_axis * coslat)
        sinbeta = np.sin(beta)
        cosbeta = np.sqrt(1 - sinbeta**2)

        # Distance between the computation point and the equatorial plane
        z_p2 = (self.semiminor_axis * sinbeta + height * sinlat) ** 2
        # Distance between the computation point and the spin axis
        r_p2 = (self.semimajor_axis * cosbeta + height * coslat) ** 2

        # Auxiliary variables
        big_d = (r_p2 - z_p2) / self.linear_eccentricity**2
        big_r = (r_p2 + z_p2) / self.linear_eccentricity**2

        # Reduced latitude of the computation point
        cosbeta_p2 = 0.5 + big_r / 2 - np.sqrt(0.25 + big_r**2 / 4 - big_d / 2)
        sinbeta_p2 = 1 - cosbeta_p2

        # Auxiliary variables
        b_p = np.sqrt(r_p2 + z_p2 - self.linear_eccentricity**2 * cosbeta_p2)
        q_0 = 0.5 * (
            (1 + 3 * (self.semiminor_axis / self.linear_eccentricity) ** 2)
            * np.arctan2(self.linear_eccentricity, self.semiminor_axis)
            - 3 * self.semiminor_axis / self.linear_eccentricity
        )
        q_p = (
            3
            * (1 + (b_p / self.linear_eccentricity) ** 2)
            * (
                1
                - b_p
                / self.linear_eccentricity
                * np.arctan2(self.linear_eccentricity, b_p)
            )
            - 1
        )
        big_w = np.sqrt(
            (b_p**2 + self.linear_eccentricity**2 * sinbeta_p2)
            / (b_p**2 + self.linear_eccentricity**2)
        )

        # Put together gamma using 3 separate terms
        term1 = self.geocentric_grav_const / (b_p**2 + self.linear_eccentricity**2)
        term2 = (0.5 * sinbeta_p2 - 1 / 6) * (
            self.semimajor_axis**2
            * self.linear_eccentricity
            * q_p
            * self.angular_velocity**2
            / ((b_p**2 + self.linear_eccentricity**2) * q_0)
        )
        term3 = -cosbeta_p2 * b_p * self.angular_velocity**2
        gamma = (term1 + term2 + term3) / big_w

        # Convert gamma from SI to mGal
        if not si_units:
            gamma *= 1e5

        return gamma
