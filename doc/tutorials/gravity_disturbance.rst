.. _gravity_disturbance:

Gravity disturbances
====================

Gravity disturbances are the differences between the measured gravity and a
normal gravity produced by an ellipsoid.

As an example, lets calculate a gravity disturbances grid at a height of 10 km
using the global gravity from EIGEN-6C4 and WGS84 ellipsoid.

.. jupyter-execute::

    import ensaio
    import pygmt
    import xarray as xr

    import boule as bl

    # Download and cache the global gravity data using Ensaio
    fname = ensaio.fetch_earth_gravity(version=1)
    # Load the gravity data using xarray
    gravity = xr.load_dataarray(fname)
    print(gravity)

    # Calculate the normal gravity using the WGS84 ellipsoid from Boule
    ellipsoid = bl.WGS84
    gamma = ellipsoid.normal_gravity(gravity.latitude, gravity.height)

    # The disturbance is the observed minus normal gravity (calculated at the
    # observation point)
    disturbance = gravity - gamma

    # Make a PyGMT pseudo-color map
    fig = pygmt.Figure()
    fig.basemap(
        region="g",
        projection="W15c",
        frame=True,
    )
    fig.grdimage(disturbance, cmap="polar+h", shading="+nt0.5")
    fig.colorbar(frame='af+l"disturbance [mGal]"')
    fig.coast(shorelines=True, resolution="c", area_thresh=1e4)
    fig.show()
