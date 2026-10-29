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

Mercury
-------

**Mercury2015**: Mercury spheroid using parameters from [Wieczorek2015]_:

.. jupyter-execute::

    print(boule.Mercury2015)

**Mercury2024**: Mercury spheroid using parameters from [Maia2024]_ and
[Mazarico2014]_:

.. jupyter-execute::

    print(boule.Mercury2024)

Venus
-----

**Venus2015**: Venus spheroid using parameters from [Wieczorek2015]_:

.. jupyter-execute::

    print(boule.Venus2015)

Earth-Moon system
-----------------

**GRS80**: The Geodetic Reference System (1980) ellipsoid as defined by the
values given in [HofmannWellenhofMoritz2006]_:

.. jupyter-execute::

    print(boule.GRS80)

**WGS84**: The World Geodetic System (1984) ellipsoid as defined by the values
given in [HofmannWellenhofMoritz2006]_:

.. jupyter-execute::

    print(boule.WGS84)

**EGM96**: Earth Gravitational Model (1996) ellipsoid as defined by the values
given in [Lemoine1998]_:

.. jupyter-execute::

    print(boule.EGM96)

**Moon2015**: Spheroid of Earth's Moon using parameters from [Wieczorek2015]_:

.. jupyter-execute::

    print(boule.Moon2015)

Mars
----

**Mars2009**: Mars ellipsoid using parameters from [Ardalan2009]_:

.. jupyter-execute::

    print(boule.Mars2009)

(1) Ceres
---------

**Ceres2018**: Ceres ellipsoid using parameters from [Konopliv2018]_ and [Park2019]_:

.. jupyter-execute::

    print(boule.Ceres2018)

(4) Vesta
---------

**Vesta2017**: Vesta ellipsoid using parameters from [Karimi2017]_:

.. jupyter-execute::

    print(boule.Vesta2017)

**VestaTriaxial2017**: Vesta triaxial ellipsoid using parameters from [Karimi2017]_:

.. jupyter-execute::

    print(boule.VestaTriaxial2017)

Jupiter system
--------------

**Io2024**: Io triaxial ellipsoid using parameters from [Thomas1998]_,
[Anderson2001]_, and [Jacobson2021]_:

.. jupyter-execute::

    print(boule.Io2024)

**Europa2024**: Europa triaxial ellipsoid using parameters from [Nimmo2007]_,
[Anderson1998]_, and [Jacobson2021]_:

.. jupyter-execute::

    print(boule.Europa2024)

**Ganymede2024**: Ganymede triaxial ellipsoid using parameters from [Zubarev2015]_,
[GomezCasajus2022]_, and [Jacobson2021]_:

.. jupyter-execute::

    print(boule.Ganymede2024)

**Callisto2024**: Callisto spheroid using parameters from [Anderson2001b]_
and [Jacobson2021]_:

    .. jupyter-execute::

        print(boule.Callisto2024)

Saturn system
-------------

**Enceladus2024**: Enceladus triaxial ellipsoid using parameters from [Park2024]_:

.. jupyter-execute::

    print(boule.Enceladus2024)

**Titan2024**: Titan triaxial ellipsoid using parameters from [Corlies2017]_,
[Durante2019]_, and [Jacobson2022]_:

.. jupyter-execute::

    print(boule.Titan2024)

Pluto system
------------

**Pluto2024**: Pluto spheroid using parameters from [Nimmo2017]_ and [Brozović2015]_:

.. jupyter-execute::

    print(boule.Pluto2024)

**Charon2024**: Charon spheroid using parameters from [Nimmo2017]_ and [Brozović2015]_:

.. jupyter-execute::

    print(boule.Charon2024)
