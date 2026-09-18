import pytest

from topography_intel.projections import direct_projections


@pytest.mark.parametrize(
    ("azimuth", "distance", "expected_east", "expected_north"),
    [
        # Cardinal axes establish the surveying azimuth convention:
        # clockwise from north.
        (0.0, 10.0, 0.0, 10.0),
        (90.0, 10.0, 10.0, 0.0),
        (180.0, 10.0, 0.0, -10.0),
        (270.0, 10.0, -10.0, 0.0),

        # The four quadrants validate the signs of both components.
        (45.0, 10.0, 7.0710678118654755, 7.0710678118654755),
        (135.0, 10.0, 7.0710678118654755, -7.0710678118654755),
        (225.0, 10.0, -7.0710678118654755, -7.0710678118654755),
        (315.0, 10.0, -7.0710678118654755, 7.0710678118654755),
    ],
)
def test_direct_projections(
    azimuth,
    distance,
    expected_east,
    expected_north,
):
    """Validate direct projection mathematics independently."""

    delta_east, delta_north = direct_projections(azimuth, distance)

    assert delta_east == pytest.approx(expected_east, abs=1e-12)
    assert delta_north == pytest.approx(expected_north, abs=1e-12)


@pytest.mark.parametrize(
    ("azimuth", "distance", "expected_east", "expected_north"),
    [
        # Main closed-traverse sides preserved in R001.
        (92 + 10 / 60 + 50 / 3600, 31.27, 31.2474, -1.1898),
        (0 + 43 / 60 + 58 / 3600, 39.54, 0.5057, 39.5368),
        (273 + 21 / 60 + 26 / 3600, 35.16, -35.0997, 2.0590),
        (226 + 30 / 60 + 14 / 3600, 23.74, -17.2215, -16.3404),
        (139 + 37 / 60 + 2 / 3600, 31.66, 20.5122, -24.1165),
    ],
)
def test_r001_direct_projection_fixtures(
    azimuth,
    distance,
    expected_east,
    expected_north,
):
    """Validate direct projections against the R001 main traverse."""

    delta_east, delta_north = direct_projections(azimuth, distance)

    assert delta_east == pytest.approx(expected_east, abs=0.0001)
    assert delta_north == pytest.approx(expected_north, abs=0.0001)


def test_r001_azimuth_to_projection_composition():
    """Validate the C04-to-C07 composition using an R001 traverse side."""

    from topography_intel.azimuth import next_azimuth

    previous_azimuth = 92 + 10 / 60 + 50 / 3600
    corrected_angle = 88 + 33 / 60 + 8 / 3600

    azimuth = next_azimuth(previous_azimuth, corrected_angle)
    delta_east, delta_north = direct_projections(azimuth, 39.54)

    assert azimuth == pytest.approx(0 + 43 / 60 + 58 / 3600)
    assert delta_east == pytest.approx(0.5057, abs=0.0001)
    assert delta_north == pytest.approx(39.5368, abs=0.0001)
