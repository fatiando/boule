.. _coordinates:

Coordinate conversions
======================

The :class:`boule.Ellipsoid` class has methods to convert coordinates between different
coordinate systems: geocentric Cartesian (a.k.a. Earth-centered Earth-fixed, ECEF),
geocentric spherical, geodetic, and ellipsoidal harmonic.

.. seealso::
 
    Boule ellipsoids are also compatible with the `pymap3d
    <https://github.com/geospace-code/pymap3d/>`__ package and be given to its functions
    as inputs. See :ref:`pymap3d`.

Below, we'll show some examples of these conversions. See the respective methods in
:class:`boule.Ellipsoid` for more details.
  
.. jupyter-execute::

    import boule as bl
    import numpy as np

The coordinate systems
----------------------

The four systems share an origin (the center of the ellipsoid), a polar axis
(the semi-minor axis of the ellipsoid), and a longitude, which is the angle
measured on the equatorial plane from the prime meridian. They differ in how
they locate a point P on the meridian plane that contains it:

* **Geocentric Cartesian**, also known as Earth-centered Earth-fixed (ECEF):
  the distances x, y, and z of P from the center along three orthogonal axes,
  with z along the polar axis and x crossing the prime meridian.
* **Geocentric spherical**: the distance r of P from the center and the
  geocentric latitude :math:`\phi'`, which is the angle between r and the
  equatorial plane.
* **Geodetic**: the geometric height h of P above the ellipsoid, measured
  along the normal to its surface, and the geodetic latitude :math:`\phi`,
  which is the angle that same normal makes with the equatorial plane. The
  normal only points at the center of the ellipsoid at the equator and the
  poles, which is why the two latitudes differ everywhere else.
* **Ellipsoidal harmonic**: the semi-minor axis u of the ellipsoid that is
  confocal with the reference ellipsoid and passes through P, and the reduced
  (or parametric) latitude :math:`\beta`. Confocal ellipsoids share the foci
  of the reference one, and the reference ellipsoid itself (u equal to its
  semi-minor axis) is an equipotential surface of the normal gravity field,
  which is what makes this system convenient for computing normal gravity.

The figure below shows the same point P in all four systems. It is drawn with
an ellipsoid flattened far beyond any planet (a flattening of 0.3 against the
0.0034 of the Earth) because the systems are otherwise indistinguishable by
eye. Everything in it is computed with Boule, so the angles and distances are
exact for the ellipsoid that is drawn.

.. jupyter-execute::
    :hide-code:

    import boule as bl
    import matplotlib.pyplot as plt
    import numpy as np

    # Exaggerate the flattening so that the systems are visibly different.
    ellipsoid = bl.Ellipsoid(
        name="Exaggerated",
        semimajor_axis=1,
        flattening=0.3,
        geocentric_grav_const=0,
        angular_velocity=0,
    )
    a = ellipsoid.semimajor_axis
    b = ellipsoid.semiminor_axis
    E = ellipsoid.linear_eccentricity

    latitude, height = 40, 0.35
    x, _, z = ellipsoid.geodetic_to_cartesian((0, latitude, height))
    x_surface, _, z_surface = ellipsoid.geodetic_to_cartesian((0, latitude, 0))
    _, latitude_spherical, _ = ellipsoid.geodetic_to_spherical((0, latitude, height))
    _, latitude_reduced, u = ellipsoid.geodetic_to_ellipsoidal_harmonic(
        (0, latitude, height)
    )
    semimajor_confocal = np.sqrt(u**2 + E**2)

    angle = np.radians(np.linspace(0, 90, 180))
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.2))

    for ax in axes:
        ax.plot(a * np.cos(angle), b * np.sin(angle), color="#333333", linewidth=2)
        ax.annotate("", xy=(1.45 * a, 0), xytext=(0, 0), arrowprops={"arrowstyle": "->"})
        ax.annotate("", xy=(0, 1.45 * b), xytext=(0, 0), arrowprops={"arrowstyle": "->"})
        ax.plot(x, z, "o", color="#d62728", zorder=5)
        ax.annotate("P", (x, z), xytext=(6, 6), textcoords="offset points", fontsize=13)
        ax.set_aspect("equal")
        ax.set_xlim(-0.2 * a, 1.5 * a)
        ax.set_ylim(-0.15 * b, 1.12 * semimajor_confocal)
        ax.axis("off")

    # Cartesian, spherical, and geodetic
    ax = axes[0]
    ax.text(1.46 * a, 0, "x", fontsize=13, va="center")
    ax.text(0, 1.48 * b, "z", fontsize=13, ha="center")
    ax.plot([0, x], [0, z], color="#1f77b4", linewidth=1.5)
    ax.plot([x_surface, x], [z_surface, z], color="#2ca02c", linewidth=1.5)
    # Extend the normal down to the equatorial plane to show the geodetic latitude.
    slope = (z - z_surface) / (x - x_surface)
    x_intercept = x_surface - z_surface / slope
    ax.plot([x_intercept, x_surface], [0, z_surface], color="#2ca02c", linestyle=":", linewidth=1.2)
    ax.plot([x, x], [0, z], color="#999999", linestyle="--", linewidth=1)
    ax.plot([0, x], [z, z], color="#999999", linestyle="--", linewidth=1)

    spherical_arc = np.radians(np.linspace(0, latitude_spherical, 60))
    ax.plot(0.42 * np.cos(spherical_arc), 0.42 * np.sin(spherical_arc), color="#1f77b4", linewidth=1.2)
    ax.text(0.5, 0.13, r"$\phi'$", color="#1f77b4", fontsize=14)
    geodetic_arc = np.radians(np.linspace(0, latitude, 60))
    ax.plot(
        x_intercept + 0.3 * np.cos(geodetic_arc),
        0.3 * np.sin(geodetic_arc),
        color="#2ca02c",
        linewidth=1.2,
    )
    ax.text(x_intercept + 0.33, 0.09, r"$\phi$", color="#2ca02c", fontsize=14)
    ax.text(
        0.5 * x - 0.02,
        0.5 * z + 0.04,
        "r",
        color="#1f77b4",
        fontsize=13,
        rotation=latitude_spherical,
    )
    ax.text(x + 0.03, 0.5 * (z + z_surface), "h", color="#2ca02c", fontsize=13)
    ax.set_title("Cartesian, spherical, and geodetic", fontsize=12)

    # Ellipsoidal harmonic
    ax = axes[1]
    ax.text(1.46 * a, 0, "x", fontsize=13, va="center")
    ax.text(0, 1.48 * b, "z", fontsize=13, ha="center")
    ax.plot(
        semimajor_confocal * np.cos(angle),
        u * np.sin(angle),
        color="#9467bd",
        linewidth=1.5,
        linestyle="--",
    )
    ax.annotate(
        "", xy=(-0.06, u), xytext=(-0.06, 0), arrowprops={"arrowstyle": "<->", "color": "#9467bd"}
    )
    ax.text(-0.13, 0.5 * u, "u", color="#9467bd", fontsize=13, va="center")
    ax.plot(E, 0, "x", color="#333333", markersize=8)
    ax.text(E, -0.09, "focus", fontsize=10, ha="center")
    # The reduced latitude is the angle on the circle circumscribing the confocal ellipse.
    ax.plot(
        semimajor_confocal * np.cos(angle),
        semimajor_confocal * np.sin(angle),
        color="#cccccc",
        linewidth=1,
    )
    x_circle = semimajor_confocal * np.cos(np.radians(latitude_reduced))
    z_circle = semimajor_confocal * np.sin(np.radians(latitude_reduced))
    ax.plot([0, x_circle], [0, z_circle], color="#9467bd", linewidth=1.2, linestyle=":")
    ax.plot([x, x_circle], [z, z_circle], color="#999999", linestyle="--", linewidth=1)
    reduced_arc = np.radians(np.linspace(0, latitude_reduced, 60))
    ax.plot(0.42 * np.cos(reduced_arc), 0.42 * np.sin(reduced_arc), color="#9467bd", linewidth=1.2)
    ax.text(0.48, 0.16, r"$\beta$", color="#9467bd", fontsize=14)
    ax.set_title("Ellipsoidal harmonic", fontsize=12)

    fig.tight_layout()

    plt.show()

Geodetic to and from geocentric spherical
-----------------------------------------

The :class:`boule.Ellipsoid` class implements coordinate conversions between
geodetic coordinates and geocentric spherical coordinates:

* :meth:`boule.Ellipsoid.geodetic_to_spherical`
* :meth:`boule.Ellipsoid.spherical_to_geodetic`

Both are common in geophysical applications when dealing with spherical harmonics or
spherical modeling of topography.

The example below will show you how to convert geodetic latitude and height
into geocentric spherical latitude and radius.

.. jupyter-execute::

    longitude = 40
    latitude = np.linspace(-90, 90, 45)
    height = 481_000  # ICESat-2 orbit height in meters

    longitude_sph, latitude_sph, radius = bl.WGS84.geodetic_to_spherical(
        (longitude, latitude, height),
    )

    print("Longitude:", longitude_sph)
    print("Geocentric latitude:", latitude_sph)
    print("Geodetic latitude:", latitude)
    print("Radius (m):", radius)

Notice that:

1. The longitude is the same in both coordinates systems.
2. The latitude is slightly different except for the poles and equator.
3. The radius (distance from the center of the ellipsoid) varies even though
   the height is constant.

.. tip::

    We used the WGS84 ellipsoid here but the workflow is the same for any
    other oblate ellipsoid. Checkout :ref:`ellipsoids` for options.

Geocentric Cartesian to and from spherical and geodetic
-------------------------------------------------------

Another common coordinate conversion used in global studies is transform between a
geocentric Cartesian system and geocentric spherical and geodetic coordinates:

* :meth:`boule.Ellipsoid.geodetic_to_cartesian`
* :meth:`boule.Ellipsoid.spherical_to_cartesian`
* :meth:`boule.Ellipsoid.cartesian_to_geodetic`
* :meth:`boule.Ellipsoid.cartesian_to_spherical`

The example below demonstrate this conversion using the Cartesian coordinates of the
`Insight lander <https://en.wikipedia.org/wiki/InSight>`__ on Mars from [LeMaistre2023]_
and the Martian ellipsoid defined in Boule.

.. jupyter-execute::

    # InSight lander coordinates (x, y, z) in meters
    cartesian_coordinates = [-2_417_504.5, 2_365_954.5, 266_266.7]  

    # Convert Cartesian to geocentric spherical
    longitude, latitude_sph, radius = bl.Mars2009.cartesian_to_spherical(
        cartesian_coordinates
    )

    print(f"Geocentric longitude: {longitude}")
    print(f"Geocentric latitude: {latitude_sph}")
    print(f"Radius (m): {radius}")

.. jupyter-execute::

    longitude, latitude_geod, height = bl.Mars2009.cartesian_to_geodetic(
        cartesian_coordinates
    )

    print(f"Geodetic longitude: {longitude}")
    print(f"Geodetic latitude: {latitude_geod}")
    print(f"Ellipsoidal height (m): {height}")

.. _pymap3d:
  
Using Boule ellipsoids with pymap3d
-----------------------------------

Boule's :class:`~boule.Ellipsoid` and :class:`~boule.Sphere` classes can be
used with `pymap3d <https://github.com/geospace-code/pymap3d/>`__ for
converting between different coordinate systems.
While pymap3d defines some ellipsoids internally, you may want to use one from
Boule if:

* You want to be certain that the parameters used for coordinate conversions
  and gravity calculations are consistent.
* You need to :ref:`define your own ellipsoid <defining_ellipsoids>`, either
  because you need different parameters than the built-in ones or they aren't
  available in either Boule or pymap3d.

The example below converts between geodetic and geocentric spherical using
``pymap3d.geodetic2spherical`` instead of
:meth:`boule.Ellipsoid.geodetic_to_spherical` to achieve the same outcome as
in the previous example.

.. jupyter-execute::

    import pymap3d

    longitude = 40
    latitude = np.linspace(-90, 90, 45)
    height = 481_000  # ICESat-2 orbit height in meters

    latitude_sph, longitude_sph, radius = pymap3d.geodetic2spherical(
        latitude, longitude, height, ell=bl.WGS84,
    )

    print("Longitude:", longitude_sph)
    print("Geocentric latitude:", latitude_sph)
    print("Radius (m):", radius)
