.. title:: Home

.. raw:: html

    <h1 class="display-2 text-center">
      Boule
    </h1>

    <p class="lead text-center front-page-callout">
      Reference ellipsoids for geodesy and geophysics
    </p>

**Boule** is Python library for representing reference ellipsoids
geometrically, calculating their gravity fields, and performing some global
coordinate conversions.
"Boule" is also French for "ball" as well as a `traditional shape of bread
resembling a squashed ball <https://en.wikipedia.org/wiki/Boule_(bread)>`__
(much like the Earth).

Some examples of where Boule can be applied:

* Storing and manipulating ellipsoid parameters for spherical harmonic analysis.
* Calculating normal gravity for generating gravity anomalies and disturbances.
* Modelling in spherical coordinates, which requires geodetic to geocentric
  spherical coordinate conversions.

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

    tutorials/overview.rst
    install.rst
    citing.rst

.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: User Guide

    ellipsoids/index.rst
    tutorials/normal_gravity.rst
    tutorials/gravity_disturbance.rst
    tutorials/geodetic_to_geocentric.rst

.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: Reference Documentation

    api/index.rst
    compatibility.rst
    changes.rst
    glossary.rst
    references.rst
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
