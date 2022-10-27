.. _ellipsoids:

Available ellipsoids
====================

These are the available ellipsoids and their corresponding defining parameters.

All ellipsoids are instances of the :class:`~boule.Ellipsoid`,
:class:`~boule.Sphere`, or :class:`~boule.TriaxialEllipsoid` classes. See the
class documentations for a list their derived physical properties (attributes)
and computations/transformations that they can perform (methods).

.. admonition:: Help!
    :class: hint

    If an ellipsoid you need isn't in Boule yet, please `reach out
    <https://www.fatiando.org/contact>`__ to the team and consider adding it
    yourself. It requires no special knowledge of the code and is a great way
    to help the project!

.. jupyter-execute::
    :hide-code:

    import boule


Earth
-----

The **WGS84 (World Geodetic System 1984)** ellipsoid as defined by the values
given in [HofmannWellenhofMoritz2006]_:

.. jupyter-execute::

    print(boule.WGS84)

The **GRS80 (Geodetic Reference System 1980)** ellipsoid as defined by the
values given in [HofmannWellenhofMoritz2006]_:

.. jupyter-execute::

    print(boule.GRS80)

Moon
----

The parameters of the Lunar spheroid were obtained from [Wieczorek2015]_:

.. jupyter-execute::

    print(boule.MOON)

Mars
----

The parameters of the Martian ellipsoid were obtained from [Ardalan2009]_:

.. jupyter-execute::

    print(boule.MARS)

Mercury
-------

The parameters of the Mercurian spheroid were obtained from [Wieczorek2015]_:

.. jupyter-execute::

    print(boule.MERCURY)

Venus
-----

The parameters of the Venusian spheroid were obtained from [Wieczorek2015]_:

.. jupyter-execute::

    print(boule.VENUS)

Vesta
-----

The parameters of the Vesta triaxial ellipsoid were obtained from [Russell2012]_:

.. jupyter-execute::

    print(boule.VESTA)
