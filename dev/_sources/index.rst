.. title:: Home

.. grid::
    :gutter: 2 3 3 3
    :margin: 5 5 0 0
    :padding: 0 0 0 0

    .. grid-item::
        :columns: 12 8 8 8

        .. raw:: html

            <h1 class="display-1">Boule</h1>

        .. div:: sd-fs-3

            Reference ellipsoids for geodesy and geophysics

    .. grid-item::
        :columns: 12 4 4 4

        .. image:: ./_static/boule-logo.svg
            :width: 200px
            :class: sd-m-auto dark-light

**Boule** is Python library for representing
:term:`reference ellipsoids <reference ellipsoid>` geometrically, calculating
their gravity fields, and performing some global coordinate conversions.
"Boule" is also French for "ball" as well as a `traditional shape of bread
resembling a squashed ball <https://en.wikipedia.org/wiki/Boule_(bread)>`__
(much like the Earth).

Boule is designed for:

* Storing and manipulating :ref:`ellipsoid parameters <defining_ellipsoids>` for spherical harmonic analysis
  and :ref:`coordinate system conversions <coordinates>`.
* Calculating :ref:`normal gravity <normal_gravity>` for generating gravity anomalies and
  :ref:`gravity disturbances <gravity_disturbance>`.

.. seealso::

    Boule is a part of the
    `Fatiando a Terra <https://www.fatiando.org/>`_ project.


.. grid:: 1 2 1 2
    :margin: 5 5 0 0
    :padding: 0 0 0 0
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

Project status
--------------

**Boule is ready for use but still changing.**
This means that we sometimes break backwards compatibility as we try to
improve the software based on user experience, new ideas, better design
decisions, etc. Please keep that in mind before you update Boule to a newer
version.

**We welcome feedback and ideas!** This is a great time to bring new ideas on
how we can improve the project.
`Join the conversation <https://www.fatiando.org/contact>`__ or submit
`issues on GitHub <https://github.com/fatiando/boule/issues>`__.

Getting involved
----------------

🗨️ **Contact us:**
Find out more about how to reach us at
`fatiando.org/contact <https://www.fatiando.org/contact/>`__.

👩🏾‍💻 **Contributing to project development:**
Please read our
`Contributing Guide <https://github.com/fatiando/boule/blob/main/CONTRIBUTING.md>`__
to see how you can help and give feedback.

🤖 **Policy on AI usage:**
Please read our
`AI Usage Policy <https://github.com/fatiando/community/blob/main/AI.md>`__.

🧑🏾‍🤝‍🧑🏼 **Code of conduct:**
This project is released with a
`Code of Conduct <https://github.com/fatiando/community/blob/main/lODE_OF_CONDUCT.md>`__.
By participating in this project you agree to abide by its terms.

    **Imposter syndrome disclaimer:**
    We want your help. **No, really.** There may be a little voice inside your
    head that is telling you that you're not ready, that you aren't skilled
    enough to contribute. We assure you that the little voice in your head is
    wrong. Most importantly, **there are many valuable ways to contribute besides
    writing code** (giving feedback, teaching, writing documentation, and more).

    *This disclaimer was adapted from the*
    `MetPy project <https://github.com/Unidata/MetPy>`__.

License
-------

This is free software: you can redistribute it and/or modify it under the terms
of the **BSD 3-clause License**. A copy of this license is provided in
`LICENSE.txt <https://github.com/fatiando/boule/blob/main/LICENSE.txt>`__.


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
    user_guide/coordinates.rst
    user_guide/defining_ellipsoids.rst

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

    Join our community <https://www.fatiando.org/contact>
    How to contribute <https://github.com/fatiando/boule/blob/main/CONTRIBUTING.md>
    Code of Conduct <https://github.com/fatiando/boule/blob/main/CODE_OF_CONDUCT.md>
    Authors <https://github.com/fatiando/boule/blob/main/AUTHORS.md>
    The Fatiando a Terra project <https://www.fatiando.org>

.. toctree::
    :maxdepth: 2
    :hidden:
    :caption: Code and packages

    GitHub <https://github.com/fatiando/boule>
    PyPI <https://pypi.python.org/pypi/boule>
    conda-forge <https://github.com/conda-forge/boule-feedstock>
    Zenodo <https://doi.org/10.5281/zenodo.3530749>
