# Copyright (c) 2019 The Boule Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
"""
Ellipsoid, Sphere and Triaxialellipsoid realizations for the Earth and other
planetary bodies.
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
        "https://doi.org/10.1016/B978-0-444-53802-4.00169-X"
    ),
)

Mercury2024 = Sphere(
    name="Mercury2024",
    long_name="Mercury spheroid (2024)",
    radius=2_439_472.7,
    geocentric_grav_const=22031815411154.895,
    angular_velocity=1.2400141739494342e-06,
    reference=(
        "Radius: Maia, J. (2024). Spherical harmonic models of the shape of "
        "Mercury [Data set]. Zenodo. https://doi.org/10.5281/zenodo.10809345"
        "\n"
        "GM, angular velocity: Mazarico, E., et al. (2014), The gravity field, "
        "orientation, and ephemeris of Mercury from MESSENGER observations "
        "after three years in orbit, J. Geophys. Res. Planets, 119, "
        "2417-2436. https://doi.org/10.1002/2014JE004675"
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
        "https://doi.org/10.1016/B978-0-444-53802-4.00169-X"
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
        "(2nd, corr. ed. 2006 edition ed.). Wien; New York: Springer."
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
        "(2nd, corr. ed. 2006 edition ed.). Wien; New York: Springer."
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
        "https://doi.org/10.1016/B978-0-444-53802-4.00169-X"
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
        "Earth, Moon, and Planets, 106, 1-13. "
        "https://doi.org/10.1007/s11038-009-9342-7"
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
        "Semimajor axis, flattening: Park, R. S., et al. (2019). High-resolution "
        "shape model of Ceres from stereophotoclinometry using Dawn Imaging Data. "
        "Icarus, 319, 812–827. https://doi.org/10.1016/j.icarus.2018.10.024"
        "\n"
        "GM, angular velocity: Konopliv, A. S., et al. (2018). The Ceres gravity "
        "field, spin pole, rotation period and orbit from the Dawn radiometric "
        "tracking and optical data. Icarus, 299, 411–429. "
        "https://doi.org/10.1016/j.icarus.2017.08.005"
    ),
    comments="Geocentric ellipsoid with aligned semiminor and rotation axes",
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
    comments="Geocentric biaxial ellipsoid",
)

VestaTriaxial2017 = TriaxialEllipsoid(
    name="VestaTriaxial2017",
    long_name="Vesta triaxial reference ellipsoid (2017)",
    semimajor_axis=280_413,
    semimedium_axis=274_572,
    semiminor_axis=231_253,
    geocentric_grav_const=17.288e9,
    angular_velocity=3.267e-4,
    semimajor_axis_longitude=8.29,
    reference=(
        "Karimi, R., Azmoudeh Ardalan, A., & Vasheghani Farahani, S. (2017). "
        "The size, shape and orientation of the asteroid Vesta based on data "
        "from the Dawn mission. Earth and Planetary Science Letters, 475, "
        "71–82. https://doi.org/10.1016/j.epsl.2017.07.033"
    ),
    comments="Geocentric triaxial ellipsoid",
)

Io2024 = TriaxialEllipsoid(
    name="Io2024",
    long_name="Io equilibrium triaxial ellipsoid (2024)",
    semimajor_axis=1_829_700,
    semimedium_axis=1_819_200,
    semiminor_axis=1_815_800,
    geocentric_grav_const=5959.91e9,
    angular_velocity=2 * np.pi / (1.762732 * 24 * 60 * 60),
    reference=(
        "Semi-axis: Thomas, P. C., et al. (1998). The Shape of Io from Galileo "
        "Limb Measurements. Icarus, 135(1), 175–180. "
        "https://doi.org/10.1006/icar.1998.5987"
        "\n"
        "GM: Anderson, J. D., et al. (2001). Io's gravity field and interior "
        "structure. J. Geophys. Res., 106, 32963–32969. "
        "https://doi.org/10.1029/2000JE001367"
        "\n"
        "Angular velocity: R. A. Jacobson (2021), The Orbits of the Regular "
        "Jovian Satellites and the Orientation of the Pole of Jupiter, personal "
        "communication to Horizons/NAIF. Accessed via JPL Solar System "
        "Dynamics, https://ssd.jpl.nasa.gov, JUP365."
    ),
    comments="Best-fit equilibrium shape",
)

Europa2024 = TriaxialEllipsoid(
    name="Europa2024",
    long_name="Europa equilibrium triaxial ellipsoid (2024)",
    semimajor_axis=1_562_600,
    semimedium_axis=1_560_100,
    semiminor_axis=1_559_300,
    geocentric_grav_const=3202.72e9,
    angular_velocity=2 * np.pi / (3.525463 * 24 * 60 * 60),
    reference=(
        "Semi-axis: Nimmo, F., et al. (2007). The global shape of Europa: "
        "Constraints on lateral shell thickness variations. Icarus, 191(1), "
        "183–192. https://doi.org/10.1016/j.icarus.2007.04.021"
        "\n"
        "GM: Anderson, J. D., et al. (1998). Europa's differentiated internal "
        "structure: Inferences from four Galileo encounters. Science, 281, "
        "2019–2022. https://doi.org/10.1126/science.281.5385.2019"
        "\n"
        "Angular velocity: R. A. Jacobson (2021), The Orbits of the Regular "
        "Jovian Satellites and the Orientation of the Pole of Jupiter, personal "
        "communication to Horizons/NAIF. Accessed via JPL Solar System "
        "Dynamics, https://ssd.jpl.nasa.gov, JUP365."
    ),
    comments="Best-fit hydrostatic ellipsoid (nominal)",
)

Ganymede2024 = TriaxialEllipsoid(
    name="Ganymede2024",
    long_name="Ganymede equilibrium triaxial ellipsoid (2024)",
    semimajor_axis=2_634_770,
    semimedium_axis=2_632_380,
    semiminor_axis=2_631_590,
    geocentric_grav_const=9.8878041807018262e12,
    angular_velocity=2 * np.pi / (7.155588 * 24 * 60 * 60),
    reference=(
        "Semi-axis: Zubarev, A., et al. (2015). New Ganymede control point "
        "network and global shape model. Planetary and Space Science, 117, "
        "246–249. https://doi.org/10.1016/j.pss.2015.06.022"
        "\n"
        "GM: Gomez Casajus, L., et al. (2022). Gravity Field of Ganymede After "
        "the Juno Extended Mission. Geophysical Research Letters, 49(24), "
        "e2022GL099475. https://doi.org/doi:10.1029/2022GL099475"
        "\n"
        "Angular velocity: R. A. Jacobson (2021), The Orbits of the Regular "
        "Jovian Satellites and the Orientation of the Pole of Jupiter, personal "
        "communication to Horizons/NAIF. Accessed via JPL Solar System "
        "Dynamics, https://ssd.jpl.nasa.gov, JUP365."
    ),
    comments="Equilibrium ellipsoid III",
)

Callisto2024 = Sphere(
    name="Callisto2024",
    long_name="Callisto spheroid (2024)",
    radius=2_410_300,
    geocentric_grav_const=7179.292e9,
    angular_velocity=2 * np.pi / (16.690440 * 24 * 60 * 60),
    reference=(
        "Radius, GM: Anderson, J. D., et al. (2001). Shape, mean radius, gravity "
        "field, and interior structure of Callisto. Icarus, 153(1), 157–161. "
        "https://doi.org/10.1006/icar.2001.6664"
        "\n"
        "Angular velocity: Satellites and the Orientation of the Pole of Jupiter, "
        "personal communication to Horizons/NAIF. Accessed via JPL Solar "
        "System Dynamics, https://ssd.jpl.nasa.gov, JUP365."
    ),
)

Enceladus2024 = TriaxialEllipsoid(
    name="Enceladus2024",
    long_name="Enceladus triaxial ellipsoid (2024)",
    semimajor_axis=256_140,
    semimedium_axis=251_160,
    semiminor_axis=248_680,
    geocentric_grav_const=7.210443e9,
    angular_velocity=262.7318870466 * 2.0 * np.pi / 360.0 / (24.0 * 60.0 * 60.0),
    reference=(
        "Park, R. S., et al. (2024). The Global Shape, Gravity Field, and "
        "Libration of Enceladus. Journal of Geophysical Research: Planets, "
        "129(1), e2023JE008054. https://doi.org/10.1029/2023JE008054"
    ),
)

Titan2024 = TriaxialEllipsoid(
    name="Titan2024",
    long_name="Titan triaxial ellipsoid (2024)",
    semimajor_axis=2_575_164,
    semimedium_axis=2_574_720,
    semiminor_axis=2_574_314,
    geocentric_grav_const=8978.1383e9,
    angular_velocity=2 * np.pi / (15.945448 * 24 * 60 * 60),
    reference=(
        "Semi-axis: Corlies, P., et al. (2017). Titan’s Topography and Shape at "
        "the End of the Cassini Mission. Geophysical Research Letters, 44(23), "
        "11,754-11,761. https://doi.org/10.1002/2017GL075518"
        "\n"
        "GM: Durante, D., et al. (2019). Titan’s gravity field and interior "
        "structure after Cassini. Icarus, 326, 123–132. "
        "https://doi.org/10.1016/j.icarus.2019.03.003"
        "\n"
        "Angular velocity: Jacobson, R. (2022). The Orbits of the Main Saturnian "
        "Satellites, the Saturnian System Gravity Field, and the Orientation "
        "of Saturn's Pole. The Astronomical Journal, 164, 199. "
        "https://doi.org/10.3847/1538-3881/ac90c9"
    ),
    comments=(
        "Fit to ellipsoid shape (not derived from spherical harmonic coefficients)"
    ),
)

Pluto2024 = Sphere(
    name="Pluto2024",
    long_name="Pluto spheroid (2024)",
    radius=1_188_300,
    geocentric_grav_const=869.6e9,
    angular_velocity=1.1385591834674098e-05,
    reference=(
        "Radius: Nimmo, et al. (2017). Mean radius and shape of Pluto and Charon "
        "from New Horizons images. Icarus, 287, 12–29. "
        "https://doi.org/10.1016/j.icarus.2016.06.027"
        "\n"
        "GM, angular velocity: Brozović, M., et al. (2015). The orbits and masses of "
        "satellites of Pluto. Icarus, 246, 317–329. "
        "https://doi.org/10.1016/j.icarus.2014.03.015"
    ),
)

Charon2024 = Sphere(
    name="Charon2024",
    long_name="Charon spheroid (2024)",
    radius=606_000,
    geocentric_grav_const=105.88e9,
    angular_velocity=1.1385591834674098e-055,
    reference=(
        "Radius: Nimmo, et al. (2017). Mean radius and shape of Pluto and Charon "
        "from New Horizons images. Icarus, 287, 12–29. "
        "https://doi.org/10.1016/j.icarus.2016.06.027"
        "\n"
        "GM, angular velocity: Brozović, M., et al. (2015). The orbits and masses of "
        "satellites of Pluto. Icarus, 246, 317–329. "
        "https://doi.org/10.1016/j.icarus.2014.03.015"
    ),
)
