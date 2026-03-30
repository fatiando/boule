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
