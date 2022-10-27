.. _coordinates:

Coordinate conversions
======================

Geodetic to geocentric spherical
--------------------------------

The :class:`boule.Ellipsoid` class implements coordinate conversions between
geocentric geodetic coordinates and geocentric spherical coordinates. Both are
common in geophysical applications when dealing with spherical harmonics or
spherical modeling of topography.

The example below will show you how to convert geodetic latitude and height
into geocentric spherical latitude and radius.

.. jupyter-execute::

    import boule as bl
    import numpy as np

    longitude = 40
    latitude = np.linspace(-90, 90, 45)
    height = 481_000  # ICESat-2 orbit height in meters

    longitude_sph, latitude_sph, radius = bl.WGS84.geodetic_to_spherical(
        longitude, latitude, height,
    )

    print("Geodetic longitude:", longitude)
    print("Spherical longitude:", longitude_sph)
    print("Geodetic latitude:", latitude)
    print("Spherical latitude:", latitude_sph)
    print("Height (m):", height)
    print("Radius (m):", radius)

Notice that:

1. The longitude is the same in both coordinates systems.
2. The latitude is slightly different except for the poles and equator.
3. The radius (distance from the center of the ellipsoid) varies even though
   the height is constant.

.. tip::

    We used the WGS84 ellipsoid here but the workflow is the same for any
    other oblate ellipsoid. Checkout :ref:`ellipsoids` for options.

Other conversions using pymap3d
-------------------------------

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

The example below converts between geodetic and geocentric spherical using
``pymap3d.geodetic2spherical`` instead of
:meth:`boule.Ellipsoid.geodetic_to_spherical` to achieve the same outcome:

.. jupyter-execute::

    import pymap3d

    longitude = 40
    latitude = np.linspace(-90, 90, 45)
    height = 481_000  # ICESat-2 orbit height in meters

    latitude_sph, longitude_sph, radius = pymap3d.geodetic2spherical(
        latitude, longitude, height, ell=bl.WGS84,
    )

    print("Geodetic longitude:", longitude)
    print("Spherical longitude:", longitude_sph)
    print("Geodetic latitude:", latitude)
    print("Spherical latitude:", latitude_sph)
    print("Height (m):", height)
    print("Radius (m):", radius)

Another common coordinate conversion done in global studies is from geodetic
latitude, longitude, and height to geocentric Cartesian X, Y, and Z.
The example below performs this conversion for the location of the
`Insight lander <https://en.wikipedia.org/wiki/InSight>`__ on Mars based on
[Parker2019]_ using the Martian ellipsoid defined in Boule:

.. jupyter-execute::

    X, Y, Z = pymap3d.geodetic2ecef(
        lat=4.502384, lon=135.623447, alt=-2613.426, ell=bl.MARS,
    )
    print(f"X = {X} m")
    print(f"Y = {Y} m")
    print(f"Z = {Z} m")
