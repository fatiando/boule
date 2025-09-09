# Copyright (c) 2019 The Boule Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Module for defining and setting the reference ellipsoid.
"""
import textwrap
from warnings import warn

import attr
import numpy as np

from ._constants import G


# Don't let ellipsoid parameters be changed to avoid messing up calculations
# accidentally.
@attr.s(frozen=True)
class Ellipsoid:
    r"""
    A rotating oblate ellipsoid.

    The ellipsoid is defined by four parameters: semimajor axis, flattening,
    geocentric gravitational constant, and angular velocity. It spins around
    its semiminor axis and has constant gravity potential at its surface. The
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
    comments : str or None
        Additional comments regarding the ellipsoid (optional).

    Notes
    -----

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
    ...     reference="Hofmann-Wellenhof & Moritz (2006)",
    ...     comments="This is the same as the boule WGS84 ellipsoid.",
    ... )
    >>> print(ellipsoid) # doctest: +ELLIPSIS
    WGS84 - World Geodetic System 1984
    Oblate ellipsoid:
      • Semimajor axis: 6378137 m
      • Flattening: 0.0033528106647474805
      • GM: 398600441800000.0 m³/s²
      • Angular velocity: 7.292115e-05 rad/s
    Source:
      Hofmann-Wellenhof & Moritz (2006)
    Comments:
      This is the same as the boule WGS84 ellipsoid.

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
    6370994.4018 m
    >>> print(f"{ellipsoid.semiaxes_mean_radius:.4f} m")
    6371008.7714 m
    >>> print(f"{ellipsoid.volume_equivalent_radius:.4f} m")
    6371000.7900 m
    >>> print(f"{ellipsoid.mass:.10e} kg")
    5.9721684941e+24 kg
    >>> print(f"{ellipsoid.mean_density:.0f} kg/m³")
    5513 kg/m³
    >>> print(f"{ellipsoid.volume * 1e-9:.5e} km³")
    1.08321e+12 km³
    >>> print(f"{ellipsoid.area:.10e} m²")
    5.1006562172e+14 m²
    >>> print(f"{ellipsoid.area_equivalent_radius:0.4f} m")
    6371007.1809 m
    >>> print(f"{ellipsoid.gravity_equator:.10f} m/s²")
    9.7803253359 m/s²
    >>> print(f"{ellipsoid.gravity_pole:.10f} m/s²")
    9.8321849379 m/s²
    >>> print(f"{ellipsoid.reference_normal_gravity_potential:.3f} m²/s²")
    62636851.715 m²/s²

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
    comments = attr.ib(default=None)

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
    def semimedium_axis(self):
        """
        The semimedium axis of the ellipsoid is equal to its semimajor axis.
        Units: :math:`m`.
        """
        return self.semimajor_axis

    @property
    def semimajor_axis_longitude(self):
        r"""
        The semimajor axis longitude of the ellipsoid is equal to zero.
        Definition: :math:`\lambda_a = 0`.
        Units: :math:`m`.
        """
        return 0

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
        Definition: :math:`E = \sqrt{a^2 - b^2}`.
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
        r"""
        The mean radius of the ellipsoid. This is equivalent to the degree 0
        spherical harmonic coefficient of the ellipsoid shape.

        Definition: :math:`R_0 = \dfrac{1}{4 \pi} {\displaystyle \int_0^{\pi}
        \int_0^{2 \pi}} r(\theta) \sin \theta \, d\theta \, d\lambda`

        in which :math:`r` is the ellipsoid spherical radius, :math:`\theta` is
        spherical latitude, and :math:`\lambda` is spherical longitude.

        Units: :math:`m`.
        """
        # The mean radius is obtained by integration in spherical coordinates.
        # The integral over longitude is 2 pi, and the integral over spherical
        # latitude is performed using Gauss-Legendre quadrature. Tests show
        # that n = 30 will return the mean radius to machine precision for an
        # object with a flattening of 0.5 (which is 100 times larger than that
        # of Mars). In an abundance of caution, we chose to use n = 50.
        n = 50
        x, weights = np.polynomial.legendre.leggauss(n)
        geocentric_latitude = 90.0 - np.rad2deg(np.arccos(x))
        radius = self.geocentric_radius(geocentric_latitude, geodetic=False)
        return np.sum(radius * weights) / 2

    @property
    def semiaxes_mean_radius(self):
        """
        The arithmetic mean radius of the ellipsoid semi-axes [Moritz1988]_.
        Definition: :math:`R_1 = (2a + b)/3`.
        Units: :math:`m`.
        """
        return 1 / 3 * (2 * self.semimajor_axis + self.semiminor_axis)

    @property
    def area(self):
        r"""
        The area of the ellipsoid.
        Definition: :math:`A = 2 \pi a^2 \left(1 + \dfrac{b^2}{e a^2}
        \text{arctanh}\,e \right)`.
        Units: :math:`m^2`.
        """
        # see https://en.wikipedia.org/wiki/Ellipsoid#Surface_area
        return (
            2
            * np.pi
            * self.semimajor_axis**2
            * (
                1
                + (self.semiminor_axis / self.semimajor_axis) ** 2
                / self.first_eccentricity
                * np.arctanh(self.first_eccentricity)
            )
        )

    @property
    def volume(self):
        r"""
        The volume bounded by the ellipsoid.
        Definition: :math:`V = \dfrac{4}{3} \pi a^2 b`.
        Units: :math:`m^3`.
        """
        return (4 / 3 * np.pi) * self.semimajor_axis**2 * self.semiminor_axis

    @property
    def reference_normal_gravity_potential(self):
        r"""
        The normal gravity potential on the surface of the ellipsoid.
        Definition: :math:`U_0 = \dfrac{GM}{E} \arctan{\dfrac{E}{b}}
        + \dfrac{1}{3} \omega^2 a^2`.
        Units: :math:`m^2 / s^2`.
        """
        return (
            self.geocentric_grav_const
            / self.linear_eccentricity
            * np.arctan(self.linear_eccentricity / self.semiminor_axis)
            + (1 / 3) * self.angular_velocity**2 * self.semimajor_axis**2
        )

    @property
    def area_equivalent_radius(self):
        r"""
        The area equivalent radius of the ellipsoid.
        Definition: :math:`R_2 = \sqrt{A / (4 \pi)}`.
        Units: :math:`m`.
        """
        return np.sqrt(self.area / (4 * np.pi))

    @property
    def mass(self):
        r"""
        The mass of the ellipsoid.
        Definition: :math:`M = GM / G`.
        Units: :math:`kg`.
        """
        return self.geocentric_grav_const / G

    @property
    def mean_density(self):
        r"""
        The mean density of the ellipsoid.
        Definition: :math:`\rho = M / V`.
        Units: :math:`kg / m^3`.
        """
        return self.mass / self.volume

    @property
    def volume_equivalent_radius(self):
        r"""
        The volume equivalent radius of the ellipsoid.
        Definition: :math:`R_3 = \left(\dfrac{3}{4 \pi} V \right)^{1/3}`.
        Units: :math:`m`.
        """
        return (self.volume * 3 / (4 * np.pi)) ** (1 / 3)

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
            self.geocentric_grav_const * (1 + self._emm * aux) / self.semimajor_axis**2
        )
        return result

    def __str__(self):
        s = self.name + " - " + self.long_name + "\n"
        s += "Oblate ellipsoid:\n"
        s += f"  • Semimajor axis: {self.semimajor_axis} m\n"
        s += f"  • Flattening: {self.flattening}\n"
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
        return self.semimajor_axis / np.sqrt(1 - self.first_eccentricity**2 * sinlat**2)

    def geodetic_to_spherical(self, coordinates):
        """
        Convert from geodetic to geocentric spherical coordinates.

        The geodetic datum is defined by this ellipsoid. The coordinates are
        converted following [Vermeille2002]_.

        Parameters
        ----------
        coordinates : tuple = (longitude, latitude_geodetic, height)
            Longitude, latitude, and geometric height coordinates of the points
            in a geodetic coordinate system. Each element can be a single
            number or an array. The shape of the arrays must be compatible.
            Longitude and latitude must be in degrees and height in meters.
            Since longitude is not affected by conversions, it can be assigned
            ``None``.

        Returns
        -------
        converted_coordinates : tuple = (longitude, latitude_spherical, radius)
            The converted longitude, geocentric spherical latitude, and radius
            in a geocentric spherical coordinate system. The shape of each
            element will be compatible with the shape of the inputs. If the
            input longitude is ``None``, the output will also be ``None``.
            Longitude and latitude will be in degrees and radius in meters.
        """
        longitude, latitude, height = coordinates
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

    def spherical_to_geodetic(self, coordinates):
        """
        Convert from geocentric spherical to geodetic coordinates.

        The geodetic datum is defined by this ellipsoid. The coordinates are
        converted following [Vermeille2002]_.

        Parameters
        ----------
        coordinates : tuple = (longitude, latitude_spherical, height)
            Longitude, latitude, and radius coordinates of the points in
            a geocentric spherical coordinate system. Each element can be
            a single number or an array. The shape of the arrays must be
            compatible. Longitude and latitude must be in degrees and radius in
            meters. Since longitude is not affected by conversions, it can be
            assigned ``None``.

        Returns
        -------
        converted_coordinates : tuple = (longitude, latitude_geodetic, height)
            The converted longitude, geodetic latitude, and geometric height in
            a geodetic coordinate system. The shape of each element will be
            compatible with the shape of the inputs. If the input longitude is
            ``None``, the output will also be ``None``. Longitude and latitude
            will be in degrees and height in meters.
        """
        longitude, spherical_latitude, radius = coordinates
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

    def geodetic_to_ellipsoidal_harmonic(self, coordinates):
        """
        Convert from geodetic to ellipsoidal harmonic coordinates.

        The geodetic datum is defined by this ellipsoid, and the coordinates
        are converted following [Lakshmanan1991]_ and [LiGotze2001]_.

        Parameters
        ----------
        coordinates : tuple = (longitude, latitude_geodetic, height)
            Longitude, latitude, and geometric height coordinates of the points
            in a geodetic coordinate system. Each element can be a single
            number or an array. The shape of the arrays must be compatible.
            Longitude and latitude must be in degrees and height in meters.
            Since longitude is not affected by conversions, it can be assigned
            ``None``.

        Returns
        -------
        converted_coordinates : tuple = (longitude, latitude_reduced, u)
            The converted longitude, reduced (or parametric) latitude, and the
            coordinate u (the semiminor axis of the ellipsoid that passes
            through the input coordinates) in a ellipsoidal harmonic coordinate
            system. The shape of each element will be compatible with the shape
            of the inputs. If the input longitude is ``None``, the output will
            also be ``None``. Longitude and latitude will be in degrees and
            u in meters.
        """
        longitude, latitude, height = coordinates
        if (np.array(height) == 0).all():
            # Use simple formula that relates geodetic and reduced latitude
            beta = np.degrees(
                np.arctan(
                    self.semiminor_axis
                    / self.semimajor_axis
                    * np.tan(np.radians(latitude))
                )
            )
            u = np.full_like(height, fill_value=self.semiminor_axis, dtype=np.float64)

            return longitude, beta, u

        # The variable names follow Li and Goetze (2001). The prime terms
        # (*_p) refer to quantities on an ellipsoid passing through the
        # computation point.
        sinlat = np.sin(np.radians(latitude))
        coslat = np.sqrt(1 - sinlat**2)
        big_e2 = self.linear_eccentricity**2

        # Reduced latitude of the projection of the point on the
        # reference ellipsoid
        beta = np.arctan2(self.semiminor_axis * sinlat, self.semimajor_axis * coslat)
        sinbeta = np.sin(beta)
        cosbeta = np.sqrt(1 - sinbeta**2)

        # Distance squared between computation point and equatorial plane
        z_p2 = (self.semiminor_axis * sinbeta + height * sinlat) ** 2
        # Distance squared between computation point and spin axis
        r_p2 = (self.semimajor_axis * cosbeta + height * coslat) ** 2

        # Auxiliary variables
        big_d = (r_p2 - z_p2) / big_e2
        big_r = (r_p2 + z_p2) / big_e2

        # cos(reduced latitude) squared of the computation point
        cosbeta_p2 = 0.5 + big_r / 2 - np.sqrt(0.25 + big_r**2 / 4 - big_d / 2)

        # Semiminor axis of the ellipsoid passing through the computation
        # point. This is the coordinate u
        b_p = np.sqrt(r_p2 + z_p2 - big_e2 * cosbeta_p2)

        # Note that the sign of beta_p needs to be fixed as it is defined
        # from -90 to 90 degrees, but arccos is from 0 to 180.
        beta_p = np.copysign(np.degrees(np.arccos(np.sqrt(cosbeta_p2))), latitude)

        return longitude, beta_p, b_p

    def ellipsoidal_harmonic_to_geodetic(self, coordinates):
        """
        Convert from ellipsoidal-harmonic coordinates to geodetic coordinates.

        The geodetic datum is defined by this ellipsoid.

        Parameters
        ----------
        coordinates : tuple = (longitude, latitude_reduced, u)
            Longitude, reduced (or parametric) latitude, and u (the semiminor
            axis of the ellipsoid that passes through the input coordinates)
            coordinates of the points in a ellipsoidal harmonic coordinate
            system. Each element can be a single number or an array. The shape
            of the arrays must be compatible. Longitude and latitude must be in
            degrees and u in meters. Since longitude is not affected by
            conversions, it can be assigned ``None``.

        Returns
        -------
        converted_coordinates : tuple = (longitude, latitude_geodetic, height)
            The converted longitude, geodetic latitude, and geometric height in
            a geodetic coordinate system. The shape of each element will be
            compatible with the shape of the inputs. If the input longitude is
            ``None``, the output will also be ``None``. Longitude and latitude
            will be in degrees and height in meters.
        """
        longitude, reduced_latitude, u = coordinates
        # Semimajor axis of the ellipsoid that passes through the input
        # coordinates
        a_p = np.sqrt(u**2 + self.linear_eccentricity**2)

        # geodetic latitude
        latitude = np.arctan(a_p / u * np.tan(np.radians(reduced_latitude)))

        # Compute height as the difference of the prime_vertical_radius of the
        # input ellipsoid and reference ellipsoid
        height = self.prime_vertical_radius(np.sin(latitude)) * (
            a_p / self.semimajor_axis - 1
        )

        return longitude, np.degrees(latitude), height

    def normal_gravity(self, coordinates, si_units=False):
        r"""
        Normal gravity of the ellipsoid.

        Computes the magnitude of the gradient of the :term:`gravity potential`
        generated by this ellipsoid at **any point outside the ellipsoid**.
        Based on the closed-form expressions by [Lakshmanan1991]_ and corrected
        by [LiGotze2001]_. This means that the **free-air correction is not
        necessary** to calculate normal gravity at the observation points.

        .. caution::

            These expressions are only valid for heights on or above the
            surface of the ellipsoid.

        Parameters
        ----------
        coordinates : tuple = (longitude, latitude_geodetic, height)
            Longitude, latitude, and geometric height coordinates of the
            computation points in a geodetic coordinate system. Each element
            can be a single number or an array. The shape of the arrays must be
            compatible. Longitude and latitude must be in degrees and height in
            meters. Since longitude is not used in computations (the field is
            symmetric with longitude), it can be assigned ``None``.
        si_units : bool
            Return the value in mGal (False, default) or m/s² (True)

        Returns
        -------
        gamma : float or array
            The normal gravity in mGal or m/s².

        Notes
        -----
        :term:`Normal gravity` is defined as the magnitude of the gradient of
        the gravity potential generated by a :term:`reference ellipsoid` at the
        given geodetic latitude :math:`\phi` and height above the ellipsoid
        :math:`h` (geometric height).

        .. math::

            \gamma(\phi, h) = \|\vec{\nabla}U(\phi, h)\|

        in which :math:`U = V + \Phi` is the gravity potential of the
        ellipsoid, :math:`V` is the gravitational potential of the ellipsoid,
        and :math:`\Phi` is the centrifugal potential.

        The equations used here assume that the internal density distribution
        of the ellipsoid is such that the gravity potential is constant at its
        surface. The specific internal density distribution is undefined.
        """
        # Warn if height is negative
        if np.any(coordinates[2] < 0):
            warn(
                "Formulas used are valid for points outside the ellipsoid."
                "Height must be greater than or equal to zero."
            )

        # Convert geodetic latitude and height to ellipsoidal-harmonic coords
        longitude, beta, u = self.geodetic_to_ellipsoidal_harmonic(coordinates)
        sinbeta2 = np.sin(np.radians(beta)) ** 2
        cosbeta2 = 1 - sinbeta2
        big_e = self.linear_eccentricity

        # Compute the auxiliary functions q and q_0 (eq 2-113 of
        # HofmannWellenhofMoritz2006)
        q_0 = 0.5 * (
            (1 + 3 * (self.semiminor_axis / big_e) ** 2)
            * np.arctan2(big_e, self.semiminor_axis)
            - 3 * self.semiminor_axis / big_e
        )
        q_p = 3 * (1 + (u / big_e) ** 2) * (1 - u / big_e * np.arctan2(big_e, u)) - 1
        big_w = np.sqrt((u**2 + big_e**2 * sinbeta2) / (u**2 + big_e**2))

        # Put together gamma using 3 separate terms
        term1 = self.geocentric_grav_const / (u**2 + big_e**2)
        term2 = (0.5 * sinbeta2 - 1 / 6) * (
            self.semimajor_axis**2
            * big_e
            * q_p
            * self.angular_velocity**2
            / ((u**2 + big_e**2) * q_0)
        )
        term3 = -cosbeta2 * u * self.angular_velocity**2
        gamma = (term1 + term2 + term3) / big_w

        # Convert gamma from SI to mGal
        if not si_units:
            gamma *= 1e5

        return gamma

    def normal_gravitational_potential(self, coordinates):
        r"""
        Normal gravitational potential of the ellipsoid.

        Computes the gravitational potential generated by the ellipsoid at the
        given geodetic latitude :math:`\phi` and height above the ellipsoid
        :math:`h` (geometric height).

        .. math::

            V(\beta, u) = \dfrac{GM}{E} \arctan{\dfrac{E}{u}} + \dfrac{1}{3}
            \omega^2 a^2 \dfrac{q}{q_0} P_2 (\sin \beta)

        in which :math:`V` is the gravitational potential of the
        ellipsoid (no centrifugal term), :math:`GM` is the geocentric
        gravitational constant, :math:`E` is the linear eccentricity,
        :math:`\omega` is the angular rotation rate, :math:`q` and :math:`q_0`
        are auxiliary functions, :math:`P_2` is the degree 2 unnormalized
        Legendre Polynomial, and :math:`u` and :math:`\beta` are
        ellipsoidal-harmonic coordinates corresponding to the input geodetic
        latitude and ellipsoidal height. See eq. 2-124 of
        [HofmannWellenhofMoritz2006]_.

        Assumes that the internal density distribution of the ellipsoid is such
        that the gravity potential is constant at its surface.

        .. caution::

            These expressions are only valid for heights on or above the
            surface of the ellipsoid.

        Parameters
        ----------
        latitude : float or array
            The geodetic latitude where the normal gravitational potential will
            be computed (in degrees).
        height : float or array
            The ellipsoidal (geometric) height of the computation the point (in
            meters).

        Returns
        -------
        V : float or array
            The normal gravitational potential in m²/s².

        """
        # Warn if height is negative
        if np.any(height < 0):
            warn(
                "Formulas used are valid for points outside the ellipsoid."
                "Height must be greater than or equal to zero."
            )

        # Convert geodetic latitude and height to ellipsoidal-harmonic coords
        longitude, beta, u = self.geodetic_to_ellipsoidal_harmonic(
            None, latitude, height
        )
        big_e = self.linear_eccentricity

        # Compute the auxiliary functions q and q_0 (eq 2-113 of
        # HofmannWellenhofMoritz2006)
        q_0 = 0.5 * (
            (1 + 3 * (self.semiminor_axis / big_e) ** 2)
            * np.arctan2(big_e, self.semiminor_axis)
            - 3 * self.semiminor_axis / big_e
        )
        q = 0.5 * ((1 + 3 * (u / big_e) ** 2) * np.arctan2(big_e, u) - 3 * u / big_e)

        big_v = self.geocentric_grav_const / big_e * np.arctan(big_e / u) + (1 / 3) * (
            self.angular_velocity * self.semimajor_axis
        ) ** 2 * q / q_0 * (1.5 * np.sin(np.radians(beta)) ** 2 - 0.5)

        return big_v

    def normal_gravity_potential(self, latitude, height):
        r"""
        Normal gravity potential of the ellipsoid at the given latitude and
        height.

        Computes the gravity potential generated by the ellipsoid at the
        given geodetic latitude :math:`\phi` and height above the ellipsoid
        :math:`h` (geometric height).

        .. math::

            U(\beta, u) = \dfrac{GM}{E} \arctan{\dfrac{E}{u}} + \dfrac{1}{2}
            \omega^2 a^2 \dfrac{q}{q_0} \left(\sin^2 \beta
            - \dfrac{1}{3}\right) + \dfrac{1}{2} \omega^2 \left(u^2
            + E^2\right) \cos^2 \beta

        in which :math:`U` is the gravity potential of the ellipsoid,
        :math:`GM` is the geocentric gravitational constant, :math:`E` is the
        linear eccentricity, :math:`\omega` is the angular rotation rate,
        :math:`q` and :math:`q_0` are auxiliary functions, and :math:`u` and
        :math:`\beta` are ellipsoidal-harmonic coordinates corresponding to the
        input geodetic latitude and ellipsoidal height. See eq. 2-126 of
        [HofmannWellenhofMoritz2006]_.

        Assumes that the internal density distribution of the ellipsoid is such
        that the gravity potential is constant at its surface.

        .. caution::

            These expressions are only valid for heights on or above the
            surface of the ellipsoid.

        Parameters
        ----------
        latitude : float or array
            The geodetic latitude where the normal gravity potential will be
            computed (in degrees).
        height : float or array
            The ellipsoidal (geometric) height of the computation the point (in
            meters).

        Returns
        -------
        V : float or array
            The normal gravity potential in m²/s².

        """
        # Warn if height is negative
        if np.any(height < 0):
            warn(
                "Formulas used are valid for points outside the ellipsoid."
                "Height must be greater than or equal to zero."
            )

        # Convert geodetic latitude and height to ellipsoidal-harmonic coords
        longitude, beta, u = self.geodetic_to_ellipsoidal_harmonic(
            None, latitude, height
        )
        big_e = self.linear_eccentricity

        # Compute the auxiliary functions q and q_0 (eq 2-113 of
        # HofmannWellenhofMoritz2006)
        q_0 = 0.5 * (
            (1 + 3 * (self.semiminor_axis / big_e) ** 2)
            * np.arctan2(big_e, self.semiminor_axis)
            - 3 * self.semiminor_axis / big_e
        )
        q = 0.5 * ((1 + 3 * (u / big_e) ** 2) * np.arctan2(big_e, u) - 3 * u / big_e)

        big_u = (
            self.geocentric_grav_const / big_e * np.arctan(big_e / u)
            + 0.5
            * (self.angular_velocity * self.semimajor_axis) ** 2
            * q
            / q_0
            * (np.sin(np.radians(beta)) ** 2 - 1 / 3)
            + 0.5
            * self.angular_velocity**2
            * (u**2 + big_e**2)
            * np.cos(np.radians(beta)) ** 2
        )

        return big_u

    def centrifugal_potential(self, latitude, height):
        r"""
        Centrifugal potential at the given geodetic latitude and height above
        the ellipsoid.

        The centrifugal potential :math:`\Phi` at geodetic latitude
        :math:`\phi` and height above the ellipsoid :math:`h` (geometric
        height) is

        .. math::

            \Phi(\phi, h) = \dfrac{1}{2}
                \omega^2 \left(N(\phi) + h\right)^2 \cos^2(\phi)

        in which :math:`N(\phi)` is the prime vertical radius of curvature of
        the ellipsoid and :math:`\omega` is the angular velocity.

        Parameters
        ----------
        latitude : float or array
            The geodetic latitude where the centrifugal potential will be
            computed (in degrees).
        height : float or array
            The ellipsoidal (geometric) height of the computation point (in
            meters).

        Returns
        -------
        Phi : float or array
            The centrifugal potential in m²/s².

        """
        # Pre-compute to avoid repeated calculations
        sinlat = np.sin(np.radians(latitude))
        coslat = np.sqrt(1 - sinlat**2)

        return (1 / 2) * (
            self.angular_velocity
            * (self.prime_vertical_radius(sinlat) + height)
            * coslat
        ) ** 2
