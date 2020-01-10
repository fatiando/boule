.. _mars:

Mars
====

The parameters of the Martian ellipsoid were obtained from [Ardalan2009]_:

.. doctest::

    >>> from boule import MARS
    >>> print(MARS)
    Ellipsoid(name='MARS', ...)
    >>> # Flattening
    >>> print("{:.5f}".format(MARS.flattening))
    0.00523
    >>> # Semimajor axis
    >>> print("{:.0f}".format(MARS.semimajor_axis))
    3395428
    >>> # Semiminor axis
    >>> print("{:.0f}".format(MARS.semiminor_axis))
    3377678
    >>> # Geocentric gravitational constant (GM)
    >>> print("{:.7e}".format(MARS.geocentric_grav_const))
    4.2828372e+13
    >>> # Angular velocity
    >>> print("{:.7e}".format(MARS.angular_velocity))
    7.0882181e-05
