.. _coordinates:

Coordinate conversions
======================

Boule's :class:`~boule.Ellipsoid` and :class:`~boule.Sphere` classes can be
used with `pymap3d <https://github.com/geospace-code/pymap3d/>`__ for
converting between different coordinate systems.
While pymap3d defines some ellipsoids internally, you may want to use one from
Boule if:

* You want to be certain that the parameters used for coordinate conversions
  and gravity calculations are consistent.
* Need to :ref:`define your own ellipsoid <defining_ellipsoids>` either because
  you need different parameters than the built-in ones or they aren't available
  in either Boule or pymap3d.

.. admonition:: Help!
    :class: hint

    If an ellipsoid you need isn't in Boule yet, please `reach out
    <https://www.fatiando.org/contact>`__ to the team and consider adding it
    yourself. It requires no special knowledge of the code and is a great way
    to help the project!

Geodetic to spherical
---------------------

The example below will show you how to convert geodetic latitude and height
into geocentric spherical latitude and radius.

.. jupyter-execute::

    import boule as bl
    import pymap3d
    import numpy as np

    latitude = np.linspace(-90, 90, 45)
    longitude = 40
    height = 481_000  # ICESat-2 orbit height in meters

    latitude_sph, longitude_sph, radius = pymap3d.geodetic2spherical(
        latitude, longitude, height, ell=bl.WGS84,
    )
    print("Geodetic latitude:", latitude)
    print("Spherical latitude:", latitude_sph)
    print()
    print("Geodetic longitude:", longitude)
    print("Spherical longitude:", longitude_sph)
    print()
    print("Height (m):", height)
    print("Radius (m):", radius)

Notice that:

1. The latitude is slightly different except for the poles and equator.
2. The longitude is the same in both coordinates systems.
3. The radius (distance from the center of the ellipsoid) varies even though
   the height is constant.

.. tip::

    We used the WGS84 ellipsoid here but the workflow is the same for any
    other oblate ellipsoid or sphere. Checkout :ref:`ellipsoids` for options.

Geodetic to Cartesian
---------------------

Another common coordinate conversion done in global studies is from geodetic
latitude, longitude, and height to geocentric Cartesian X, Y, and Z.
The example below performs this conversion for the location of the
`Insight lander <https://en.wikipedia.org/wiki/InSight>`__ on Mars based on
[Parker2019]_:

.. jupyter-execute::

    X, Y, Z = pymap3d.geodetic2ecef(
        lat=4.502384, lon=135.623447, alt=-2613.426, ell=bl.MARS,
    )
    print(f"X = {X} m")
    print(f"Y = {Y} m")
    print(f"Z = {Z} m")
