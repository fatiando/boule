.. _mercury:

Mercury
=======

The parameters of the Mercurian spheroid were obtained from [Wieczorek2015]_:

.. doctest::

    >>> from boule import MERCURY
    >>> print(MERCURY)
    Ellipsoid(name='MERCURY', ...)
    >>> # Flattening (Note Mercury is a sphere)
    >>> print("{:.5f}".format(MERCURY.flattening))
    0.00000
    >>> # Radius
    >>> print("{:.0f}".format(MERCURY.semimajor_axis))
    2439372
    >>> # Geocentric gravitational constant (GM)
    >>> print("{:.7e}".format(MERCURY.geocentric_grav_const))
    2.2031839e+13
    >>> # Angular velocity
    >>> print("{:.7e}".format(MERCURY.angular_velocity))
    1.2400173e-06
