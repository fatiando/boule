.. _changes:

Changelog
=========

Version 0.3.0
-------------

*Released on: 2021/10/18*

doi:`10.5281/zenodo.5575827 <https://doi.org/10.5281/zenodo.5575827>`__

Highlights:

* Add support for Python 3.9 and 3.10 (`#87 <https://github.com/fatiando/boule/pull/87>`__)
* Add reference ``Sphere`` class for bodies with zero flattening (`#42 <https://github.com/fatiando/boule/pull/42>`__)
* Add spheroids for Venus (`#68 <https://github.com/fatiando/boule/pull/68>`__), Mercury, and the Earth's Moon (`#71 <https://github.com/fatiando/boule/pull/71>`__)

Enhancements:

* Warn users if normal gravity is being computed on internal point (`#83 <https://github.com/fatiando/boule/pull/83>`__)
* Add option to return normal gravity in SI units (`#69 <https://github.com/fatiando/boule/pull/69>`__)
* Add parameter validation for the ``Sphere`` class (`#56 <https://github.com/fatiando/boule/pull/56>`__)
* Add parameter validation for the ``Ellipsoid`` class (`#45 <https://github.com/fatiando/boule/pull/45>`__)
* Make parameter validation methods private (`#55 <https://github.com/fatiando/boule/pull/55>`__)
* Tests normal gravity against Somigliana equation (`#51 <https://github.com/fatiando/boule/pull/51>`__)
* Fix normal gravity equation of ``Sphere`` (`#52 <https://github.com/fatiando/boule/pull/52>`__)
* Fix missing centrifugal term for spheres at the equator (`#48 <https://github.com/fatiando/boule/pull/48>`__)

Documentation:

* Update documentation theme to sphinx-book-theme (`#92 <https://github.com/fatiando/boule/pull/92>`__)
* Add tutorial for geodetic to geocentric coordinate transformations (`#84 <https://github.com/fatiando/boule/pull/84>`__)
* Improvements to docstrings of Ellipsoid and Sphere (`#49 <https://github.com/fatiando/boule/pull/49>`__)

Maintenance:

* Add Mariana Gomez to ``AUTHORS.md`` (`#90 <https://github.com/fatiando/boule/pull/90>`__)
* Add Chris Dinneen to ``AUTHORS.md`` (`#74 <https://github.com/fatiando/boule/pull/74>`__)
* Only run CI for Python 3.6 and 3.10 now that it's out (`#89 <https://github.com/fatiando/boule/pull/89>`__)
* Update ``setuptools_scm`` configuration to save a ``boule/_version.py`` file instead of relying on ``pkg_resources`` to get the version number (`#91 <https://github.com/fatiando/boule/pull/91>`__)
* Use the OSI version of item 3 in the license (`#70 <https://github.com/fatiando/boule/pull/70>`__)
* Add license and copyright notice to every ``.py`` file (`#67 <https://github.com/fatiando/boule/pull/67>`__)
* Refactor GitHub Actions workflows to separate building the docs (`#65 <https://github.com/fatiando/boule/pull/65>`__)
* Replace versioneer with setuptools-scm (`#61 <https://github.com/fatiando/boule/pull/61>`__)
* Remove configuration files for unused CI (`#60 <https://github.com/fatiando/boule/pull/60>`__)
* Replace Travis and Azure with GitHub Actions (`#57 <https://github.com/fatiando/boule/pull/57>`__)
* Add conda-forge badge to the README (`#40 <https://github.com/fatiando/boule/pull/40>`__)
* Format the ``doc/conf.py`` file with Black (`#41 <https://github.com/fatiando/boule/pull/41>`__)

This release contains contributions from:

* Chris Dinneen
* Mariana Gomez
* Hugo van Kemenade
* Lu Li
* Santiago Soler
* Leonardo Uieda

Version 0.2.0
-------------

*Released on: 2020/07/10*

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3939204.svg
    :alt: Digital Object Identifier
    :target: https://doi.org/10.5281/zenodo.3939204

* Add the ``Ellipsoid.geocentric_radius`` method to calculate the distance from the center of the ellipsoid to its surface as a function of latitude (geodetic or geocentric). (`#37 <https://github.com/fatiando/boule/pull/37>`__)
* Add the ``Ellipsoid.prime_vertical_radius`` method for computing the prime vertical radius (usually represented by N in equations) as a function of geodetic latitude. (`#35 <https://github.com/fatiando/boule/pull/35>`__)
* Fix typo in README contributing section (`#32 <https://github.com/fatiando/boule/pull/32>`__)

This release contains contributions from:

* Leonardo Uieda
* Rowan Cockett
* Santiago Soler

Version 0.1.1
-------------

*Released on: 2020/01/10*

This release contains only a documentation fix: include install instructions
for conda and pip. No functionality has been changed (hence, no DOI was
issued).

Version 0.1.0
-------------

*Released on: 2020/01/10*

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3603997.svg
    :alt: Digital Object Identifier
    :target: https://doi.org/10.5281/zenodo.3603997

First release of *Boule* including basic functionality:

* Definition of the ``Ellipsoid`` class: based on the semi-major axis,
  flattening, geocentric gravitational constant, and angular velocity. Other
  quantities are derived from these 4.
* Computation of normal gravity and coordinate conversions between geodetic and
  geocentric.
* Ellipsoid realizations for the Earth (WGS84 and GRS80) and Mars.

Version 0.0.1
-------------

*Released on: 2019/11/06*

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3530750.svg
    :alt: Digital Object Identifier
    :target: https://doi.org/10.5281/zenodo.3530750

This release is a placeholder that serves as a marker for the start of this
project. It is used to register the project on PyPI and test the continuous
integration deployment process.
