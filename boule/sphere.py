"""
Module for defining and setting the reference sphere.
"""
import attr

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
    flattening = attr.ib(init=False, default=0)

    @semimajor_axis.default
    def _set_semimajor_axis(self):
        "The semimajor axis should be the radius"
        return self.radius

    def normal_gravity(self, latitude, height):
        r"""
        Calculate normal gravity at any latitude and height.

        .. warning::

            Normal gravity is computed considering a non-rotating sphere in
            hydrostatic equilibrium.

        Computes the magnitude of the gradient of the gravity potential of
        a sphere in hydrostatic equilibrium, which is not under rotation.
        The normal gravity is then computed as the magnitude of the gradient of
        the gravity potential without taking into account the centrifugal
        potential.

        .. math::

            \gamma = \frac{GM}{r^2}

        Parameters
        ----------
        latitude : float or array
            The latitude where the normal gravity will be computed (in degrees).
        height : float or array
            The height (above the sphere) of computation point (in meters).

        Returns
        -------
        gamma : float or array
            The normal gravity of the non-rotating sphere in mGal.

        References
        ----------
        [Heiskanen-Moritz]_
        """
        return 1e5 * self.geocentric_grav_const / (self.radius + height) ** 2

    @property
    def gravity_equator(self):
        """
        The norm of the gravity vector at the equator of the sphere [m/s^2]

        .. warning::

            The gravity vector is computed considering a non-rotating sphere in
            hydrostatic equilibrium.

        Computes the norm of the gravity vector at the equator of the
        non-rotating sphere.
        """
        return self.gravity_surface

    @property
    def gravity_pole(self):
        """
        The norm of the gravity vector at the poles of the sphere [m/s^2]

        .. warning::

            The gravity vector is computed considering a non-rotating sphere in
            hydrostatic equilibrium.

        Computes the norm of the gravity vector at the poles of the
        non-rotating sphere.
        """
        return self.gravity_surface

    @property
    def gravity_surface(self):
        """
        The norm of the gravity vector at the surface of the sphere [m/s^2]

        .. warning::

            The gravity vector is computed considering a non-rotating sphere in
            hydrostatic equilibrium.

        Computes the norm of the gravity vector at the poles of the
        non-rotating sphere.
        """
        return self.geocentric_grav_const / self.radius ** 2
