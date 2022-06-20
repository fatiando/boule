<img src="https://github.com/fatiando/boule/raw/main/doc/_static/readme-banner.png" alt="Boule">

<h2 align="center">Reference ellipsoids for geodesy and geophysics</h2>

<p align="center">
<a href="https://www.fatiando.org/boule"><strong>Documentation</strong> (latest)</a> •
<a href="https://www.fatiando.org/boule/dev"><strong>Documentation</strong> (main branch)</a> •
<a href="https://github.com/fatiando/boule/blob/main/CONTRIBUTING.md"><strong>Contributing</strong></a> •
<a href="https://www.fatiando.org/contact/"><strong>Contact</strong></a>
</p>

<p align="center">
Part of the <a href="https://www.fatiando.org"><strong>Fatiando a Terra</strong></a> project
</p>

<p align="center">
<a href="https://pypi.python.org/pypi/boule"><img src="http://img.shields.io/pypi/v/boule.svg?style=flat-square" alt="Latest version on PyPI"></a>
<a href="https://github.com/conda-forge/boule-feedstock"><img src="https://img.shields.io/conda/vn/conda-forge/boule.svg?style=flat-square" alt="Latest version on conda-forge"></a>
<a href="https://codecov.io/gh/fatiando/boule"><img src="https://img.shields.io/codecov/c/github/fatiando/boule/main.svg?style=flat-square" alt="Test coverage status"></a>
<a href="https://pypi.python.org/pypi/boule"><img src="https://img.shields.io/pypi/pyversions/boule.svg?style=flat-square" alt="Compatible Python versions."></a>
<a href="https://doi.org/10.5281/zenodo.3530749"><img src="https://img.shields.io/badge/doi-10.5281%2Fzenodo.3530749-blue?style=flat-square" alt="DOI used to cite Boule"></a>
</p>

## About

**Boule** is Python library for representing
[reference ellipsoids](https://en.wikipedia.org/wiki/Reference_ellipsoid),
calculating their gravity fields, and performing some global coordinate
conversions.
"Boule" is also French for "ball" as well as a
[traditional shape of bread resembling a squashed ball](https://en.wikipedia.org/wiki/Boule_(bread)).

Some examples of where Boule can be applied:

* Storing and manipulating ellipsoid parameters for spherical harmonic analysis.
* Calculating normal gravity for generating gravity anomalies and disturbances.
* Modelling in spherical coordinates, which requires geodetic to geocentric
  spherical coordinate conversions.

## Project goals

* Provide a representation of ellipsoid parameters and derived quantities,
  including units and citations.
* Convert between geodetic coordinates and geocentric spherical, topocentric,
  etc.
* Calculate the gravity, gravitational, and centrifugal potential (and its
  derivatives) of ellipsoids in closed form.
* Include a range ellipsoids for the Earth and other planetary bodies.

## Project status

**Boule is ready for use but still changing.**
This means that we sometimes break backwards compatibility as we try to
improve the software based on user experience, new ideas, better design
decisions, etc. Please keep that in mind before you update Boule to a newer
version.

**We welcome feedback and ideas!** This is a great time to bring new ideas on
how we can improve the project.
[Join the conversation](https://www.fatiando.org/contact) or submit
[issues on GitHub](https://github.com/fatiando/boule/issues).

## Getting involved

🗨️ **Contact us:**
Find out more about how to reach us at
[fatiando.org/contact](https://www.fatiando.org/contact/).

👩🏾‍💻 **Contributing to project development:**
Please read our
[Contributing Guide](https://github.com/fatiando/boule/blob/main/CONTRIBUTING.md)
to see how you can help and give feedback.

🧑🏾‍🤝‍🧑🏼 **Code of conduct:**
This project is released with a
[Code of Conduct](https://github.com/fatiando/community/blob/main/CODE_OF_CONDUCT.md).
By participating in this project you agree to abide by its terms.

> **Imposter syndrome disclaimer:**
> We want your help. **No, really.** There may be a little voice inside your
> head that is telling you that you're not ready, that you aren't skilled
> enough to contribute. We assure you that the little voice in your head is
> wrong. Most importantly, **there are many valuable ways to contribute besides
> writing code**.
>
> *This disclaimer was adapted from the*
> [MetPy project](https://github.com/Unidata/MetPy).

## License

This is free software: you can redistribute it and/or modify it under the terms
of the **BSD 3-clause License**. A copy of this license is provided in
[`LICENSE.txt`](https://github.com/fatiando/boule/blob/main/LICENSE.txt).
