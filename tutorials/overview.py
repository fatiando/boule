r"""
.. _overview:

Overview
========

The main functionality of Boule is contained in the :class:`~boule.Ellipsoid`
class.
It defines a `Reference Ellipsoid <https://en.wikipedia.org/wiki/Reference_ellipsoid>`__:
an *oblate* ellipsoid that approximates the shape of the Earth (or other
planetary body).
Ellipsoids are generally specified by 4 parameters:

1. The semi-major axis (:math:`a`): the equatorial radius.
2. The flattening (:math:`f = (a - b)/a`): the ratio between the equatorial and
   polar radii.
3. The geocentric gravitational constant (:math:`GM`): the multiplication of
   the total mass of the ellipsoid and the `gravitational constant
   <https://en.wikipedia.org/wiki/Gravitational_constant>`__.
4. The angular velocity (:math:`\omega`): spin rate of the ellipsoid which
   defines the centrifugal potential.

With these parameters, Boule can calculate gravity, coordinate conversions, and
other derived physical and geometric properties of the ellipsoid.

The library
-----------

All functions and classes in Boule are available in the base namespace of the
:mod:`boule` package. This means that you can access all of them with a single
import:

"""

# Boule is usually imported as bl
import boule as bl

###############################################################################
# Ellipsoids
# ----------
#
# Boule comes with :ref:`built-in ellipsoids <ellipsoids>` that can be accessed
# as global variables in the :mod:`boule` module:

print(bl.WGS84)
print(bl.MARS)

###############################################################################
# As seen above, :class:`~boule.Ellipsoid` instances can be printed to record
# their defining attributes. Additionally, ellipsoids define a name (short and
# long version) and reference for the origin of the numbers used:

print(bl.MARS.name)
print(bl.MARS.reference)

###############################################################################
# Other derived properties of ellipsoids are calculated on demand when
# accessed:

print(bl.MARS.first_eccentricity)
print(bl.MARS.gravity_pole)
print(bl.MARS.gravity_equator)

###############################################################################
# You can also define your own ellipsoid. For example, this would be a definition of an
# ellipsoid with 1000 m semimajor axis, flattening equal to 0.5 and dummy values for
# :math:`GM` and :math:`\omega`:

ellipsoid = bl.Ellipsoid(
    name="Ellipsoid",
    long_name="Ellipsoid with 0.5 flattening",
    flattening=0.5,
    semimajor_axis=1000,
    geocentric_grav_const=1,
    angular_velocity=1,
)
print(ellipsoid)
print(ellipsoid.semiminor_axis)
print(ellipsoid.first_eccentricity)


###############################################################################
# If the ellipsoid has zero flattening (a sphere), you must use the
# :class:`boule.Sphere` class instead. For example, this would be the definition of
# a sphere with 1000 m radius and dummy values for :math:`GM` and :math:`\omega`:

sphere = bl.Sphere(
    name="Sphere",
    long_name="Ellipsoid with 0 flattening",
    radius=1000,
    geocentric_grav_const=1,
    angular_velocity=1,
)
print(sphere)

###############################################################################
# Computations
# ------------
#
# Ellipsoids can be used for computations generally encountered in geodetic and
# geophysical applications:
#
# 1. :ref:`Normal gravity <normal_gravity>`
# 2. Converting geodetic latitude and height into geocentric latitude and
#    radius.
#
# See the respective tutorials and :ref:`reference documentation <api>` for
# more information.
