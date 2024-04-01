# Copyright (c) 2019 The Boule Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Ellipsoid and Sphere realizations for the Earth and other planetary bodies.
"""
import numpy as np

from ._ellipsoid import Ellipsoid
from ._sphere import Sphere
from ._triaxialellipsoid import TriaxialEllipsoid

Mercury2015 = Sphere(
    name="Mercury2015",
    long_name="Mercury spheroid (2015)",
    radius=2_439_372,
    geocentric_grav_const=22.031839224e12,
    angular_velocity=1.2400172589e-6,
    reference=(
        "Wieczorek, MA (2015). 10.05 - Gravity and Topography of the Terrestrial "
        "Planets, Treatise of Geophysics (Second Edition); Elsevier. "
        "doi:10.1016/B978-0-444-53802-4.00169-X"
    ),
)

Mercury2024 = Sphere(
    name="Mercury2024",
    long_name="Mercury spheroid (2023)",
    radius=2439472.7,
    geocentric_grav_const=22031815411154.895,
    angular_velocity=1.2400141739494342e-06,
    reference=(
        "R: Maia, J. (2024). Spherical harmonic models of the shape of "
        "Mercury [Data set]. Zenodo. https://doi.org/10.5281/zenodo.10809345; "
        "GM, OMEGA: Mazarico, E., et al. (2014), The gravity field, "
        "orientation, and ephemeris of Mercury from MESSENGER observations "
        "after three years in orbit, J. Geophys. Res. Planets, 119, "
        "2417-2436, doi:10.1002/2014JE004675."
    ),
)

Venus2015 = Sphere(
    name="Venus2015",
    long_name="Venus spheroid (2015)",
    radius=6_051_878,
    geocentric_grav_const=324.858592e12,
    angular_velocity=-299.24e-9,
    reference=(
        "Wieczorek, MA (2015). 10.05 - Gravity and Topography of the Terrestrial "
        "Planets, Treatise of Geophysics (Second Edition); Elsevier. "
        "doi:10.1016/B978-0-444-53802-4.00169-X"
    ),
)

WGS84 = Ellipsoid(
    name="WGS84",
    long_name="World Geodetic System (1984)",
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
    long_name="Geodetic Reference System (1980)",
    semimajor_axis=6378137,
    flattening=1 / 298.257222101,
    geocentric_grav_const=3986005.0e8,
    angular_velocity=7292115e-11,
    reference=(
        "Hofmann-Wellenhof, B., & Moritz, H. (2006). Physical Geodesy "
        "(2nd, corr. ed. 2006 edition ed.). Wien ; New York: Springer."
    ),
)

EGM96 = Ellipsoid(
    name="EGM96",
    long_name="Earth Gravitational Model (1996)",
    semimajor_axis=6378136.3,
    flattening=1 / 0.298256415099e3,
    geocentric_grav_const=3986004.415e8,
    angular_velocity=7292115e-11,
    reference=(
        "Lemoine, F. G., et al. (1998). The Development of the Joint NASA "
        "GSFC and the National Imagery and Mapping Agency (NIMA) Geopotential "
        "Model EGM96. NASA Goddard Space Flight Center, NASA/TP 1998-206861."
    ),
)

Moon2015 = Sphere(
    name="Moon2015",
    long_name="Moon spheroid (2015)",
    radius=1_737_151,
    geocentric_grav_const=4.90280007e12,
    angular_velocity=2.6617073e-6,
    reference=(
        "Wieczorek, MA (2015). 10.05 - Gravity and Topography of the Terrestrial "
        "Planets, Treatise of Geophysics (Second Edition); Elsevier. "
        "doi:10.1016/B978-0-444-53802-4.00169-X"
    ),
)

Mars2009 = Ellipsoid(
    name="Mars2009",
    long_name="Mars ellipsoid (2009)",
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

Vesta2012_triaxial = TriaxialEllipsoid(
    name="Vesta2012_triaxial",
    long_name="Vesta triaxial ellipsoid (2012)",
    semimajor_axis=286_300,
    semimedium_axis=278_600,
    semiminor_axis=223_200,
    geocentric_grav_const=2.59076e20 * 6.6743e-11,
    angular_velocity=1617.333119 * 2 * np.pi / 360 / 24 / 60 / 60,
    reference=(
        "Russell, C. T., Raymond, C. A., Coradini, A., McSween, H. Y., Zuber, "
        "M. T., Nathues, A., et al. (2012). Dawn at Vesta: Testing the "
        "Protoplanetary Paradigm. Science. doi:10.1126/science.1219381"
    ),
)

Vesta2017 = Ellipsoid(
    name="Vesta2017",
    long_name="Vesta reference ellipsoid (2017)",
    semimajor_axis=278_556,
    flattening=(278_556 - 229_921) / 278_556,
    geocentric_grav_const=17.288e9,
    angular_velocity=3.267e-4,
    reference=(
        "Karimi, R., Azmoudeh Ardalan, A., & Vasheghani Farahani, S. (2017). "
        "The size, shape and orientation of the asteroid Vesta based on data "
        "from the Dawn mission. Earth and Planetary Science Letters, 475, "
        "71–82. https://doi.org/10.1016/j.epsl.2017.07.033"
    ),
)

Vesta2017_triaxial = TriaxialEllipsoid(
    # Note that this triaxial reference ellipsoid is rotated in longitude
    # by 8.29 E with respect to the Vesta coordinate system.
    name="Vesta2017_triaxial",
    long_name="Vesta triaxial reference ellipsoid (2017)",
    semimajor_axis=280_413,
    semimedium_axis=274_572,
    semiminor_axis=231_253,
    geocentric_grav_const=17.288e9,
    angular_velocity=3.267e-4,
    reference=(
        "Karimi, R., Azmoudeh Ardalan, A., & Vasheghani Farahani, S. (2017). "
        "The size, shape and orientation of the asteroid Vesta based on data "
        "from the Dawn mission. Earth and Planetary Science Letters, 475, "
        "71–82. https://doi.org/10.1016/j.epsl.2017.07.033"
    ),
)

Ceres2018 = Ellipsoid(
    name="Ceres2018",
    long_name="Ceres ellipsoid (2018)",
    semimajor_axis=482_100,
    flattening=(482_100 - 445.94) / 482_100,
    geocentric_grav_const=62629053612.1,
    angular_velocity=1.9234038694078873e-4,
    reference=(
        "A, F: Park, R. S., et al. (2019). High-resolution shape model of "
        "Ceres from stereophotoclinometry using Dawn Imaging Data. Icarus, "
        "319, 812–827. https://doi.org/10.1016/j.icarus.2018.10.024; "
        "GM, OMEGA: Konopliv, A. S., et al. (2018). The Ceres gravity field, "
        "spin pole, rotation period and orbit from the Dawn radiometric "
        "tracking and optical data. Icarus, 299, 411–429. "
        "https://doi.org/10.1016/j.icarus.2017.08.005"
    ),
)
