.. _overview:

Overview
========

The library
-----------

All functions and classes in Boule are available from the base namespace of the
:mod:`boule` package. This means that you can access all of them with a single
import:

.. jupyter-execute::

    # Boule is usually imported as bl
    import boule as bl

Ellipsoids
----------

Boule comes with several :ref:`built-in ellipsoids <ellipsoids>` that are
available as global variables in the :mod:`boule` module.
The ellipsoids can be printed to view their defining attributes:

.. jupyter-execute::

    print(bl.WGS84)
    print(bl.MOON)
    print(bl.VESTA)

Ellipsoids define a name (short and long version) and reference for the origin
of the numbers used:

.. jupyter-execute::

    print(f"{bl.MARS.name}: {bl.MARS.long_name}")
    print(bl.MARS.reference)

Other derived properties of ellipsoids are calculated on demand when
accessed:

.. jupyter-execute::

    print(bl.GRS80.first_eccentricity)
    print(bl.GRS80.gravity_pole)
    print(bl.GRS80.gravity_equator)

.. hint::

    You may have noticed that there are 3 different types of ellipsoids:
    :class:`~boule.Ellipsoid`, :class:`~boule.Sphere`, and
    :class:`~boule.TriaxialEllipsoid`. They each offer different attributes and
    capabilities. Be sure to check out the :ref:`api` for a full list of what
    each class offers.

Normal gravity
--------------

Ellipsoids can be used for computations generally encountered in geodetic and
geophysical applications.
A common one is calculating :term:`normal gravity`.
Here is an example of using Boule to calculate the :term:`normal gravity` of
the WGS84 ellipsoid on the Earth's surface (topography in the continents, the
geoid in the oceans).

First, we need to import a few other packages:

.. jupyter-execute::

    import ensaio        # For downloading sample data
    import pygmt         # For plotting maps
    import xarray as xr  # For manipulating grids

.. jupyter-execute::
   :hide-code:

   # Needed so that displaying works on jupyter-sphinx and sphinx-gallery at
   # the same time. Using PYGMT_USE_EXTERNAL_DISPLAY="false" in the Makefile
   # for sphinx-gallery to work means that fig.show won't display anything here
   # either.
   pygmt.set_display(method="notebook")

Now we can download and open :term:`co-located grids` of topography and geoid
using :mod:`ensaio` and :mod:`xarray`:

.. jupyter-execute::

    fname_topo = ensaio.fetch_earth_topography(version=1)
    fname_geoid = ensaio.fetch_earth_geoid(version=1)
    topography = xr.load_dataarray(fname_topo)
    geoid = xr.load_dataarray(fname_geoid)
    geoid

The computation height can be defined by combining topography and geoid:

.. jupyter-execute::

    height = xr.where(
        topography >= 0,
        topography + geoid,  # geometric height of topography in the continents
        geoid,  # geoid height in the oceans
    )

Finally, we can calculate normal gravity using
:meth:`~boule.Ellipsoid.normal_gravity` at the given heights and plot it on a
map with :mod:`pygmt`:

.. jupyter-execute::

    gamma = bl.WGS84.normal_gravity(topography.latitude, height)

    fig = pygmt.Figure()
    fig.grdimage(gamma, projection="W20c", cmap="viridis", shading="+a45+nt0.3")
    fig.basemap(frame=["af", "WEsn"])
    fig.colorbar(position="JCB+w10c", frame=["af", 'y+l"mGal"'])
    fig.show()

.. seealso::

    :ref:`normal_gravity` provides a more detailed tutorial, including the
    different definitions of normal gravity for each ellipsoid type.
