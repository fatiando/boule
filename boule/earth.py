"""
Earth ellipsoids
"""
from .ellipsoid import Ellipsoid


class WGS84(Ellipsoid):
    """
    World Geodetic System 1984.

    The WGS84 ellipsoid as defined by the values given in
    [Hofmann-WellenhofMoritz2006]_.

    Note that the ellipsoid gravity at the pole differs from
    [Hofmann-WellenhofMoritz2006]_ on the last digit. This is sufficiently
    small as to not be a cause for concern.

    Examples
    --------

    >>> wgs84 = WGS84()
    >>> print(wgs84) # doctest: +ELLIPSIS
    WGS84(name='WGS84', ...)
    >>> print("{:.4f}".format(wgs84.semiminor_axis))
    6356752.3142
    >>> print("{:.7f}".format(wgs84.flattening))
    0.0033528
    >>> print("{:.13e}".format(wgs84.linear_eccentricity))
    5.2185400842339e+05
    >>> print("{:.13e}".format(wgs84.first_eccentricity))
    8.1819190842621e-02
    >>> print("{:.13e}".format(wgs84.second_eccentricity))
    8.2094437949696e-02
    >>> print("{:.4f}".format(wgs84.mean_radius))
    6371008.7714
    >>> print("{:.14f}".format(wgs84.emm))
    0.00344978650684
    >>> print("{:.10f}".format(wgs84.gravity_equator))
    9.7803253359
    >>> print("{:.10f}".format(wgs84.gravity_pole))
    9.8321849379

    """

    def __init__(self):
        super().__init__(
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
