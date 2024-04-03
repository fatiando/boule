# Copyright (c) 2019 The Boule Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Define a reference triaxial ellipsoid.
"""
from warnings import warn

import attr
import numpy as np


# Don't let ellipsoid parameters be changed to avoid messing up calculations
# accidentally.
@attr.s(frozen=True)
class TriaxialEllipsoid:
    r"""
    A rotating triaxial ellipsoid.

    The ellipsoid is defined by five parameters: semimajor axis, semimedium
    axis, semiminor axis, geocentric gravitational constant, and angular
    velocity The thee semi-axis are different and the ellipsoid spins around
    it's largest moment of inertia.

    **This class is read-only:** Input parameters and attributes cannot be
    changed after instantiation.

    **Units:** All input parameters and derived attributes are in SI units.

    .. attention::

        Gravity calculations have not been implemented yet for triaxial
        ellipsoids. If you're interested in this feature or would like to help
        implement it, please
        `get in touch <https://www.fatiando.org/contact>`__.

    Parameters
    ----------
    name : str
        A short name for the ellipsoid, for example ``"WGS84"``.
    semimajor_axis : float
        The semimajor (largest) axis of the ellipsoid.
        Definition: :math:`a`.
        Units: :math:`m`.
    semimedium_axis : float
        The semimedium (middle) axis of the ellipsoid.
        Definition: :math:`b`.
        Units: :math:`m`.
    semiminor_axis : float
        The semiminor (smallest) axis of the ellipsoid.
        Definition: :math:`c`.
        Units: :math:`m`.
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

    Examples
    --------

    We can define an ellipsoid by setting the 5 key numerical parameters:

    >>> ellipsoid = TriaxialEllipsoid(
    ...     name="VESTA",
    ...     long_name="Vesta Triaxial Ellipsoid",
    ...     semimajor_axis=286_300,
    ...     semimedium_axis=278_600,
    ...     semiminor_axis=223_200,
    ...     geocentric_grav_const=1.729094e10,
    ...     angular_velocity=326.71050958367e-6,
    ...     reference=(
    ...         "Russell, C. T., Raymond, C. A., Coradini, A., McSween, "
    ...         "H. Y., Zuber, M. T., Nathues, A., et al. (2012). Dawn at "
    ...         "Vesta: Testing the Protoplanetary Paradigm. Science. "
    ...         "doi:10.1126/science.1219381"
    ...     ),
    ... )
    >>> print(ellipsoid) # doctest: +ELLIPSIS
    TriaxialEllipsoid(name='VESTA', ...)
    >>> print(ellipsoid.long_name)
    Vesta Triaxial Ellipsoid

    The class then defines several derived attributes based on the input
    parameters:

    >>> print(f"{ellipsoid.mean_radius:.0f} m")
    262700 m
    >>> print(f"{ellipsoid.volume * 1e-9:.0f} km³")
    74573626 km³

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
        "Raise a ValueError informing that the axis are invalid."
        raise ValueError(
            "Invalid triaxial ellipsoid axis: "
            f"major={self.semimajor_axis} "
            f"medium={self.semimedium_axis} "
            f"minor={self.semiminor_axis}. "
            "Must be major > medium > minor."
        )

    @semimajor_axis.validator
    def _check_semimajor_axis(self, semimajor_axis, value):
        """
        Check if semimajor_axis is positive and is the largest of the axis.
        """
        if not value > 0:
            raise ValueError(
                f"Invalid semi-major axis '{value}'. Should be greater than zero."
            )
        if self.semimedium_axis > value:
            self._raise_invalid_axis()

    @semimedium_axis.validator
    def _check_semimedium_axis(self, semimedium_axis, value):
        """
        Check if semimedium_axis is positive and larger than semi-minor axis.
        """
        if not value > 0:
            raise ValueError(
                f"Invalid semi-medium axis '{value}'. Should be greater than zero."
            )
        if self.semiminor_axis > value:
            self._raise_invalid_axis()

    @semiminor_axis.validator
    def _check_semiminor_axis(self, semiminor_axis, value):
        "Check if semiminor_axis is positive."
        if not value > 0:
            raise ValueError(
                f"Invalid semi-minor axis '{value}'. Should be greater than zero."
            )
        # Don't need to check here because if the two checks for major and
        # medium pass it means that this is the smallest.

    @geocentric_grav_const.validator
    def _check_geocentric_grav_const(self, geocentric_grav_const, value):
        "Warn if geocentric_grav_const is negative."
        if value < 0:
            warn(f"The geocentric gravitational constant is negative: '{value}'")

    @property
    def mean_radius(self):
        r"""
        The arithmetic mean radius of the ellipsoid.
        Definition: :math:`R = \dfrac{a + b + c}{3}`.
        Units: :math:`m`.
        """
        return (self.semimajor_axis + self.semimedium_axis + self.semiminor_axis) / 3

    @property
    def volume(self):
        r"""
        The volume bounded by the ellipsoid.
        Definition: :math:`V = \dfrac{4}{3} \pi a b c`.
        Units: :math:`m^3`.
        """
        return (
            (4 / 3 * np.pi)
            * self.semimajor_axis
            * self.semimedium_axis
            * self.semiminor_axis
        )

    @property
    def equatorial_flattening(self):
        r"""
        The equatorial flattening of the ellipsoid.
        Definition: :math:`f_b = \frac{a - b}{a}`.
        Units: adimensional.
        """
        return (self.semimajor_axis - self.semimedium_axis) / self.semimajor_axis

    @property
    def meridional_flattening(self):
        r"""
        The meridional flattening of the ellipsoid in the meridian plane
        containing the semi-major axis.
        Definition: :math:`f_c = \frac{a - c}{a}`.
        Units: adimensional.
        """
        return (self.semimajor_axis - self.semiminor_axis) / self.semimajor_axis

    def geocentric_radius(self, longitude, latitude, longitude_semimajor_axis=0.0):
        r"""
        Radial distance from the center of the ellipsoid to its surface.

        Assumes geocentric spherical latitude and geocentric spherical
        longitudes. The geocentric radius is calculated following [Pec1983]_.

        Parameters
        ----------
        longitude : float or array
            Longitude coordinates on spherical coordinate system in degrees.
        latitude : float or array
            Latitude coordinates on spherical coordinate system in degrees.
        longitude_semimajor_axis : float (optional)
            Longitude coordinate of the meridian containing the semi-major axis
            on spherical coordinate system in degrees. Optional, default value
            is 0.0.

        Returns
        -------
        geocentric_radius : float or array
            The geocentric radius for the given spherical latitude(s) and
            spherical longitude(s) in the same units as the axes of the
            ellipsoid.


        .. tip::

            No elevation is taken into account.

        Notes
        -----

        Given geocentric spherical latitude :math:`\phi` and geocentric
        spherical longitude :math:`\lambda`, the geocentric surface radius
        :math:`R` is computed as (see Eq. 1 of [Pec1983]_)

        .. math::

            R(\phi, \lambda) =
            \frac{
                a \, (1 - f_c) \, (1 - f_b)
            }{
                \sqrt{
                    1
                    - (2 f_c - f_c^2) \cos^2 \phi
                    - (2 f_b - f_b^2) \sin^2 \phi
                    - (1 - f_c)^2 (2 f_b - f_b^2)
                        \cos^2 \phi \cos^2 (\lambda - \lambda_a)
                }
            },

        where :math:`f_c` is the meridional flattening

        .. math::

            f_c = \frac{a - c}{a},

        :math:`f_b` is the equatorial flattening

        .. math::

            f_b = \frac{a - b}{a},

        with :math:`a`, :math:`b` and :math:`c` being the semi-major,
        semi-medium and semi-minor axes of the ellipsoid, and :math:`\lambda_a`
        being the geocentric spherical longitude of the meridian containing the
        semi-major axis.

        Note that [Pěč1983]_ use geocentric spherical co-latitude, while here
        we used geocentric spherical latitude.
        """
        latitude_rad = np.radians(latitude)
        longitude_rad = np.radians(longitude)
        longitude_semimajor_axis_rad = np.radians(longitude_semimajor_axis)

        coslat, sinlat = np.cos(latitude_rad), np.sin(latitude_rad)

        fc = self.meridional_flattening
        fb = self.equatorial_flattening

        radius = (self.semimajor_axis * (1.0 - fc) * (1.0 - fb)) / np.sqrt(
            1.0
            - (2.0 * fc - fc**2) * coslat**2
            - (2.0 * fb - fb**2) * sinlat**2
            - (1.0 - fc) ** 2
            * (2.0 * fb - fb**2)
            * coslat**2
            * np.cos(longitude_rad - longitude_semimajor_axis_rad) ** 2
        )
        return radius
