# Copyright (c) 2019 The Boule Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Representation of an oblate ellipsoid with homogeneous density.
"""

import textwrap

import attr
import numpy as np

from ._constants import G
from ._ellipsoid import (
    Centrifugal,
    CoordinateConversion,
    GeometricProperties,
    check_coordinate_system,
    to_cartesian,
    validate_flattening,
    validate_semimajor_axis,
)


@attr.s(frozen=True)
class HomogeneousEllipsoid(GeometricProperties, CoordinateConversion, Centrifugal):
    r"""
    A rotating oblate ellipsoid with homogeneous density.

    The ellipsoid is defined by four parameters: semimajor axis, flattening,
    density, and angular velocity. It spins around     its semiminor axis and
    **does not have** constant gravity potential at its surface (unlike the
    :class:`boule.Ellipsoid`).

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
    density : float
        The density of the ellipsoid, considered constant throughout its volume.
        Definition: :math:`\rho`. Units:
        :math:`kg.m^{-3}`.
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

        Use :class:`boule.Sphere` if you desire zero flattening. The sphere also
        has homogeneous density and gravity computations will likely be faster.

    Examples
    --------
    We can define an ellipsoid by setting the 4 key numerical parameters and
    some metadata about where they came from:

    >>> ellipsoid = HomogeneousEllipsoid(
    ...     name="Earth",
    ...     long_name="Constant density Earth model",
    ...     semimajor_axis=6378137,
    ...     flattening=1 / 298.257223563,
    ...     density=5513.41223873,
    ...     angular_velocity=7292115e-11,
    ...     reference="Hofmann-Wellenhof & Moritz (2006)",
    ...     comments="The geometric properties are the same as WGS84.",
    ... )
    >>> print(ellipsoid) # doctest: +ELLIPSIS
    Earth - Constant density Earth model
    Homogeneous oblate ellipsoid:
      • Semimajor axis: 6378137 m
      • Flattening: 0.0033528106647474805
      • Density: 5513.41223873 kg/m³
      • Angular velocity: 7.292115e-05 rad/s
    Source:
      Hofmann-Wellenhof & Moritz (2006)
    Comments:
      The geometric properties are the same as WGS84.

    >>> print(ellipsoid.long_name)
    Constant density Earth model

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
    >>> print(f"{ellipsoid.volume * 1e-9:.5e} km³")
    1.08321e+12 km³
    >>> print(f"{ellipsoid.area:.10e} m²")
    5.1006562172e+14 m²
    >>> print(f"{ellipsoid.area_equivalent_radius:0.4f} m")
    6371007.1809 m

    Use the class methods for calculating normal gravity and other geometric
    quantities.
    """

    name = attr.ib()
    semimajor_axis = attr.ib(validator=validate_semimajor_axis)
    flattening = attr.ib(validator=validate_flattening)
    density = attr.ib()
    angular_velocity = attr.ib()
    long_name = attr.ib(default=None)
    reference = attr.ib(default=None)
    comments = attr.ib(default=None)

    def __str__(self):
        """
        Define a string representation of this class.
        """
        s = self.name + " - " + self.long_name + "\n"
        s += "Homogeneous oblate ellipsoid:\n"
        s += f"  • Semimajor axis: {self.semimajor_axis} m\n"
        s += f"  • Flattening: {self.flattening}\n"
        s += f"  • Density: {self.density} kg/m³\n"
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

    @property
    def mass(self):
        r"""
        The mass of the ellipsoid.

        Definition: :math:`M = V \rho`, in which :math:`V` is the volume and
        :math:`\rho` if the density.

        Units: :math:`kg`.
        """
        return self.density * self.volume

    # Gravity calculations
    # ##################################################################################

    def normal_gravitation_vector(
        self, coordinates, *, coordinate_system="geodetic", si_units=False
    ):
        r"""
        Calculate the normal gravitation vector of the ellipsoid.

        Computes the gradient vector of the :term:`gravitational potential`
        generated by this ellipsoid at **any point outside the ellipsoid**.
        Based on the closed-form expressions by [Clark1986]_ and [Takahashi2017]_.

        .. caution::

            These expressions are only valid for heights on or above the
            surface of the ellipsoid.

        Parameters
        ----------
        coordinates : tuple = (coordinate1, coordinate2, coordinate3)
            Tuple with 3 arrays containing the coordinates of the computation points.
            The meaning of the arrays is determined by the ``coordinate_system``
            argument: longitude, geodetic latitude, and geometric height for a geodetic
            system; longitude, geocentric latitude, and radius for a geocentric
            spherical system; longitude, reduced latitude, and u for an ellipsoidal
            harmonic system; x, y, and z for a geocentric Cartesian system. Each
            element can be a single number or an array. The shape of the arrays must be
            compatible. Longitude and latitudes must be in degrees and height, radius,
            and u in meters. Since longitude is not used in computations (the potential
            is symmetric with longitude), it can be assigned ``None``.
        coordinate_system : str
            The coordinate system that will be assumed for the given coordinates. Should
            be one of: ``"geodetic"`` (default), ``"spherical"``, ``"cartesian"``, or
            ``"ellipsoidal harmonic"``.
        si_units : bool
            Return the value in mGal (False, default) or m/s² (True).

        Returns
        -------
        gravitation_vector : tuple = (gx, gy, gz)
            Tuple with arrays representing the 3 components of the gravitation
            vector in the geocentric Cartesian system in mGal or m/s².

        Notes
        -----
        .. note::

            Since the calculations happen in geocentric Cartesian coordinates,
            passing inputs in any other coordinate system will require
            conversion, which may slow down computations if done in a loop.
        """
        check_coordinate_system(coordinate_system)
        x, y, z = to_cartesian(coordinates, coordinate_system, self)
        # Calculates the largest root of the equation for lambda in Takahashi
        # et. al. (2017; https://doi.org/10.5194/gmd-10-3591-2017).
        p1 = self.semiminor_axis**2 + self.semimajor_axis**2 - x**2 - y**2 - z**2
        p0 = (
            self.semiminor_axis**2 * self.semimajor_axis**2
            - self.semiminor_axis**2 * np.hypot(x, y) ** 2
            - self.semimajor_axis**2 * z**2
        )
        lamb = (-p1 + np.sqrt(p1**2 - 4 * p0)) / 2
        # Terms used all the 3 components
        const = (
            2 * np.pi * G * self.density * self.semiminor_axis * self.semimajor_axis**2
        ) / np.sqrt((self.semimajor_axis**2 - self.semiminor_axis**2) ** 3)
        atan2 = np.arctan2(
            np.sqrt(self.semimajor_axis**2 - self.semiminor_axis**2),
            np.sqrt(self.semiminor_axis**2 + lamb),
        )
        horizontal_term = const * (
            np.sqrt(
                (self.semimajor_axis**2 - self.semiminor_axis**2)
                * (self.semiminor_axis**2 + lamb)
            )
            / (self.semimajor_axis**2 + lamb)
            - atan2
        )
        gx = x * horizontal_term
        gy = y * horizontal_term
        gz = (
            z
            * 2
            * const
            * (
                atan2
                - np.sqrt(
                    (self.semimajor_axis**2 - self.semiminor_axis**2)
                    / (self.semiminor_axis**2 + lamb)
                )
            )
        )
        # convert from si to mgal
        if not si_units:
            gx *= 1e5
            gy *= 1e5
            gz *= 1e5
        return (gx, gy, gz)

    def normal_gravitation(
        self, coordinates, *, coordinate_system="geodetic", si_units=False
    ):
        r"""
        Calculate the normal gravitation of the ellipsoid.

        Computes the magnitude of the gradient of the :term:`gravitational
        potential` generated by this ellipsoid at **any point outside the
        ellipsoid**. Based on the closed-form expressions by [Clark1986]_ and
        [Takahashi2017]_.

        .. caution::

            These expressions are only valid for heights on or above the
            surface of the ellipsoid.

        Parameters
        ----------
        coordinates : tuple = (coordinate1, coordinate2, coordinate3)
            Tuple with 3 arrays containing the coordinates of the computation points.
            The meaning of the arrays is determined by the ``coordinate_system``
            argument: longitude, geodetic latitude, and geometric height for a geodetic
            system; longitude, geocentric latitude, and radius for a geocentric
            spherical system; longitude, reduced latitude, and u for an ellipsoidal
            harmonic system; x, y, and z for a geocentric Cartesian system. Each
            element can be a single number or an array. The shape of the arrays must be
            compatible. Longitude and latitudes must be in degrees and height, radius,
            and u in meters. Since longitude is not used in computations (the potential
            is symmetric with longitude), it can be assigned ``None``.
        coordinate_system : str
            The coordinate system that will be assumed for the given coordinates. Should
            be one of: ``"geodetic"`` (default), ``"spherical"``, ``"cartesian"``, or
            ``"ellipsoidal harmonic"``.
        si_units : bool
            Return the value in mGal (False, default) or m/s² (True).

        Returns
        -------
        gravitation : float or array
            The magnitude of the gravitation vector in mGal or m/s².

        Notes
        -----
        .. note::

            Since the calculations happen in geocentric Cartesian coordinates,
            passing inputs in any other coordinate system will require
            conversion, which may slow down computations if done in a loop.
        """
        gx, gy, gz = self.normal_gravitation_vector(
            coordinates, coordinate_system=coordinate_system, si_units=si_units
        )
        return np.sqrt(gx**2 + gy**2 + gz**2)

    def normal_gravity_vector(
        self, coordinates, *, coordinate_system="geodetic", si_units=False
    ):
        r"""
        Calculate the normal gravity vector of the ellipsoid.

        Computes the gradient vector of the :term:`gravity potential`
        (gravitational plus centrifugal) generated by this ellipsoid at **any
        point outside the ellipsoid**. Based on the closed-form expressions by
        [Clark1986]_ and [Takahashi2017]_.

        .. caution::

            These expressions are only valid for heights on or above the
            surface of the ellipsoid.

        Parameters
        ----------
        coordinates : tuple = (coordinate1, coordinate2, coordinate3)
            Tuple with 3 arrays containing the coordinates of the computation points.
            The meaning of the arrays is determined by the ``coordinate_system``
            argument: longitude, geodetic latitude, and geometric height for a geodetic
            system; longitude, geocentric latitude, and radius for a geocentric
            spherical system; longitude, reduced latitude, and u for an ellipsoidal
            harmonic system; x, y, and z for a geocentric Cartesian system. Each
            element can be a single number or an array. The shape of the arrays must be
            compatible. Longitude and latitudes must be in degrees and height, radius,
            and u in meters. Since longitude is not used in computations (the potential
            is symmetric with longitude), it can be assigned ``None``.
        coordinate_system : str
            The coordinate system that will be assumed for the given coordinates. Should
            be one of: ``"geodetic"`` (default), ``"spherical"``, ``"cartesian"``, or
            ``"ellipsoidal harmonic"``.
        si_units : bool
            Return the value in mGal (False, default) or m/s² (True).

        Returns
        -------
        gravity_vector : tuple = (gx, gy, gz)
            Tuple with arrays representing the 3 components of the gravity
            vector in the geocentric Cartesian system in mGal or m/s².

        Notes
        -----
        .. note::

            Since the calculations happen in geocentric Cartesian coordinates,
            passing inputs in any other coordinate system will require
            conversion, which may slow down computations if done in a loop.
        """
        gx, gy, gz = self.normal_gravitation_vector(
            coordinates, coordinate_system=coordinate_system, si_units=si_units
        )
        fx, fy, fz = self.centrifugal_acceleration(
            coordinates, coordinate_system=coordinate_system, si_units=si_units
        )
        return (gx + fx, gy + fy, gz + fz)

    def normal_gravity(
        self, coordinates, *, coordinate_system="geodetic", si_units=False
    ):
        r"""
        Calculate the normal gravity of the ellipsoid.

        Computes the magnitude of the gradient vector of the :term:`gravity
        potential` (gravitational plus centrifugal) generated by this ellipsoid
        at **any point outside the ellipsoid**. Based on the closed-form
        expressions by [Clark1986]_ and [Takahashi2017]_.

        .. caution::

            These expressions are only valid for heights on or above the
            surface of the ellipsoid.

        Parameters
        ----------
        coordinates : tuple = (coordinate1, coordinate2, coordinate3)
            Tuple with 3 arrays containing the coordinates of the computation points.
            The meaning of the arrays is determined by the ``coordinate_system``
            argument: longitude, geodetic latitude, and geometric height for a geodetic
            system; longitude, geocentric latitude, and radius for a geocentric
            spherical system; longitude, reduced latitude, and u for an ellipsoidal
            harmonic system; x, y, and z for a geocentric Cartesian system. Each
            element can be a single number or an array. The shape of the arrays must be
            compatible. Longitude and latitudes must be in degrees and height, radius,
            and u in meters. Since longitude is not used in computations (the potential
            is symmetric with longitude), it can be assigned ``None``.
        coordinate_system : str
            The coordinate system that will be assumed for the given coordinates. Should
            be one of: ``"geodetic"`` (default), ``"spherical"``, ``"cartesian"``, or
            ``"ellipsoidal harmonic"``.
        si_units : bool
            Return the value in mGal (False, default) or m/s² (True).

        Returns
        -------
        gravity : float or array
            The magnitude of the gravity vector in mGal or m/s².

        Notes
        -----
        .. note::

            Since the calculations happen in geocentric Cartesian coordinates,
            passing inputs in any other coordinate system will require
            conversion, which may slow down computations if done in a loop.
        """
        gx, gy, gz = self.normal_gravity_vector(
            coordinates, coordinate_system=coordinate_system, si_units=si_units
        )
        return np.sqrt(gx**2 + gy**2 + gz**2)
