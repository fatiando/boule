.. _gravity_disturbance:

Gravity disturbances
====================

One of the main uses of Boule in geophysics is the calculation of
:term:`gravity disturbances <gravity disturbance>`.
Our closed-form implementation of :ref:`normal gravity <normal_gravity>` allows
accurate gravity disturbance calculation at any height without the errors
associated with approximate free-air corrections.

As an example, lets calculate a gravity disturbance grid for the Earth using a
global gravity from the
`EIGEN-6C4 spherical harmonic model <https://doi.org/10.5880/icgem.2015.1>`__
at a height of 10 km.
We'll use the WGS84 ellipsoid for this but the workflow is the same for any other ellipsoid.

First off, we import the required packages to do this:

.. jupyter-execute::

    import boule as bl
    import ensaio
    import xarray as xr  # For loading the grid data
    import pygmt         # For plotting nice maps

Next, we can download and cache the gravity grid using :mod:`ensaio` and load
it with :mod:`xarray`:

.. jupyter-execute::

    fname = ensaio.fetch_earth_gravity(version=1)
    observed_gravity = xr.load_dataarray(fname)
    observed_gravity

Now we can calculate the WGS84 normal gravity at the same points as the
observed gravity and subtract it from the data grid to obtain the gravity
disturbance:

.. jupyter-execute::

    normal_gravity = bl.WGS84.normal_gravity(
        observed_gravity.latitude, observed_gravity.height,
    )
    disturbance = observed_gravity - normal_gravity
    disturbance

Finally, we can display the disturbance in a nice global map using
:mod:`pygmt`:

.. jupyter-execute::

    fig = pygmt.Figure()
    fig.grdimage(
        disturbance, projection="W20c", cmap="polar+h", shading="+a45+nt0.2",
    )
    fig.basemap(frame=["af", "WEsn"])
    fig.colorbar(
        position="JCB+w10c",
        frame=["af", 'y+l"mGal"', 'x+l"gravity disturbance"'],
    )
    fig.coast(shorelines=True, resolution="c", area_thresh=1e4)
    fig.show()

The disturbance clearly highlights all of the major subduction zones and large
oceanic island chains, all of which are not in local isostatic equilibrium.
