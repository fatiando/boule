.. _venus:

Venus
=====

The parameters of the Venusian spheroid were obtained from [Wieczorek2015]_:

.. doctest::

    >>> from boule import VENUS
    >>> print(VENUS)
    Ellipsoid(name='VENUS', ...)
    >>> # Flattening (Note Venus is a sphere)
    >>> print("{:.5f}".format(VENUS.flattening))
    0.00000
    >>> # Radius
    >>> print("{:.0f}".format(VENUS.semimajor_axis))
    6051878
    >>> # Geocentric gravitational constant (GM)
    >>> print("{:.7e}".format(VENUS.geocentric_grav_const))
    3.2485859e+14
    >>> # Angular velocity
    >>> print("{:.7e}".format(VENUS.angular_velocity))
    -2.9924000e-07
