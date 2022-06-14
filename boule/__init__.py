# Copyright (c) 2019 The Boule Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
#
# This code is part of the Fatiando a Terra project (https://www.fatiando.org)
#
# Import functions/classes to make the public API
from ._version import __version__
from .ellipsoid import Ellipsoid
from .realizations import GRS80, MARS, MERCURY, MOON, VENUS, VESTA, WGS84
from .sphere import Sphere
from .triaxialellipsoid import TriaxialEllipsoid

ELLIPSOIDS = [WGS84, GRS80, MARS, VENUS, MOON, MERCURY]
