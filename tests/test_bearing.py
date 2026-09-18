import pytest

from topography_intel.bearing import azimuth_to_bearing


@pytest.mark.parametrize(
    ("azimuth", "expected_angle", "expected_direction"),
    [
        # Quadrant I — northeast.
        (45.0, 45.0, "NE"),

        # Quadrant II — southeast.
        (135.0, 45.0, "SE"),

        # Quadrant III — southwest.
        (225.0, 45.0, "SW"),

        # Quadrant IV — northwest.
        (315.0, 45.0, "NW"),

        # Exact cardinal axes.
        (0.0, 0.0, "N"),
        (90.0, 0.0, "E"),
        (180.0, 0.0, "S"),
        (270.0, 0.0, "W"),

        # Inputs outside the canonical azimuth interval must normalize
        # independently inside C05.
        (360.0, 0.0, "N"),
        (450.0, 0.0, "E"),
        (-90.0, 0.0, "W"),
    ],
)
def test_azimuth_to_bearing(azimuth, expected_angle, expected_direction):
    """Validate quadrant-bearing conversion independently of other modules."""

    angle, direction = azimuth_to_bearing(azimuth)

    assert angle == pytest.approx(expected_angle)
    assert direction == expected_direction



@pytest.mark.parametrize(
    ("azimuth", "expected_angle", "expected_direction"),
    [
        (
            92.0 + 10.0 / 60.0 + 50.0 / 3600.0,
            87.0 + 49.0 / 60.0 + 10.0 / 3600.0,
            "SE",
        ),
        (
            0.0 + 43.0 / 60.0 + 58.0 / 3600.0,
            0.0 + 43.0 / 60.0 + 58.0 / 3600.0,
            "NE",
        ),
        (
            273.0 + 21.0 / 60.0 + 26.0 / 3600.0,
            86.0 + 38.0 / 60.0 + 34.0 / 3600.0,
            "NW",
        ),
        (
            226.0 + 30.0 / 60.0 + 14.0 / 3600.0,
            46.0 + 30.0 / 60.0 + 14.0 / 3600.0,
            "SW",
        ),
        (
            139.0 + 37.0 / 60.0 + 2.0 / 3600.0,
            40.0 + 22.0 / 60.0 + 58.0 / 3600.0,
            "SE",
        ),
    ],
)
def test_r001_azimuth_to_bearing(azimuth, expected_angle, expected_direction):
    """Validate C05 against the known R001 traverse azimuths."""

    # R001 fixtures exercise all quadrants actually present in the traverse
    # while remaining independent of the upstream azimuth calculation.
    angle, direction = azimuth_to_bearing(azimuth)

    assert angle == pytest.approx(expected_angle)
    assert direction == expected_direction
