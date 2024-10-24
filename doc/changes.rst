.. _changes:

Changelog
=========

Version 0.5.0
-------------

Released on: 2024/10/22

doi: https://doi.org/10.5281/zenodo.13975491

Breaking changes:

-  Drop support for Python 3.7 (`#188 <https://github.com/fatiando/boule/pull/188>`__)

New features:

-  Add ``geocentric_radius`` to ``TriaxialEllipsoid`` (`#146 <https://github.com/fatiando/boule/pull/146>`__)
-  Add a ``volume`` property for the Sphere (`#152 <https://github.com/fatiando/boule/pull/152>`__)
-  Add ``mass``, ``mean_density``, and ``volume_equivalent_radius`` properties to classes (`#173 <https://github.com/fatiando/boule/pull/173>`__)
-  Add true mean radius for ``Sphere``, ``Ellipsoid`` and ``TriaxialEllipsoid`` (`#177 <https://github.com/fatiando/boule/pull/177>`__)
-  Add ``area`` and ``area_equivalent_radius`` to all three ellipsoid classes (`#178 <https://github.com/fatiando/boule/pull/178>`__)
-  Add new planetary ellipsoids and new naming scheme (`#180 <https://github.com/fatiando/boule/pull/180>`__)
-  Add attributes for the normal potential to ``Sphere`` and ``Ellipsoid`` (`#184 <https://github.com/fatiando/boule/pull/184>`__)
-  Add ``normal_gravitational_potential``, ``normal_gravity_potential``, and ``centrifugal_potential`` methods to ``Ellipsoid`` and ``Sphere`` classes (`#187 <https://github.com/fatiando/boule/pull/187>`__)
-  Add the ``semimedium_axis`` and ``semimajor_axis_longitude`` to the Sphere and Ellipsoid classes for compatibility with the ``TriaxialEllipsoid`` (`#192 <https://github.com/fatiando/boule/pull/192>`__)
-  Add ``__str__`` method to Ellipsoid classes (`#213 <https://github.com/fatiando/boule/pull/213>`__)

Maintenance:

-  Extend support for Python 3.11 (`#147 <https://github.com/fatiando/boule/pull/147>`__)
-  Add Blazej Bucha to ``AUTHORS.md`` (`#148 <https://github.com/fatiando/boule/pull/148>`__)
-  Update Leo’s affiliation from Liverpool to São Paulo (`#149 <https://github.com/fatiando/boule/pull/149>`__)
-  Update Black format to version 24.2 (`#150 <https://github.com/fatiando/boule/pull/150>`__)
-  Use Burocrata to check/add license notices (`#153 <https://github.com/fatiando/boule/pull/153>`__)
-  Use Dependabot to manage updates to GitHub Actions (`#154 <https://github.com/fatiando/boule/pull/154>`__)
-  Use Trusted Publisher to deploy to PyPI (`#160 <https://github.com/fatiando/boule/pull/160>`__)
-  Move package configuration to ``pyproject.toml`` (`#171 <https://github.com/fatiando/boule/pull/171>`__)
-  Add link to Leo’s ORCID (`#190 <https://github.com/fatiando/boule/pull/190>`__)
-  Extend support to Python 3.12 (`#189 <https://github.com/fatiando/boule/pull/189>`__)
-  Run tests with oldest dependencies on x86 macos (`#200 <https://github.com/fatiando/boule/pull/200>`__)
-  Replace ``_version_generated.py`` for ``_version.py`` (`#199 <https://github.com/fatiando/boule/pull/199>`__)
-  Move push to codecov to its own job in Actions (`#203 <https://github.com/fatiando/boule/pull/203>`__)
-  Update how output variables are stored in Actions (`#206 <https://github.com/fatiando/boule/pull/206>`__)
-  Replace ``build`` for ``python-build`` in environment.yml (`#207 <https://github.com/fatiando/boule/pull/207>`__)

Documentation:

-  Update the version of Sphinx and its plugins (`#170 <https://github.com/fatiando/boule/pull/170>`__)
-  Fix typo in installation instructions (`#172 <https://github.com/fatiando/boule/pull/172>`__)
-  Update coordinate conversions web documentation (`#212 <https://github.com/fatiando/boule/pull/212>`__)
-  Replace sphinx napoleon for numpydoc (`#195 <https://github.com/fatiando/boule/pull/195>`__)

This release contains contributions from:

-  Leonardo Uieda
-  Mark Wieczorek
-  Santiago Soler
-  Blazej Bucha


Version 0.4.1
-------------

Released on: 2022/10/27

doi: https://doi.org/10.5281/zenodo.7258175

Documentation:

* Update contact link in the docs side bar (`#141 <https://github.com/fatiando/boule/pull/141>`__)
* Add definition of “co-located grids” to the glossary (`#139 <https://github.com/fatiando/boule/pull/139>`__)
* Fix typo in overview docs page (`#137 <https://github.com/fatiando/boule/pull/137>`__)

Maintenance:

* Undo deprecation of coordinate conversion methods (`#142 <https://github.com/fatiando/boule/pull/142>`__)
* Drop support for Python 3.6 (`#144 <https://github.com/fatiando/boule/pull/144>`__)
* Add ``serve`` target in ``doc/Makefile`` (`#136 <https://github.com/fatiando/boule/pull/136>`__)

This release contains contributions from:

* Mariana Gomez
* Santiago Soler
* Leonardo Uieda

Version 0.4.0
-------------

Released on: 2022/08/09

doi: https://doi.org/10.5281/zenodo.6779998

.. warning::

    **Boule v0.4.0 is the last release that is compatible with Python 3.6.**

**Backwards incompatible changes:**

* Refactor the ``Sphere`` class to not inherit from ``Ellipsoid``. Breaks backwards compatibility due to the removal of inherited methods and attributes (`#129 <https://github.com/fatiando/boule/pull/129>`__)
* Make all package modules private by adding a leading ``_`` to their name (`#119 <https://github.com/fatiando/boule/pull/119>`__)
* Rename the ``Ellipsoid.emm`` attribute to ``Ellipsoid._emm`` to make it private (`#123 <https://github.com/fatiando/boule/pull/123>`__)
* Remove the ``boule.test`` function (`#116 <https://github.com/fatiando/boule/pull/116>`__)

Deprecations:

* Deprecate the coordinate conversion methods which have been ported to the pymap3d library v2.9.0 (`#126 <https://github.com/fatiando/boule/pull/126>`__)

New features:

* Add the ``volume`` property to ``Ellipsoid`` (`#132 <https://github.com/fatiando/boule/pull/132>`__)
* Add missing attributes to ``Ellipsoid`` for pymap3 compatibility (`#121 <https://github.com/fatiando/boule/pull/121>`__)
* Add the ``TriaxialEllipsoid`` class with geometric parameters (`#72 <https://github.com/fatiando/boule/pull/72>`__)
* Add a normal gravitation method to ``Sphere`` (`#73 <https://github.com/fatiando/boule/pull/73>`__)

Documentation:

* Add a logo for Boule (`#125 <https://github.com/fatiando/boule/pull/125>`__)
* Refactor the documentation tutorials to shift the focus to how to do things with Boule and point to other pages for more of the theory (`#130 <https://github.com/fatiando/boule/pull/130>`__)
* Refactor documentation of ``TriaxialEllipsoid`` (`#128 <https://github.com/fatiando/boule/pull/128>`__)
* Refactor the documentation of ``Ellipsoid`` (`#127 <https://github.com/fatiando/boule/pull/127>`__)
* Fix formatting for code to pip install from GitHub (`#118 <https://github.com/fatiando/boule/pull/118>`__)
* Fix license link and compatibility warning in the README (`#117 <https://github.com/fatiando/boule/pull/117>`__)
* Use jupyter-sphinx instead of sphinx-gallery and update the documentation front page (`#112 <https://github.com/fatiando/boule/pull/112>`__)
* Point to our organization wide guides in the documentation (`#108 <https://github.com/fatiando/boule/pull/108>`__)
* Add an example calculating global gravity disturbances (`#102 <https://github.com/fatiando/boule/pull/102>`__)
* Update Sphinx version to 4.5.0 (`#103 <https://github.com/fatiando/boule/pull/103>`__)

Maintenance:

* Convert the README to Markdown (`#113 <https://github.com/fatiando/boule/pull/113>`__)
* Specify oldest supported version of each dependency (`#111 <https://github.com/fatiando/boule/pull/111>`__)
* Move to ``pyproject.toml/setup.cfg`` with ``build`` instead of ``setup.py`` (`#110 <https://github.com/fatiando/boule/pull/110>`__)
* Replace pylint with flake8 and some extensions (`#109 <https://github.com/fatiando/boule/pull/109>`__)
* Rename the git "master" branch to "main" (`#107 <https://github.com/fatiando/boule/pull/107>`__)
* Update code style to Black 22.3.0 (`#104 <https://github.com/fatiando/boule/pull/104>`__)
* Replace Google Analytics with Plausible for page visit statistics (`#99 <https://github.com/fatiando/boule/pull/99>`__)

This release contains contributions from:

* Agustina Pesce
* Chris Dinneen
* Leonardo Uieda
* Santiago Soler

Version 0.3.1
-------------

Released on: 2021/10/19

doi:`10.5281/zenodo.5577885 <https://doi.org/10.5281/zenodo.5577885>`__

Bug fix:

* Package the missing ``requirements.txt`` file in source distributions (`#96 <https://github.com/fatiando/boule/pull/96>`__)

This release contains contributions from:

* Leonardo Uieda

Version 0.3.0
-------------

Released on: 2021/10/18

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

Released on: 2020/07/10

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

Released on: 2020/01/10

This release contains only a documentation fix: include install instructions
for conda and pip. No functionality has been changed (hence, no DOI was
issued).

Version 0.1.0
-------------

Released on: 2020/01/10

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

Released on: 2019/11/06

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3530750.svg
    :alt: Digital Object Identifier
    :target: https://doi.org/10.5281/zenodo.3530750

This release is a placeholder that serves as a marker for the start of this
project. It is used to register the project on PyPI and test the continuous
integration deployment process.
