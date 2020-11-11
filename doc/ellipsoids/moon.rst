.. _moon:

Moon
====

The parameters of the Lunar spheroid were obtained from [Wieczorek2015]_:

.. doctest::

    >>> from boule import MOON
    >>> print(MOON)
    Sphere(name='MOON', ...)
    >>> # Flattening (Note the Moon is a sphere)
    >>> print("{:.5f}".format(MOON.flattening))
    0.00000
    >>> # Radius
    >>> print("{:.0f}".format(MOON.semimajor_axis))
    1737151
    >>> # Geocentric gravitational constant (GM)
    >>> print("{:.7e}".format(MOON.geocentric_grav_const))
    4.9028001e+12
    >>> # Angular velocity
    >>> print("{:.7e}".format(MOON.angular_velocity))
    2.6617073e-06
    >>> # Acceleration due to gravity alone
    >>> print("{:.3f}".format(MOON.normal_gravitation(height=0, si_units=True)))
    1.625
