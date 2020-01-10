GRS80: Geodetic Reference System 1980
=====================================

The GRS80 ellipsoid as defined by the values given in
[Hofmann-WellenhofMoritz2006]_:

.. doctest::

    >>> from boule import GRS80
    >>> print(GRS80)
    Ellipsoid(name='GRS80', ...)
    >>> # Inverse flattening
    >>> print("{:.9f}".format(1 / GRS80.flattening))
    298.257222101
    >>> # Semimajor axis
    >>> print("{:.0f}".format(GRS80.semimajor_axis))
    6378137
    >>> # Geocentric gravitational constant (GM)
    >>> print("{:.7e}".format(GRS80.geocentric_grav_const))
    3.9860050e+14
    >>> # Angular velocity
    >>> print("{:.6e}".format(GRS80.angular_velocity))
    7.292115e-05

The following are some of the derived attributes:

.. doctest::

    >>> print("{:.14f}".format(GRS80.flattening))
    0.00335281068118
    >>> print("{:.4f}".format(GRS80.semiminor_axis))
    6356752.3141
    >>> print("{:.9e}".format(GRS80.linear_eccentricity))
    5.218540097e+05
    >>> print("{:.14f}".format(GRS80.first_eccentricity ** 2))
    0.00669438002290
    >>> print("{:.14f}".format(GRS80.second_eccentricity ** 2))
    0.00673949677548
    >>> print("{:.14f}".format(GRS80.emm))
    0.00344978600308
    >>> print("{:.10f}".format(GRS80.gravity_equator))
    9.7803267715
    >>> print("{:.10f}".format(GRS80.gravity_pole))
    9.8321863685

