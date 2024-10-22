.. _defining_ellipsoids:

Defining custom ellipsoids
==========================

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

----

.. _defining_ellipsoids_oblate:

Oblate ellipsoids
-----------------

Oblate ellipsoids are defined by 4 numerical parameters:

1. The semi-major axis (:math:`a`): the equatorial radius.
2. The flattening (:math:`f = (a - b)/a`): the ratio between the equatorial and
   polar radii.
3. The :term:`geocentric gravitational constant` (:math:`GM`).
4. The angular velocity (:math:`\omega`): spin rate of the ellipsoid which
   defines the centrifugal potential.

You can also include metadata about where the defining parameters came from (a
citation) and a long descriptive name for the ellipsoid. For example, this is
how the WGS84 ellipsoid can be defined with :class:`boule.Ellipsoid` using
parameters from [HofmannWellenhofMoritz2006]_:

.. jupyter-execute::

    import boule as bl


    WGS84 = bl.Ellipsoid(
        name="WGS84",
        long_name="World Geodetic System 1984",
        semimajor_axis=6378137,
        flattening=1 / 298.257223563,
        geocentric_grav_const=3986004.418e8,
        angular_velocity=7292115e-11,
        reference=(
            "Hofmann-Wellenhof, B., & Moritz, H. (2006). Physical Geodesy "
            "(2nd, corr. ed. 2006 edition ed.). Wien ; New York: Springer."
        ),
    )
    print(WGS84)

.. warning::

    You **must** use :class:`boule.Sphere` to represent ellipsoids with
    **zero flattening**. This is because normal gravity calculations in
    :class:`boule.Ellipsoid` make assumptions that fail for the case of
    ``flattening=0`` (mainly that the :term:`gravity potential` is constant on
    the surface of the ellipsoid).

.. _defining_ellipsoids_sphere:

Spheres
-------

Spheres are defined by 3 numerical parameters:

1. The radius (:math:`R`).
2. The :term:`geocentric gravitational constant` (:math:`GM`).
3. The angular velocity (:math:`\omega`): spin rate of the sphere which defines
   the centrifugal potential.

As with oblate ellipsoids, :class:`boule.Sphere` also takes the same metadata
as input.
For example, here is the definition of the Mercury spheroid from parameters
found in [Wieczorek2015]_:

.. jupyter-execute::

    MERCURY = bl.Sphere(
        name="MERCURY",
        long_name="Mercury Spheroid",
        radius=2_439_372,
        geocentric_grav_const=22.031839221e12,
        angular_velocity=1.2400172589e-6,
        reference=(
            "Wieczorek, MA (2015). 10.05 - Gravity and Topography of the Terrestrial "
            "Planets, Treatise of Geophysics (Second Edition); Elsevier. "
            "doi:10.1016/B978-0-444-53802-4.00169-X"
        ),
    )
    print(MERCURY)

.. _defining_ellipsoids_triaxial:

Triaxial ellipsoids
-------------------

Triaxial ellipsoids are defined by 5 numerical parameters:

1. The semi-major axis (:math:`a`): the largest radius.
2. The semi-medium axis (:math:`b`): the middle radius.
3. The semi-minor axis (:math:`c`): the smallest radius.
4. The :term:`geocentric gravitational constant` (:math:`GM`).
5. The angular velocity (:math:`\omega`): spin rate of the ellipsoid which
   defines the centrifugal potential.

:class:`boule.TriaxialEllipsoid` also takes the same metadata attributes as
input.
For example, here is the definition of the Vesta ellipsoid using parameters
from [Russell2012]_:

.. jupyter-execute::

    VESTA = bl.TriaxialEllipsoid(
        name="VESTA",
        long_name="Vesta Triaxial Ellipsoid",
        semimajor_axis=286_300,
        semimedium_axis=278_600,
        semiminor_axis=223_200,
        geocentric_grav_const=1.729094e10,
        angular_velocity=326.71050958367e-6,
        reference=(
            "Russell, C. T., Raymond, C. A., Coradini, A., McSween, H. Y., Zuber, "
            "M. T., Nathues, A., et al. (2012). Dawn at Vesta: Testing the "
            "Protoplanetary Paradigm. Science. doi:10.1126/science.1219381"
        ),
    )
    print(VESTA)


.. attention::

    Gravity calculations have not been implemented yet for triaxial ellipsoids.
    If you're interested in this feature or would like to help implement it,
    please `get in touch <https://www.fatiando.org/contact>`__.
