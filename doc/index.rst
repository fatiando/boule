.. title:: Home

.. raw:: html

    <h1 class="display-2 text-center">
      Boule
    </h1>

    <p class="lead text-center front-page-callout">
      Reference ellipsoids for geodesy and geophysics
    </p>

**Boule** is Python library for representing
:term:`reference ellipsoids <reference ellipsoid>` geometrically, calculating
their gravity fields, and performing some global coordinate conversions.
"Boule" is also French for "ball" as well as a `traditional shape of bread
resembling a squashed ball <https://en.wikipedia.org/wiki/Boule_(bread)>`__
(much like the Earth).

Boule is designed for:

* Storing and manipulating ellipsoid parameters for spherical harmonic analysis
  and coordinate system conversions.
* Calculating :term:`normal gravity` for generating gravity anomalies and
  disturbances.

Here is an example of using Boule to calculate the :term:`normal gravity` of
the WGS84 ellipsoid on the Earth's surface (topography in the continents, the
geoid the oceans):


.. jupyter-execute::

    import boule as bl
    import ensaio
    import pygmt
    import xarray as xr

    # Download and open colocated topography and geoid grids using Ensaio
    fname_topo = ensaio.fetch_earth_topography(version=1)
    fname_geoid = ensaio.fetch_earth_geoid(version=1)
    topography = xr.load_dataarray(fname_topo)
    geoid = xr.load_dataarray(fname_geoid)

    # Define height by combining topography and geoid using xarray
    height = xr.where(
        topography >= 0,
        topography + geoid,  # geometric height of topography in the continents
        geoid,  # geoid height in the oceans
    )

    # Calculate normal gravity
    gamma = bl.WGS84.normal_gravity(topography.latitude, height)

    # Plot a map of it using PyGMT
    fig = pygmt.Figure()
    fig.grdimage(gamma, projection="W20c", cmap="viridis", shading="+a45+nt0.3")
    fig.basemap(frame=["af", "WEsn"])
    fig.colorbar(position="JCB+w10c", frame=["af", 'y+l"mGal"'])
    fig.show()

----

.. grid:: 1 1 2 2
    :margin: 5 5 0 0
    :gutter: 4

    .. grid-item-card:: :octicon:`info` Getting started
        :text-align: center
        :class-title: sd-fs-5
        :class-card: sd-p-3

        New to Boule? Start here!

        .. button-ref:: overview
            :ref-type: ref
            :click-parent:
            :color: primary
            :outline:
            :expand:

    .. grid-item-card:: :octicon:`comment-discussion` Need help?
        :text-align: center
        :class-title: sd-fs-5
        :class-card: sd-p-3

        Ask on our community channels.

        .. button-link:: https://www.fatiando.org/contact
            :click-parent:
            :color: primary
            :outline:
            :expand:

            Join the conversation :octicon:`link-external`

    .. grid-item-card:: :octicon:`file-badge` Reference documentation
        :text-align: center
        :class-title: sd-fs-5
        :class-card: sd-p-3

        A list of modules and functions.

        .. button-ref:: api
            :ref-type: ref
            :color: primary
            :outline:
            :expand:

    .. grid-item-card:: :octicon:`bookmark` Using Boule for research?
        :text-align: center
        :class-title: sd-fs-5
        :class-card: sd-p-3

        Citations help support our work!

        .. button-ref:: citing
            :ref-type: ref
            :color: primary
            :outline:
            :expand:

----

.. admonition:: Boule is ready for use but still changing
    :class: important

    This means that we sometimes break backwards compatibility as we try to
    improve the software based on user experience, new ideas, better design
    decisions, etc. Please keep that in mind before you update Boule to a newer
    version.

    :octicon:`code-review` **We welcome feedback and ideas!** This is a great
    time to bring new ideas on how we can improve the project. `Join the
    conversation <https://www.fatiando.org/contact>`__ or submit `issues on
    GitHub <https://github.com/fatiando/boule/issues>`__.

.. seealso::

    Boule is a part of the
    `Fatiando a Terra <https://www.fatiando.org/>`_ project.




.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: Getting Started

    overview.rst
    install.rst

.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: User Guide

    user_guide/normal_gravity.rst
    user_guide/gravity_disturbance.rst
    user_guide/geodetic_to_geocentric.rst

.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: Reference Documentation

    api/index.rst
    ellipsoids.rst
    citing.rst
    glossary.rst
    references.rst
    changes.rst
    compatibility.rst
    versions.rst

.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: Community

    Join the community <http://contact.fatiando.org>
    How to contribute <https://github.com/fatiando/boule/blob/main/CONTRIBUTING.md>
    Code of Conduct <https://github.com/fatiando/boule/blob/main/CODE_OF_CONDUCT.md>
    Source code on GitHub <https://github.com/fatiando/boule>
    The Fatiando a Terra project <https://www.fatiando.org>
