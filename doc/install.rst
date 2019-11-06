.. _install:

Installing
==========

Which Python?
-------------

You'll need **Python 3.6 or greater**.

We recommend using the
`Anaconda Python distribution <https://www.anaconda.com/download>`__
to ensure you have all dependencies installed and the ``conda`` package manager
available.
Installing Anaconda does not require administrative rights to your computer and
doesn't interfere with any other Python installations in your system.


Dependencies
------------

* List dependencies here with links to the projects


Installing the latest development version
-----------------------------------------

You can use ``pip`` to install the latest source from Github::

    pip install https://github.com/fatiando/boule/archive/master.zip

Alternatively, you can clone the git repository locally and install from there::

    git clone https://github.com/fatiando/boule.git
    cd boule
    pip install .


Testing your install
--------------------

We ship a full test suite with the package.
To run the tests, you'll need to install some extra dependencies first:

* `pytest <https://docs.pytest.org/>`__

After that, you can test your installation by running the following inside a Python
interpreter::

    import boule
    boule.test()
