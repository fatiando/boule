.. _normal_gravity:

Normal gravity
==============

One of the main uses for ellipsoids in geodesy and geophysics is the
computation of :term:`normal gravity` (usually represented by :math:`\gamma`).
The exact calculation and underlying assumptions are a bit different between
the different types of ellipsoids.

Oblate ellipsoids
-----------------

Method :meth:`boule.Ellipsoid.normal_gravity` performs the normal gravity
calculations.
It can operate on single values:

.. jupyter-execute::

    import boule as bl

    # coordiantes = longitude, latitude, height (m)
    gamma = bl.WGS84.normal_gravity(coordinates=(0, 45, 500))
    print(f"{gamma:.2f} mGal")

Or on numpy array-like data (including :class:`pandas.DataFrame` and
:class:`xarray.DataArray`):

.. jupyter-execute::

    import numpy as np

    height = np.linspace(0, 1000, 10)
    gamma = bl.WGS84.normal_gravity(coordinates=(0, 45, height))
    print(gamma)

The arrays can be multi-dimensional so we can use :mod:`bordado` to generate a
grid of normal gravity (the non-dimensional coordinate is the geometric height,
which is constant):

.. jupyter-execute::

    import bordado as bd

    coordinates = bd.grid_coordinates(
        region=[0, 360, -90, 90], spacing=0.5, non_dimensional_coords=10_000,
    )
    gamma = bl.WGS84.normal_gravity(coordinates)
    print(gamma)

Which can be put in a :class:`xarray.DataArray` for convenience:

.. jupyter-execute::

    import xarray as xr
    
    grid = xr.DataArray(
        gamma,
        coords={"longitude": coordinates[0][0, :], "latitude": coordinates[1][:, 0]},
        dims=("latitude", "longitude"),
    )
    grid

And plotted with :mod:`pygmt`:

.. jupyter-execute::
   :hide-code:

   # Needed so that displaying works on jupyter-sphinx and sphinx-gallery at
   # the same time. Using PYGMT_USE_EXTERNAL_DISPLAY="false" in the Makefile
   # for sphinx-gallery to work means that fig.show won't display anything here
   # either.
   import pygmt
   pygmt.set_display(method="notebook")

.. jupyter-execute::

    import pygmt

    fig = pygmt.Figure()
    fig.grdimage(grid, projection="W20c", cmap="viridis")
    fig.basemap(frame=["af", "WEsn"])
    fig.colorbar(position="JCB+w10c", frame=["af", 'y+l"mGal"', 'x+l"WGS84"'])
    fig.show()


.. admonition:: Did you notice?
    :class: note

    The calculations were performed at a non-zero height without the need for a
    free-air correction. That's because
    method :meth:`boule.Ellipsoid.normal_gravity` implements the closed-form
    formula of [Lakshmanan1991]_ and [LiGotze2001]_ instead of the classic
    Somigliana equation.
    This allows us to calculate normal gravity precisely at any height above
    the ellipsoid **without the need for a free-air correction**, which is
    particularly useful for geophysics.

These calculations can be performed for any oblate ellipsoid (see
:ref:`ellipsoids`). Here is the normal gravity of the Martian ellipsoid:

.. jupyter-execute::

    gamma_mars = bl.Mars2009.normal_gravity(coordinates)

    grid_mars = xr.DataArray(
        gamma_mars,
        coords={"longitude": coordinates[0][0, :], "latitude": coordinates[1][:, 0]},
        dims=("latitude", "longitude"),
    )

    fig = pygmt.Figure()
    fig.grdimage(grid_mars, projection="W20c", cmap="lajolla")
    fig.basemap(frame=["af", "WEsn"])
    fig.colorbar(position="JCB+w10c", frame=["af", 'y+l"mGal"', 'x+l"Mars"'])
    fig.show()


Notice that the overall trend is the same as for the Earth (the Martian
ellipsoid is also oblate) but the range of values is different. The mean
gravity on Mars is much weaker than on the Earth: around 370,000 mGal or 3.7
m/s² when compared to 970,000 mGal or 9.7 m/s² for the Earth.

.. admonition:: Assumptions for oblate ellipsoids
    :class: important

    Normal gravity of oblate ellipsoids is calculated under the following
    assumptions:

    * The :term:`gravity potential` is constant on the surface of the ellipsoid.
    * The internal density structure is unspecified but must lead to a constant
      potential at the surface.

    **Important:** A homogeneous density ellipsoid **does not** satisfy the
    condition of constant potential at the surface. See [Karcol2017]_ for a
    thorough discussion.


Spheres
-------

Method :meth:`boule.Sphere.normal_gravity` performs the normal gravity
calculations for spheres. It behaves mostly the same as the oblate ellipsoid
version except that the latitude is a *geocentric spherical latitude* instead
of a geodetic latitude (for spheres they are actually the same thing).

.. jupyter-execute::

    # coordiantes = longitude, latitude, height (m)
    gamma = bl.Moon2015.normal_gravity(coordinates=(None, 45, height))
    print(gamma)

This is what the normal gravity of Moon looks like on a map:

.. jupyter-execute::

    coordinates = bd.grid_coordinates(
        region=[0, 360, -90, 90], spacing=0.5, non_dimensional_coords=10_000,
    )
    gamma_moon = bl.Moon2015.normal_gravity(coordinates)

    grid_moon = xr.DataArray(
        gamma_moon,
        coords={"longitude": coordinates[0][0, :], "latitude": coordinates[1][:, 0]},
        dims=("latitude", "longitude"),
    )

    fig = pygmt.Figure()
    fig.grdimage(grid_moon, projection="W20c", cmap="lapaz")
    fig.basemap(frame=["af", "WEsn"])
    fig.colorbar(position="JCB+w10c", frame=["af", 'y+l"mGal"', 'x+l"Moon"'])
    fig.show()

.. admonition:: Assumptions for spheres
    :class: important

    Normal gravity of spheres is calculated under the following assumptions:

    * The normal gravity is the magnitude of the gradient of the :term:`gravity
      potential` of the sphere.
    * The internal density structure is unspecified but must be either
      homogeneous or vary radially (e.g., in concentric layers).

    A constant gravity potential on the surface of a rotating sphere is not
    possible. Therefore, the normal gravity calculated for a sphere is
    different than that of an oblate ellipsoid (hence why we need a separate
    method of calculation).

Gravity versus gravitation
++++++++++++++++++++++++++

Notice that the variation between poles and equator is much smaller than for
the Earth or Mars.
That's because the **variation is due solely to the centrifugal acceleration**.

We can see this clearly when we calculate the **normal gravitation** (without
the centrifugal component) using :meth:`boule.Sphere.normal_gravitation`:

.. jupyter-execute::

    gravitation = bl.Moon2015.normal_gravitation(
        coordinates=(None, np.linspace(-90, 90, 100), np.full(100, 10_000))
    )
    gravitation

Since there is no centrifugal acceleration, the normal gravitation is due
solely to the mass of a sphere and depends only on the height above the sphere
and not latitude.

.. tip::

   For spherical bodies it can often be better to use
   :meth:`boule.Sphere.normal_gravitation` since services like the
   `ICGEM <http://icgem.gfz-potsdam.de/home>`__ offer the ability to generate
   grids of observed gravitation (without the centrifugal component).
