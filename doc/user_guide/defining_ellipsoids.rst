.. _defining_ellipsoids:

Defining ellipsoids
===================

Boule comes with a range of :ref:`built-in ellipsoids <ellipsoids>` already but
you may want to define your own.
If that's the case, then you have the following options to choose from:

.. grid:: 1 2 1 2
    :margin: 2 5 0 0
    :padding: 0 0 0 0
    :gutter: 4

    .. grid-item-card:: Oblate ellipsoid
        :class-title: sd-fs-4 text-center

        **Class:** :class:`boule.Ellipsoid`

        **When to use:** Your model has 2 semi-axis and non-zero flattening.

        **Caveat:** Assumes constant :term:`gravity potential` on its surface
        and has no specified density distribution.

        .. button-ref:: defining_ellipsoids_oblate
            :ref-type: ref
            :click-parent:
            :color: primary
            :outline:
            :expand:

            Example

    .. grid-item-card:: Sphere
        :class-title: sd-fs-4 text-center

        **Class:** :class:`boule.Sphere`

        **When to use:** Your model has zero flattening.

        **Caveat:** Definition of :term:`normal gravity` is slightly different
        since it's not possible for a rotating sphere to have constant gravity
        potential on its surface.

        .. button-ref:: defining_ellipsoids_sphere
            :ref-type: ref
            :click-parent:
            :color: primary
            :outline:
            :expand:

            Example

    .. grid-item-card:: Triaxial ellipsoid
        :class-title: sd-fs-4 text-center

        **Class:** :class:`boule.TriaxialEllipsoid`

        **When to use:** Your model has 3 distinct semi-axis.

        **Caveat:** Definition of :term:`normal gravity` is the same as the
        case for the sphere. Gravity calculations are not yet available.

        .. button-ref:: defining_ellipsoids_triaxial
            :ref-type: ref
            :click-parent:
            :color: primary
            :outline:
            :expand:

            Example

.. _defining_ellipsoids_oblate:

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


.. _defining_ellipsoids_sphere:

Spheres
-------

.. _defining_ellipsoids_triaxial:

Triaxial ellipsoids
-------------------
