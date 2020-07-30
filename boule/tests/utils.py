"""
Shared utility functions for testing.
"""
import numpy as np


def normal_gravity_surface(latitude, ellipsoid):
    """
    Computes normal gravity on the surface of the ellipsoid [mGal]

    Uses the closed-form Somigliana equation [Hofmann-WellenhofMoritz2006]_.
    """
    latitude_radians = np.radians(latitude)
    coslat = np.cos(latitude_radians)
    sinlat = np.sin(latitude_radians)
    gravity = (
        ellipsoid.semimajor_axis * ellipsoid.gravity_equator * coslat ** 2
        + ellipsoid.semiminor_axis * ellipsoid.gravity_pole * sinlat ** 2
    ) / np.sqrt(
        ellipsoid.semimajor_axis ** 2 * coslat ** 2
        + ellipsoid.semiminor_axis ** 2 * sinlat ** 2
    )
    # Convert to mGal
    return 1e5 * gravity
