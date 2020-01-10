WGS84: World Geodetic System 1984
=================================

The WGS84 ellipsoid as defined by the values given in
[Hofmann-WellenhofMoritz2006]_:

.. doctest::

    >>> from boule import WGS84
    >>> print(WGS84)
    Ellipsoid(name='WGS84', ...)
    >>> # Inverse flattening
    >>> print("{:.9f}".format(1 / WGS84.flattening))
    298.257223563
    >>> # Semimajor axis
    >>> print("{:.0f}".format(WGS84.semimajor_axis))
    6378137
    >>> # Geocentric gravitational constant (GM)
    >>> print("{:.9e}".format(WGS84.geocentric_grav_const))
    3.986004418e+14
    >>> # Angular velocity
    >>> print("{:.6e}".format(WGS84.angular_velocity))
    7.292115e-05

The following are some of the derived attributes:

.. doctest::

    >>> print("{:.7f}".format(WGS84.flattening))
    0.0033528
    >>> print("{:.4f}".format(WGS84.semiminor_axis))
    6356752.3142
    >>> print("{:.13e}".format(WGS84.linear_eccentricity))
    5.2185400842339e+05
    >>> print("{:.13e}".format(WGS84.first_eccentricity))
    8.1819190842621e-02
    >>> print("{:.13e}".format(WGS84.second_eccentricity))
    8.2094437949696e-02
    >>> print("{:.4f}".format(WGS84.mean_radius))
    6371008.7714
    >>> print("{:.14f}".format(WGS84.emm))
    0.00344978650684
    >>> print("{:.10f}".format(WGS84.gravity_equator))
    9.7803253359
    >>> print("{:.10f}".format(WGS84.gravity_pole))
    9.8321849379

Note that the ellipsoid gravity at the pole differs from
[Hofmann-WellenhofMoritz2006]_ on the last digit.
This is sufficiently small as to not be a cause for concern.
