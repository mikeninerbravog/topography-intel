import pytest

from topography_intel.azimuth import (
    next_azimuth,
    normalize_azimuth,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (273.0, 273.0),
        (-86.0, 274.0),
        (360.0, 0.0),
        (361.0, 1.0),
        (720.0, 0.0),
        (-1.0, 359.0),
    ],
)
def test_normalize_azimuth(value, expected):
    """Validate azimuth normalization independently of other modules."""

    # Every azimuth must be represented within one complete clockwise turn,
    # including inputs below zero or beyond 360 degrees.
    assert normalize_azimuth(value) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("previous", "corrected_angle", "expected"),
    [
        (
            92.0 + 10.0 / 60.0 + 50.0 / 3600.0,
            88.0 + 33.0 / 60.0 + 8.0 / 3600.0,
            0.0 + 43.0 / 60.0 + 58.0 / 3600.0,
        ),
        (
            0.0 + 43.0 / 60.0 + 58.0 / 3600.0,
            92.0 + 37.0 / 60.0 + 28.0 / 3600.0,
            273.0 + 21.0 / 60.0 + 26.0 / 3600.0,
        ),
        (
            273.0 + 21.0 / 60.0 + 26.0 / 3600.0,
            133.0 + 8.0 / 60.0 + 48.0 / 3600.0,
            226.0 + 30.0 / 60.0 + 14.0 / 3600.0,
        ),
        (
            226.0 + 30.0 / 60.0 + 14.0 / 3600.0,
            93.0 + 6.0 / 60.0 + 48.0 / 3600.0,
            139.0 + 37.0 / 60.0 + 2.0 / 3600.0,
        ),
    ],
)
def test_next_azimuth(previous, corrected_angle, expected):
    """Validate azimuth propagation using known traverse transitions."""

    # Inputs are supplied directly in decimal degrees so C04 remains
    # independently testable without angle-conversion or correction modules.
    assert next_azimuth(previous, corrected_angle) == pytest.approx(expected)



def test_r001_azimuth_pipeline():
    """Validate complete C04 azimuth propagation for the known traverse."""

    # Start from the known initial azimuth and propagate each subsequent
    # direction using corrected interior angles expressed in decimal degrees.
    azimuth = 92.0 + 10.0 / 60.0 + 50.0 / 3600.0

    corrected_angles = [
        88.0 + 33.0 / 60.0 + 8.0 / 3600.0,
        92.0 + 37.0 / 60.0 + 28.0 / 3600.0,
        133.0 + 8.0 / 60.0 + 48.0 / 3600.0,
        93.0 + 6.0 / 60.0 + 48.0 / 3600.0,
    ]

    expected_azimuths = [
        0.0 + 43.0 / 60.0 + 58.0 / 3600.0,
        273.0 + 21.0 / 60.0 + 26.0 / 3600.0,
        226.0 + 30.0 / 60.0 + 14.0 / 3600.0,
        139.0 + 37.0 / 60.0 + 2.0 / 3600.0,
    ]

    for corrected_angle, expected in zip(corrected_angles, expected_azimuths):
        azimuth = next_azimuth(azimuth, corrected_angle)
        assert azimuth == pytest.approx(expected)
