.. title:: Home

.. raw:: html

    <h1 class="display-2 text-center">
      Boule
    </h1>

    <p class="lead text-center front-page-callout">
      Reference ellipsoids for geodesy and geophysics
    </p>

*Boule* is Python library for representing reference ellipsoids geometrically,
calculating their gravity fields, and performing some global coordinate
conversions.

The main use cases are:

* Storing and manipulating ellipsoid parameters for spherical harmonic analysis.
* Calculating normal gravity for generating gravity anomalies and disturbances.
* Modelling in spherical coordinates, which requires geodetic to geocentric
  spherical coordinate conversions.

**What's with the name?**
"Boule" is French for "ball" and also a `traditional shape of bread resembling
a squashed ball <https://en.wikipedia.org/wiki/Boule_(bread)>`__ (much like the
Earth).

.. grid:: 1 1 2 2
    :margin: 4 5 0 0
    :gutter: 4

    .. grid-item-card:: :octicon:`info` Getting started
        :text-align: center
        :class-title: sd-fs-5

        New to Boule? Start here!

        .. button-ref:: overview
            :ref-type: ref
            :click-parent:
            :color: primary
            :shadow:

    .. grid-item-card:: :octicon:`comment-discussion` Need help?
        :text-align: center
        :class-title: sd-fs-5

        Ask on our community channels

        .. button-link:: https://www.fatiando.org/contact
            :click-parent:
            :color: primary
            :shadow:

            Join the conversation

    .. grid-item-card:: :octicon:`file-badge` Reference documentation
        :text-align: center
        :class-title: sd-fs-5

        A list of modules and functions

        .. button-ref:: api
            :ref-type: ref
            :color: primary
            :shadow:

    .. grid-item-card:: :octicon:`bookmark` Using Boule for research?
        :text-align: center
        :class-title: sd-fs-5

        Citations help support our work

        .. button-ref:: citing
            :ref-type: ref
            :color: primary
            :shadow:


.. admonition:: Ready for daily use but still changing
    :class: seealso

    This means that we are still adding new features and sometimes we make
    changes to the ones we already have while we try to improve the software
    based on users' experience, test new ideas, take better design decisions,
    etc. Some of these changes could be **backwards incompatible**. Keep that
    in mind before you update Boule to a newer version.

    **We welcome any feedback and ideas!** This is a great time to bring new
    ideas on how we can improve the project, feel free to `join the
    conversation <https://www.fatiando.org/contact>`__ or submit
    `issues on GitHub <https://github.com/fatiando/boule/issues>`__.


.. seealso::

    Boule is a part of the
    `Fatiando a Terra <https://www.fatiando.org/>`_ project.

----

Table of contents
-----------------

.. toctree::
    :maxdepth: 2
    :caption: Getting Started

    tutorials/overview.rst
    install.rst
    citing.rst

.. toctree::
    :maxdepth: 2
    :caption: User Guide

    ellipsoids/index.rst
    tutorials/normal_gravity.rst
    tutorials/gravity_disturbance.rst
    tutorials/geodetic_to_geocentric.rst

.. toctree::
    :maxdepth: 2
    :caption: Reference Documentation

    api/index.rst
    compatibility.rst
    changes.rst
    references.rst
    versions.rst

.. toctree::
    :maxdepth: 2
    :caption: Community

    Join the community <http://contact.fatiando.org>
    How to contribute <https://github.com/fatiando/boule/blob/main/CONTRIBUTING.md>
    Code of Conduct <https://github.com/fatiando/boule/blob/main/CODE_OF_CONDUCT.md>
    Source code on GitHub <https://github.com/fatiando/boule>
    The Fatiando a Terra project <https://www.fatiando.org>
