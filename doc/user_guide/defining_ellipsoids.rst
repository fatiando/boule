Defining Ellipsoids
===================

The main functionality of Boule is contained in the classes used to define a
:term:`reference ellipsoid`: :class:`~boule.Ellipsoid`, :class:`~boule.Sphere`,
and :class:`~boule.TriaxialEllipsoid`.

Oblate ellipsoids
-----------------

It defines a :term:`reference ellipsoid`: an *oblate* ellipsoid
that approximates the shape of the Earth (or other planetary body).
Ellipsoids are generally specified by 4 parameters:

1. The semi-major axis (:math:`a`): the equatorial radius.
2. The flattening (:math:`f = (a - b)/a`): the ratio between the equatorial and
   polar radii.
3. The :term:`geocentric gravitational constant` (:math:`GM`).
4. The angular velocity (:math:`\omega`): spin rate of the ellipsoid which
   defines the centrifugal potential.

With these parameters, Boule can calculate gravity, coordinate conversions, and
other derived physical and geometric properties of the ellipsoid.

You can also define your own ellipsoid. For example, this would be a
definition of an ellipsoid with 1000 m semimajor axis, flattening equal to
0.5 and dummy values for :math:`GM` and :math:`\omega`:

.. jupyter-execute::

    import boule as bl
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

If the ellipsoid has zero flattening (a sphere), you must use the
:class:`boule.Sphere` class instead. For example, this would be the
definition of a sphere with 1000 m radius and dummy values for :math:`GM` and
:math:`\omega`:

.. jupyter-execute::

    sphere = bl.Sphere(
        name="Sphere",
        long_name="Ellipsoid with 0 flattening",
        radius=1000,
        geocentric_grav_const=1,
        angular_velocity=1,
    )
    print(sphere)

Spheres
-------


Triaxial ellipsoids
-------------------
