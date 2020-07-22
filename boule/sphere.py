"""
Module for defining and setting the reference sphere.
"""
import attr
import numpy as np

from . import Ellipsoid


# Don't let ellipsoid parameters be changed to avoid messing up calculations
# accidentally.
@attr.s(frozen=True)
class Sphere(Ellipsoid):
    """
    Reference spherical ellipsoid

    Represents ellipsoids with zero flattening (spheres). Inherits methods and
    properties of the :class:`boule.Ellipsoid`, guaranteeing no singularities
    due to zero flattening (and thus zero eccentricity).

    All parameters are in SI units.

    Parameters
    ----------
    name : str
        A short name for the ellipsoid, for example ``'MOON'``.
    radius : float
        The radius of the sphere [meters].
    geocentric_grav_const : float
        The geocentric gravitational constant (GM) [m^3 s^-2].
    angular_velocity : float
        The angular velocity of the rotating ellipsoid (omega) [rad s^-1].
    long_name : str or None
        A long name for the ellipsoid, for example ``"Moon Reference System"``
        (optional).
    reference : str or None
        Citation for the ellipsoid parameter values (optional).

    Examples
    --------

    We can define a unit sphere:

    >>> sphere = Sphere(
    ...     name="sphere",
    ...     radius=1,
    ...     geocentric_grav_const=1,
    ...     angular_velocity=0,
    ...     long_name="Spherical Ellipsoid",
    ... )
    >>> print(sphere) # doctest: +ELLIPSIS
    Sphere(name='sphere', ...)
    >>> print(sphere.long_name)
    Spherical Ellipsoid
    >>> print("{:.2f}".format(sphere.semiminor_axis))
    1.00
    >>> print("{:.2f}".format(sphere.mean_radius))
    1.00
    >>> print("{:.2f}".format(sphere.flattening))
    0.00
    >>> print("{:.2f}".format(sphere.linear_eccentricity))
    0.00
    >>> print("{:.2f}".format(sphere.first_eccentricity))
    0.00
    >>> print("{:.2f}".format(sphere.second_eccentricity))
    0.00
    >>> print(sphere.normal_gravity(latitude=0, height=1))
    25000.0
    >>> print(sphere.normal_gravity(latitude=90, height=1))
    25000.0
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
    semimajor_axis = attr.ib(init=False)
    flattening = attr.ib(init=False)

    def __attrs_post_init__(self):
        """
        Overwrite inherited attributes
        """
        object.__setattr__(self, "semimajor_axis", self.radius)
        object.__setattr__(self, "flattening", 0)

    def normal_gravity(self, latitude, height):
        """
        Calculate normal gravity at any latitude and height

        Computes the magnitude of the gradient of the gravity potential
        (gravitational + centrifugal) generated by the sphere at the given
        latitude and height.

        Parameters
        ----------
        latitude : float or array
            The latitude where the normal gravity will be computed (in degrees).
        height : float or array
            The height (above the sphere) of computation point (in meters).

        Returns
        -------
        gamma : float or array
            The normal gravity in mGal.

        References
        ----------
        [Heiskanen-Moritz]_
        """
        return self._gravity_sphere(height) + self._centrifugal_force(latitude, height)

    def _gravity_sphere(self, height):
        """
        Calculate the gravity generated by a solid sphere (mGal)
        """
        return 1e5 * self.geocentric_grav_const / (self.radius + height) ** 2

    def _centrifugal_force(self, latitude, height):
        """
        Calculate the centrifugal force due to the rotation of the sphere (mGal)
        """
        return 1e5 * (
            (-1)
            * self.angular_velocity ** 2
            * (self.radius + height)
            * np.cos(np.radians(latitude))
        )

    @property
    def gravity_equator(self):
        """
        The norm of the gravity vector at the equator on the sphere [m/s^2]

        Overrides the inherited method from :class:`boule.Ellipsoid` to avoid
        singularities due to zero flattening.
        """
        return self._gravity_on_surface

    @property
    def gravity_pole(self):
        """
        The norm of the gravity vector at the poles on the sphere [m/s^2]

        Overrides the inherited method from :class:`boule.Ellipsoid` to avoid
        singularities due to zero flattening.
        """
        return self._gravity_on_surface

    @property
    def _gravity_on_surface(self):
        """
        Compute norm of the gravity vector on the surface of the sphere [m/s^2]

        Due to rotational symmetry, the norm of the gravity vector is the same
        on every point of the surface.
        """
        return self.geocentric_grav_const / self.radius ** 2
