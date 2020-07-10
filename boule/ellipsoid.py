"""
Module for defining and setting the reference ellipsoid.
"""
import attr
import numpy as np


# Don't let ellipsoid parameters be changed to avoid messing up calculations
# accidentally.
@attr.s(frozen=True)
class Ellipsoid:
    """
    Reference oblate ellipsoid.

    The ellipsoid is oblate and spins around it's minor axis. It is defined by
    four parameters and offers other derived quantities as read-only
    properties. In fact, all attributes of this class are read-only and cannot
    be changed after instantiation.

    All ellipsoid parameters are in SI units.

    Parameters
    ----------
    name : str
        A short name for the ellipsoid, for example ``'WGS84'``.
    semimajor_axis : float
        The semi-major axis of the ellipsoid (equatorial radius), usually
        represented by "a" [meters].
    flattening : float
        The flattening of the ellipsoid (f) [adimensional].
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

    We can define a reference unit sphere by using 0 as the flattening:

    >>> sphere = Ellipsoid(
    ...     name="sphere",
    ...     long_name="Unit sphere",
    ...     semimajor_axis=1,
    ...     flattening=0,
    ...     geocentric_grav_const=1,
    ...     angular_velocity=0
    ... )
    >>> print(sphere) # doctest: +ELLIPSIS
    Ellipsoid(name='sphere', ...)
    >>> print(sphere.long_name)
    Unit sphere
    >>> print("{:.2f}".format(sphere.semiminor_axis))
    1.00
    >>> print("{:.2f}".format(sphere.mean_radius))
    1.00
    >>> print("{:.2f}".format(sphere.linear_eccentricity))
    0.00
    >>> print("{:.2f}".format(sphere.first_eccentricity))
    0.00
    >>> print("{:.2f}".format(sphere.second_eccentricity))
    0.00

    """

    name = attr.ib()
    semimajor_axis = attr.ib()
    flattening = attr.ib()
    geocentric_grav_const = attr.ib()
    angular_velocity = attr.ib()
    long_name = attr.ib(default=None)
    reference = attr.ib(default=None)

    @property
    def semiminor_axis(self):
        "The small (polar) axis of the ellipsoid [meters]"
        return self.semimajor_axis * (1 - self.flattening)

    @property
    def linear_eccentricity(self):
        "The linear eccentricity [meters]"
        return np.sqrt(self.semimajor_axis ** 2 - self.semiminor_axis ** 2)

    @property
    def first_eccentricity(self):
        "The first eccentricity [adimensional]"
        return self.linear_eccentricity / self.semimajor_axis

    @property
    def second_eccentricity(self):
        "The second eccentricity [adimensional]"
        return self.linear_eccentricity / self.semiminor_axis

    @property
    def mean_radius(self):
        """
        The arithmetic mean radius [meters]

        :math:`R_1 = (2a + b) /3` [Moritz2000]_
        """
        return 1 / 3 * (2 * self.semimajor_axis + self.semiminor_axis)

    @property
    def emm(self):
        r"Auxiliary quantity :math:`m = \omega^2 a^2 b / (GM)`"
        return (
            self.angular_velocity ** 2
            * self.semimajor_axis ** 2
            * self.semiminor_axis
            / self.geocentric_grav_const
        )

    @property
    def gravity_equator(self):
        """
        The norm of the gravity vector at the equator on the ellipsoid [m/s^2]
        """
        ratio = self.semiminor_axis / self.linear_eccentricity
        arctan = np.arctan2(self.linear_eccentricity, self.semiminor_axis)
        aux = (
            self.second_eccentricity
            * (3 * (1 + ratio ** 2) * (1 - ratio * arctan) - 1)
            / (3 * ((1 + 3 * ratio ** 2) * arctan - 3 * ratio))
        )
        axis_mul = self.semimajor_axis * self.semiminor_axis
        result = self.geocentric_grav_const * (1 - self.emm - self.emm * aux) / axis_mul
        return result

    @property
    def gravity_pole(self):
        "The norm of the gravity vector at the poles on the ellipsoid [m/s^2]"
        ratio = self.semiminor_axis / self.linear_eccentricity
        arctan = np.arctan2(self.linear_eccentricity, self.semiminor_axis)
        aux = (
            self.second_eccentricity
            * (3 * (1 + ratio ** 2) * (1 - ratio * arctan) - 1)
            / (1.5 * ((1 + 3 * ratio ** 2) * arctan - 3 * ratio))
        )
        result = (
            self.geocentric_grav_const * (1 + self.emm * aux) / self.semimajor_axis ** 2
        )
        return result

    def geocentric_radius(self, latitude, geodetic=True):
        r"""
        Distance from the center of the ellipsoid to its surface.

        The geocentric radius and is a function of the geodetic latitude
        :math:`\phi` and the semi-major and semi-minor axis, a and b:

        .. math::

            R(\phi) = \sqrt{\dfrac{
                (a^2\cos\phi)^2 + (b^2\sin\phi)^2}{
                (a\cos\phi)^2 + (b\sin\phi)^2 }
            }

        See https://en.wikipedia.org/wiki/Earth_radius#Geocentric_radius

        The same could be achieved with
        :meth:`boule.Ellipsoid.geodetic_to_spherical` by passing any value for
        the longitudes and heights equal to zero. This method provides a
        simpler and possibly faster alternative.

        Alternatively, the geocentric radius can also be expressed in terms of
        the geocentric (spherical) latitude :math:`\theta`:

        .. math::

            R(\theta) = \sqrt{\dfrac{1}{
                (\frac{\cos\theta}{a})^2 + (\frac{\sin\theta}{b})^2 }
            }

        This can be useful if you already have the geocentric latitudes and
        need the geocentric radius of the ellipsoid (for example, in spherical
        harmonic analysis). In these cases, the coordinate conversion route is
        not possible since we need a radius to do that in the first place.

        Boule generally tries to avoid doing coordinate conversions inside
        functions in favour of the user handling the conversions prior to
        input. This simplifies the code and makes sure that users know
        precisely which conversions are taking place. This method is an
        exception since a coordinate conversion route would not be possible.

        .. note::

            No elevation is taken into account (the height is zero). If you
            need the geocentric radius at a height other than zero, use
            :meth:`boule.Ellipsoid.geodetic_to_spherical` instead.

        Parameters
        ----------
        latitude : float or array
            Latitude coordinates on geodetic coordinate system in degrees.
        geodetic : bool
            If True (default), will assume that latitudes are geodetic
            latitudes. Otherwise, will that they are geocentric spherical
            latitudes.

        Returns
        -------
        geocentric_radius : float or array
            The geocentric radius for the given latitude(s) in the same units
            as the ellipsoid axis.

        """
        latitude_rad = np.radians(latitude)
        coslat, sinlat = np.cos(latitude_rad), np.sin(latitude_rad)
        # Avoid doing this in favour of having the user do the conversions when
        # possible. It's not the case here, so we made an exception.
        if geodetic:
            radius = np.sqrt(
                (
                    (self.semimajor_axis ** 2 * coslat) ** 2
                    + (self.semiminor_axis ** 2 * sinlat) ** 2
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
        Calculate the prime vertical radius for a given geodetic latitude

        The prime vertical radius is defined as:

        .. math::

            N(\phi) = \frac{a}{\sqrt{1 - e^2 \sin^2(\phi)}}

        Where :math:`a` is the semimajor axis and :math:`e` is the first
        eccentricity.

        This function receives the sine of the latitude as input to avoid
        repeated computations of trigonometric functions.

        Parameters
        ----------
        sinlat : float or array-like
            Sine of the latitude angle.

        Returns
        -------
        prime_vertical_radius : float or array-like
            Prime vertical radius given in the same units as the semimajor axis

        """
        return self.semimajor_axis / np.sqrt(
            1 - self.first_eccentricity ** 2 * sinlat ** 2
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
        latitude_rad = np.radians(latitude)
        coslat, sinlat = np.cos(latitude_rad), np.sin(latitude_rad)
        prime_vertical_radius = self.prime_vertical_radius(sinlat)
        # Instead of computing X and Y, we only compute the projection on the
        # XY plane: xy_projection = sqrt( X**2 + Y**2 )
        xy_projection = (height + prime_vertical_radius) * coslat
        z_cartesian = (
            height + (1 - self.first_eccentricity ** 2) * prime_vertical_radius
        ) * sinlat
        radius = np.sqrt(xy_projection ** 2 + z_cartesian ** 2)
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
        spherical_latitude = np.radians(spherical_latitude)
        k, big_z, big_d = self._spherical_to_geodetic_terms(spherical_latitude, radius)
        latitude = np.degrees(
            2 * np.arctan(big_z / (big_d + np.sqrt(big_d ** 2 + big_z ** 2)))
        )
        height = (
            (k + self.first_eccentricity ** 2 - 1)
            / k
            * np.sqrt(big_d ** 2 + big_z ** 2)
        )
        return longitude, latitude, height

    def _spherical_to_geodetic_terms(self, spherical_latitude, radius):
        "Calculate intermediate terms needed for the conversion."
        # Offload computation of these intermediate variables here to clean up
        # the main function body
        cos_latitude = np.cos(spherical_latitude)
        big_z = radius * np.sin(spherical_latitude)
        p_0 = radius ** 2 * cos_latitude ** 2 / self.semimajor_axis ** 2
        q_0 = (1 - self.first_eccentricity ** 2) / self.semimajor_axis ** 2 * big_z ** 2
        r_0 = (p_0 + q_0 - self.first_eccentricity ** 4) / 6
        s_0 = self.first_eccentricity ** 4 * p_0 * q_0 / 4 / r_0 ** 3
        t_0 = np.cbrt(1 + s_0 + np.sqrt(2 * s_0 + s_0 ** 2))
        u_0 = r_0 * (1 + t_0 + 1 / t_0)
        v_0 = np.sqrt(u_0 ** 2 + q_0 * self.first_eccentricity ** 4)
        w_0 = self.first_eccentricity ** 2 * (u_0 + v_0 - q_0) / 2 / v_0
        k = np.sqrt(u_0 + v_0 + w_0 ** 2) - w_0
        big_d = k * radius * cos_latitude / (k + self.first_eccentricity ** 2)
        return k, big_z, big_d

    def normal_gravity(self, latitude, height):
        """
        Calculate normal gravity at any latitude and height.

        Computes the magnitude of the gradient of the gravity potential
        (gravitational + centrifugal) generated by the ellipsoid at the given
        latitude and (geometric) height. Uses of a closed form expression of
        [LiGotze2001]_.

        Parameters
        ----------
        latitude : float or array
            The (geodetic) latitude where the normal gravity will be computed
            (in degrees).
        height : float or array
            The ellipsoidal (geometric) height of computation point (in meters).

        Returns
        -------
        gamma : float or array
            The normal gravity in mGal.

        """
        sinlat = np.sin(np.deg2rad(latitude))
        coslat = np.sqrt(1 - sinlat ** 2)
        # The terms below follow the variable names from Li and Goetze (2001)
        cosbeta_l2, sinbeta_l2, b_l, q_0, q_l, big_w = self._normal_gravity_terms(
            sinlat, coslat, height
        )
        # Put together gamma using 3 terms
        term1 = self.geocentric_grav_const / (b_l ** 2 + self.linear_eccentricity ** 2)
        term2 = (0.5 * sinbeta_l2 - 1 / 6) * (
            self.semimajor_axis ** 2
            * self.linear_eccentricity
            * q_l
            * self.angular_velocity ** 2
            / ((b_l ** 2 + self.linear_eccentricity ** 2) * q_0)
        )
        term3 = -cosbeta_l2 * b_l * self.angular_velocity ** 2
        gamma = (term1 + term2 + term3) / big_w
        # Convert gamma from SI to mGal
        return gamma * 1e5

    def _normal_gravity_terms(self, sinlat, coslat, height):
        "Calculate intermediate terms needed for the calculations."
        # Offload computation of these intermediate variables here to clean up
        # the main function body
        beta = np.arctan2(self.semiminor_axis * sinlat, self.semimajor_axis * coslat)
        zl2 = (self.semiminor_axis * np.sin(beta) + height * sinlat) ** 2
        rl2 = (self.semimajor_axis * np.cos(beta) + height * coslat) ** 2
        big_d = (rl2 - zl2) / self.linear_eccentricity ** 2
        big_r = (rl2 + zl2) / self.linear_eccentricity ** 2
        cosbeta_l2 = 0.5 * (1 + big_r) - np.sqrt(0.25 * (1 + big_r ** 2) - 0.5 * big_d)
        sinbeta_l2 = 1 - cosbeta_l2
        b_l = np.sqrt(rl2 + zl2 - self.linear_eccentricity ** 2 * cosbeta_l2)
        q_0 = 0.5 * (
            (1 + 3 * (self.semiminor_axis / self.linear_eccentricity) ** 2)
            * np.arctan2(self.linear_eccentricity, self.semiminor_axis)
            - 3 * self.semiminor_axis / self.linear_eccentricity
        )
        q_l = (
            3
            * (1 + (b_l / self.linear_eccentricity) ** 2)
            * (
                1
                - b_l
                / self.linear_eccentricity
                * np.arctan2(self.linear_eccentricity, b_l)
            )
            - 1
        )
        big_w = np.sqrt(
            (b_l ** 2 + self.linear_eccentricity ** 2 * sinbeta_l2)
            / (b_l ** 2 + self.linear_eccentricity ** 2)
        )
        return cosbeta_l2, sinbeta_l2, b_l, q_0, q_l, big_w
