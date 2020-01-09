"""
Ellipsoid realizations for the Earth and other planetary bodies.
"""
from .ellipsoid import Ellipsoid


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


MOON = Ellipsoid(
    name="Moon",
    long_name="",
    semimajor_axis=1737151,
    flattening=0,
    geocentric_grav_const=4.90280007e12,
    angular_velocity=2.6617073e-6,
    reference=(
        "Wieczorek, M. A. (2015). Gravity and Topography of the Terrestrial "
        "Planets. In Treatise on Geophysics (pp. 153-193). Elsevier. "
        "doi:10.1016/B978-0-444-53802-4.00169-X"
    ),
)
