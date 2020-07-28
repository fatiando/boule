Boule
=====

    Reference ellipsoids for geodesy, geophysics, and coordinate calculations

`Documentation <https://www.fatiando.org/boule>`__ |
`Documentation (dev version) <https://www.fatiando.org/boule/dev>`__ |
`Contact <http://contact.fatiando.org>`__ |
Part of the `Fatiando a Terra <https://www.fatiando.org>`__ project

.. image:: http://img.shields.io/pypi/v/boule.svg?style=flat-square
    :alt: Latest version on PyPI
    :target: https://pypi.python.org/pypi/boule
.. image:: http://img.shields.io/travis/fatiando/boule/master.svg?style=flat-square&label=TravisCI
    :alt: TravisCI build status
    :target: https://travis-ci.org/fatiando/boule
.. image:: https://img.shields.io/codecov/c/github/fatiando/boule/master.svg?style=flat-square
    :alt: Test coverage status
    :target: https://codecov.io/gh/fatiando/boule
.. image:: https://img.shields.io/pypi/pyversions/boule.svg?style=flat-square
    :alt: Compatible Python versions.
    :target: https://pypi.python.org/pypi/boule
.. image:: https://img.shields.io/badge/doi-10.5281%2Fzenodo.3530749-blue.svg?style=flat-square
    :alt: Digital Object Identifier
    :target: https://doi.org/10.5281/zenodo.3530749


.. placeholder-for-doc-index


Disclaimer
----------

🚨 **This package is in early stages of design and implementation.** 🚨

We welcome any feedback and ideas!
Let us know by submitting
`issues on Github <https://github.com/fatiando/boule/issues>`__
or send us a message on our
`Slack chatroom <http://contact.fatiando.org>`__.


About
-----

*Boule* is Python library for representing `Reference Ellipsoids
<https://en.wikipedia.org/wiki/Reference_ellipsoid>`__, calculating their
gravity fields, and converting coordinates defined on the ellipsoids.

The main use cases are:

* Calculating normal gravity (for gravity anomalies and disturbances).
* Spherical gravity modeling, which requires geodetic to geocentric spherical
  coordinate conversions.
* Input ellipsoid parameters for spherical harmonic analysis.

Boule is French for "ball" and also a `traditional shape of bread resembling a
squashed ball <https://en.wikipedia.org/wiki/Boule_(bread)>`__ (much like the
Earth).


Project goals
-------------

* Provide a representation of ellipsoid parameters and derived quantities,
  including units and citations.
* Convert between geodetic coordinates and geocentric spherical, topocentric,
  etc.
* Calculate the gravity, gravitational, and centrifugal potential (and its
  derivatives) of ellipsoids in closed form.
* Include a range ellipsoids for the Earth and other planetary bodies.


Contacting Us
-------------

* Most discussion happens `on Github <https://github.com/fatiando/boule>`__.
  Feel free to `open an issue
  <https://github.com/fatiando/boule/issues/new>`__ or comment
  on any open issue or pull request.
* We have `chat room on Slack <http://contact.fatiando.org>`__
  where you can ask questions and leave comments.


Contributing
------------

Code of conduct
+++++++++++++++

Please note that this project is released with a
`Contributor Code of Conduct <https://github.com/fatiando/boule/blob/master/CODE_OF_CONDUCT.md>`__.
By participating in this project you agree to abide by its terms.

Contributing Guidelines
+++++++++++++++++++++++

Please read our
`Contributing Guide <https://github.com/fatiando/boule/blob/master/CONTRIBUTING.md>`__
to see how you can help and give feedback.

Imposter syndrome disclaimer
++++++++++++++++++++++++++++

**We want your help.** No, really.

There may be a little voice inside your head that is telling you that you're
not ready to be an open source contributor; that your skills aren't nearly good
enough to contribute.
What could you possibly offer?

We assure you that the little voice in your head is wrong.

**Being a contributor doesn't just mean writing code**.
Equally important contributions include:
writing or proof-reading documentation, suggesting or implementing tests, or
even giving feedback about the project (including giving feedback about the
contribution process).
If you're coming to the project with fresh eyes, you might see the errors and
assumptions that seasoned contributors have glossed over.
If you can write any code at all, you can contribute code to open source.
We are constantly trying out new skills, making mistakes, and learning from
those mistakes.
That's how we all improve and we are happy to help others learn.

*This disclaimer was adapted from the*
`MetPy project <https://github.com/Unidata/MetPy>`__.


License
-------

This is free software: you can redistribute it and/or modify it under the terms
of the **BSD 3-clause License**. A copy of this license is provided in
`LICENSE.txt <https://github.com/fatiando/boule/blob/master/LICENSE.txt>`__.


Documentation for other versions
--------------------------------

* `Development <http://www.fatiando.org/boule/dev>`__ (reflects the *master* branch on
  Github)
* `Latest release <http://www.fatiando.org/boule/latest>`__
* `v0.2.0 <http://www.fatiando.org/boule/v0.2.0>`__
* `v0.1.1 <http://www.fatiando.org/boule/v0.1.1>`__
* `v0.1.0 <http://www.fatiando.org/boule/v0.1.0>`__
* `v0.0.1 <http://www.fatiando.org/boule/v0.0.1>`__
