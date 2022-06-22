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

    gamma = bl.WGS84.normal_gravity(latitude=45, height=50)
    print(f"{gamma:.2f} mGal")

Or on numpy array-like data (including ``pandas.DataFrame`` and
``xarray.DataArray``):

.. jupyter-execute::

    import numpy as np

    height = np.linspace(0, 1000, 10)
    gamma = bl.WGS84.normal_gravity(latitude=45, height=height)
    print(gamma)

The arrays can be multi-dimensional so we can use :mod:`verde` to generate a
grid of normal gravity:

.. jupyter-execute::

    import verde as vd

    longitude, latitude = vd.grid_coordinates(
        region=[0, 360, -90, 90], spacing=0.5,
    )
    gamma = bl.WGS84.normal_gravity(latitude=latitude, height=10_000)
    print(gamma)

Which can be put in a :class:`xarray.Dataset`:

.. jupyter-execute::

    grid = vd.make_xarray_grid(
        (longitude, latitude), gamma, data_names="normal_gravity",
    )
    grid

And plotted with :mod:`pygmt`:

.. jupyter-execute::

    import pygmt

    fig = pygmt.Figure()
    fig.grdimage(grid.normal_gravity, projection="W20c", cmap="viridis")
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

    gamma_mars = bl.MARS.normal_gravity(latitude=latitude, height=10_000)
    grid_mars = vd.make_xarray_grid(
        (longitude, latitude), gamma_mars, data_names="normal_gravity",
    )

    fig = pygmt.Figure()
    fig.grdimage(grid_mars.normal_gravity, projection="W20c", cmap="lajolla")
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
