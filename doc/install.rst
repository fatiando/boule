.. _install:

Installing
==========

There are different ways to install Boule:

.. tab-set::

    .. tab-item:: pip

        Using the `pip package manager <https://pypi.org/project/pip/>`__:

        .. code:: bash

            pip install boule

    .. tab-item:: conda/mamba

        Using the `conda package manager <https://conda.io/>`__ (or ``mamba``)
        that comes with the Anaconda/Miniconda distribution:

        .. code:: bash

            conda install boule --channel conda-forge

    .. tab-item:: Development version

        You can use ``pip`` to install the latest **unreleased** version from
        GitHub (**not recommended** in most situations):

        .. code:: bash

            python -m pip install --upgrade git+https://github.com/fatiando/boule

.. note::

   The commands above should be executed in a terminal. On Windows, use the
   ``cmd.exe`` or the "Anaconda Prompt" app if you’re using Anaconda.


Which Python?
-------------

You'll need **Python >= 3.7**.
See :ref:`python-versions` if you require support for older versions.

Dependencies
------------

These required dependencies should be installed automatically when you install
Boule with ``pip`` or ``conda``:

* `numpy <http://www.numpy.org/>`__
* `attrs <https://www.attrs.org/>`__

See :ref:`dependency-versions` for the our policy of oldest supported versions
of each dependency.
