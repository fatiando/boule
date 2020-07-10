# pylint: disable=redefined-outer-name
"""
Test the base Ellipsoid class.
"""
import pytest
import numpy as np
import numpy.testing as npt

from .. import Ellipsoid, ELLIPSOIDS


ELLIPSOID_NAMES = [e.name for e in ELLIPSOIDS]


@pytest.fixture
def sphere():
    "A spherical ellipsoid"
    ellipsoid = Ellipsoid(
        name="unit_sphere",
        semimajor_axis=1.0,
        flattening=0,
        geocentric_grav_const=0,
        angular_velocity=0,
    )
    return ellipsoid


def test_geodetic_to_spherical_with_spherical_ellipsoid(sphere):
    "Test geodetic to geocentric conversion if ellipsoid is a sphere."
    rtol = 1e-10
    size = 5
    longitude = np.linspace(0, 180, size)
    latitude = np.linspace(-90, 90, size)
    height = np.linspace(-0.2, 0.2, size)
    sph_longitude, sph_latitude, radius = sphere.geodetic_to_spherical(
        longitude, latitude, height
    )
    npt.assert_allclose(sph_longitude, longitude, rtol=rtol)
    npt.assert_allclose(sph_latitude, latitude, rtol=rtol)
    npt.assert_allclose(radius, sphere.mean_radius + height, rtol=rtol)


def test_spherical_to_geodetic_with_spherical_ellipsoid(sphere):
    "Test spherical to geodetic conversion if ellipsoid is a sphere."
    rtol = 1e-10
    size = 5
    spherical_longitude = np.linspace(0, 180, size)
    spherical_latitude = np.linspace(-90, 90, size)
    radius = np.linspace(0.8, 1.2, size)
    longitude, latitude, height = sphere.spherical_to_geodetic(
        spherical_longitude, spherical_latitude, radius
    )
    npt.assert_allclose(spherical_longitude, longitude, rtol=rtol)
    npt.assert_allclose(spherical_latitude, latitude, rtol=rtol)
    npt.assert_allclose(radius, sphere.mean_radius + height, rtol=rtol)


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_geodetic_to_spherical_on_equator(ellipsoid):
    "Test geodetic to geocentric coordinates conversion on equator."
    rtol = 1e-10
    size = 5
    longitude = np.linspace(0, 180, size)
    height = np.linspace(-1e4, 1e4, size)
    latitude = np.zeros_like(size)
    sph_longitude, sph_latitude, radius = ellipsoid.geodetic_to_spherical(
        longitude, latitude, height
    )
    npt.assert_allclose(sph_longitude, longitude, rtol=rtol)
    npt.assert_allclose(sph_latitude, latitude, rtol=rtol)
    npt.assert_allclose(radius, height + ellipsoid.semimajor_axis, rtol=rtol)


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_geodetic_to_spherical_on_poles(ellipsoid):
    "Test geodetic to geocentric coordinates conversion on poles."
    rtol = 1e-10
    size = 5
    longitude = np.hstack([np.linspace(0, 180, size)] * 2)
    height = np.hstack([np.linspace(-1e4, 1e4, size)] * 2)
    latitude = np.array([90.0] * size + [-90.0] * size)
    sph_longitude, sph_latitude, radius = ellipsoid.geodetic_to_spherical(
        longitude, latitude, height
    )
    npt.assert_allclose(sph_longitude, longitude, rtol=rtol)
    npt.assert_allclose(sph_latitude, latitude, rtol=rtol)
    npt.assert_allclose(radius, height + ellipsoid.semiminor_axis, rtol=rtol)


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_spherical_to_geodetic_on_equator(ellipsoid):
    "Test spherical to geodetic coordinates conversion on equator."
    rtol = 1e-10
    size = 5
    spherical_latitude = np.zeros(size)
    spherical_longitude = np.linspace(0, 180, size)
    radius = np.linspace(-1e4, 1e4, size) + ellipsoid.semimajor_axis
    longitude, latitude, height = ellipsoid.spherical_to_geodetic(
        spherical_longitude, spherical_latitude, radius
    )
    npt.assert_allclose(spherical_longitude, longitude, rtol=rtol)
    npt.assert_allclose(spherical_latitude, latitude, rtol=rtol)
    npt.assert_allclose(radius, height + ellipsoid.semimajor_axis, rtol=rtol)


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_spherical_to_geodetic_on_poles(ellipsoid):
    "Test spherical to geodetic coordinates conversion on poles."
    rtol = 1e-10
    size = 5
    spherical_longitude = np.hstack([np.linspace(0, 180, size)] * 2)
    spherical_latitude = np.array([90.0] * size + [-90.0] * size)
    radius = np.hstack([np.linspace(-1e4, 1e4, size) + ellipsoid.semiminor_axis] * 2)
    longitude, latitude, height = ellipsoid.spherical_to_geodetic(
        spherical_longitude, spherical_latitude, radius
    )
    npt.assert_allclose(spherical_longitude, longitude, rtol=rtol)
    npt.assert_allclose(spherical_latitude, latitude, rtol=rtol)
    npt.assert_allclose(radius, height + ellipsoid.semiminor_axis, rtol=rtol)


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_spherical_to_geodetic_identity(ellipsoid):
    "Test if applying both conversions in series is the identity operator"
    rtol = 1e-10
    longitude = np.linspace(0, 350, 36)
    latitude = np.linspace(-90, 90, 19)
    height = np.linspace(-1e4, 1e4, 8)
    coordinates = np.meshgrid(longitude, latitude, height)
    spherical_coordinates = ellipsoid.geodetic_to_spherical(*coordinates)
    reconverted_coordinates = ellipsoid.spherical_to_geodetic(*spherical_coordinates)
    npt.assert_allclose(coordinates, reconverted_coordinates, rtol=rtol)


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_normal_gravity_pole_equator(ellipsoid):
    "Compare normal gravity values at pole and equator"
    rtol = 1e-10
    height = 0
    # Convert gamma to mGal
    gamma_pole = ellipsoid.gravity_pole * 1e5
    gamma_eq = ellipsoid.gravity_equator * 1e5
    npt.assert_allclose(gamma_pole, ellipsoid.normal_gravity(-90, height), rtol=rtol)
    npt.assert_allclose(gamma_pole, ellipsoid.normal_gravity(90, height), rtol=rtol)
    npt.assert_allclose(gamma_eq, ellipsoid.normal_gravity(0, height), rtol=rtol)


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_normal_gravity_arrays(ellipsoid):
    "Compare normal gravity passing arrays as arguments instead of floats"
    rtol = 1e-10
    heights = np.zeros(3)
    latitudes = np.array([-90, 90, 0])
    gammas = np.array(
        [ellipsoid.gravity_pole, ellipsoid.gravity_pole, ellipsoid.gravity_equator]
    )
    # Convert gammas to mGal
    gammas *= 1e5
    npt.assert_allclose(gammas, ellipsoid.normal_gravity(latitudes, heights), rtol=rtol)


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_normal_gravity_non_zero_height(ellipsoid):
    "Check consistency of normal gravity above and below the ellipsoid."
    # Convert gamma to mGal
    gamma_pole = ellipsoid.gravity_pole * 1e5
    gamma_eq = ellipsoid.gravity_equator * 1e5
    assert gamma_pole > ellipsoid.normal_gravity(90, 1000)
    assert gamma_pole > ellipsoid.normal_gravity(-90, 1000)
    assert gamma_eq > ellipsoid.normal_gravity(0, 1000)
    assert gamma_pole < ellipsoid.normal_gravity(90, -1000)
    assert gamma_pole < ellipsoid.normal_gravity(-90, -1000)
    assert gamma_eq < ellipsoid.normal_gravity(0, -1000)


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_prime_vertical_radius(ellipsoid):
    r"""
    Check prime vertical radius on equator, poles and 45 degrees

    The prime vertical radius can be also expressed in terms of the semi-major and
    semi-minor axis:

    .. math:

        N(\phi) = \frac{a^2}{\sqrt{a^2 \cos^2 \phi + b^2 \sin^2 \phi}}
    """
    # Compute prime vertical radius on the equator and the poles
    latitudes = np.array([0, 90, -90, 45])
    prime_vertical_radii = ellipsoid.prime_vertical_radius(
        np.sin(np.radians(latitudes))
    )
    # Computed expected values
    prime_vertical_radius_equator = ellipsoid.semimajor_axis
    prime_vertical_radius_pole = (
        ellipsoid.semimajor_axis ** 2 / ellipsoid.semiminor_axis
    )
    prime_vertical_radius_45 = ellipsoid.semimajor_axis ** 2 / np.sqrt(
        0.5 * ellipsoid.semimajor_axis ** 2 + 0.5 * ellipsoid.semiminor_axis ** 2
    )
    expected_pvr = np.array(
        [
            prime_vertical_radius_equator,
            prime_vertical_radius_pole,
            prime_vertical_radius_pole,
            prime_vertical_radius_45,
        ]
    )
    # Compare calculated vs expected values
    npt.assert_allclose(prime_vertical_radii, expected_pvr)


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_geocentric_radius(ellipsoid):
    "Check against geocentric coordinate conversion results"
    latitude = np.linspace(-80, 80, 100)
    longitude = np.linspace(-180, 180, latitude.size)
    height = np.zeros(latitude.size)
    radius_conversion = ellipsoid.geodetic_to_spherical(longitude, latitude, height)[2]
    npt.assert_allclose(radius_conversion, ellipsoid.geocentric_radius(latitude))


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_geocentric_radius_pole_equator(ellipsoid):
    "Check against values at the pole and equator"
    latitude = np.array([-90, 90, 0])
    radius_true = np.array(
        [ellipsoid.semiminor_axis, ellipsoid.semiminor_axis, ellipsoid.semimajor_axis]
    )
    npt.assert_allclose(radius_true, ellipsoid.geocentric_radius(latitude))


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_geocentric_radius_geocentric(ellipsoid):
    "Check against coordinate conversion results with geocentric latitude"
    latitude = np.linspace(-80, 80, 100)
    longitude = np.linspace(-180, 180, latitude.size)
    height = np.zeros(latitude.size)
    latitude_spherical, radius_conversion = ellipsoid.geodetic_to_spherical(
        longitude, latitude, height
    )[1:]
    npt.assert_allclose(
        radius_conversion,
        ellipsoid.geocentric_radius(latitude_spherical, geodetic=False),
    )


@pytest.mark.parametrize("ellipsoid", ELLIPSOIDS, ids=ELLIPSOID_NAMES)
def test_geocentric_radius_geocentric_pole_equator(ellipsoid):
    "Check against values at the pole and equator with geocentric latitude"
    latitude = np.array([-90, 90, 0])
    radius_true = np.array(
        [ellipsoid.semiminor_axis, ellipsoid.semiminor_axis, ellipsoid.semimajor_axis]
    )
    npt.assert_allclose(
        radius_true, ellipsoid.geocentric_radius(latitude, geodetic=False)
    )
