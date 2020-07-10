.. _changes:

Changelog
=========

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
