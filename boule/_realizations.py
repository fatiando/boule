# Copyright (c) 2019 The Boule Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Ellipsoid and Sphere realizations for the Earth and other planetary bodies.
"""
from ._ellipsoid import Ellipsoid
from ._sphere import Sphere
from ._triaxialellipsoid import TriaxialEllipsoid

WGS84 = Ellipsoid(
    name="WGS84",
    long_name="World Geodetic System 1984",
    semimajor_axis=6378137,
    flattening=1 / 298.257223563,
    geocentric_grav_const=3986004.418e8,
    angular_velocity=7292115e-11,
    reference=(
        "Hofmann-Wellenhof, B., & Moritz, H. (2006). Physical Geodesy "
        "(2nd, corr. ed. 2006 edition ed.). Wien ; New York: Springer."
    ),
)


GRS80 = Ellipsoid(
    name="GRS80",
    long_name="Geodetic Reference System 1980",
    semimajor_axis=6378137,
    flattening=1 / 298.257222101,
    geocentric_grav_const=3986005.0e8,
    angular_velocity=7292115e-11,
    reference=(
        "Hofmann-Wellenhof, B., & Moritz, H. (2006). Physical Geodesy "
        "(2nd, corr. ed. 2006 edition ed.). Wien ; New York: Springer."
    ),
)


MARS = Ellipsoid(
    name="MARS",
    long_name="Mars Ellipsoid",
    semimajor_axis=3_395_428,
    flattening=(3_395_428 - 3_377_678) / 3_395_428,
    geocentric_grav_const=42828.372e9,
    angular_velocity=7.0882181e-5,
    reference=(
        "Ardalan, A. A., Karimi, R., & Grafarend, E. W. (2009). A New Reference "
        "Equipotential Surface, and Reference Ellipsoid for the Planet Mars. "
        "Earth, Moon, and Planets, 106(1), 1. "
        "doi:10.1007/s11038-009-9342-7"
    ),
)

VENUS = Sphere(
    name="VENUS",
    long_name="Venus Spheroid",
    radius=6_051_878,
    geocentric_grav_const=324.858592e12,
    angular_velocity=-299.24e-9,
    reference=(
        "Wieczorek, MA (2015). 10.05 - Gravity and Topography of the Terrestrial "
        "Planets, Treatise of Geophysics (Second Edition); Elsevier. "
        "doi:10.1016/B978-0-444-53802-4.00169-X"
    ),
)

MOON = Sphere(
    name="MOON",
    long_name="Moon Spheroid",
    radius=1_737_151,
    geocentric_grav_const=4.90280007e12,
    angular_velocity=2.6617073e-6,
    reference=(
        "Wieczorek, MA (2015). 10.05 - Gravity and Topography of the Terrestrial "
        "Planets, Treatise of Geophysics (Second Edition); Elsevier. "
        "doi:10.1016/B978-0-444-53802-4.00169-X"
    ),
)

MERCURY = Sphere(
    name="MERCURY",
    long_name="Mercury Spheroid",
    radius=2_439_372,
    geocentric_grav_const=22.031839221e12,
    angular_velocity=1.2400172589e-6,
    reference=(
        "Wieczorek, MA (2015). 10.05 - Gravity and Topography of the Terrestrial "
        "Planets, Treatise of Geophysics (Second Edition); Elsevier. "
        "doi:10.1016/B978-0-444-53802-4.00169-X"
    ),
)

VESTA = TriaxialEllipsoid(
    name="VESTA",
    long_name="Vesta Triaxial Ellipsoid",
    semimajor_axis=286_300,
    semimedium_axis=278_600,
    semiminor_axis=223_200,
    geocentric_grav_const=1.729094e10,
    angular_velocity=326.71050958367e-6,
    reference=(
        "Russell, C. T., Raymond, C. A., Coradini, A., McSween, H. Y., Zuber, "
        "M. T., Nathues, A., et al. (2012). Dawn at Vesta: Testing the "
        "Protoplanetary Paradigm. Science. doi:10.1126/science.1219381"
    ),
)
