import pytest

from topography_intel.angular_correction import (
    angular_closure_error,
    equal_angle_correction,
    theoretical_angle_sum,
)


# Validate the theoretical interior-angle sum for closed traverses.
#
# A closed traverse with n stations follows the polygon rule:
# (n - 2) * 180 degrees. Multiple station counts verify that the function
# implements the general rule rather than a value specific to one traverse.
@pytest.mark.parametrize(
    ("stations", "expected"),
    [
        (3, 180.0),
        (4, 360.0),
        (5, 540.0),
        (6, 720.0),
    ],
)
def test_theoretical_angle_sum(stations, expected):
    assert theoretical_angle_sum(stations) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("observed", "theoretical", "expected"),
    [
        (540.0 + 1.0 / 60.0, 540.0, 1.0 / 60.0),
        (539.0 + 59.0 / 60.0, 540.0, -1.0 / 60.0),
        (540.0, 540.0, 0.0),
    ],
)
def test_angular_closure_error(observed, theoretical, expected):
    """Validate signed angular closure error independently of other modules."""

    # Positive error means observed angles exceed the theoretical sum.
    # Negative error means they fall short; zero represents exact closure.
    assert angular_closure_error(observed, theoretical) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("error", "stations", "expected"),
    [
        (1.0 / 60.0, 5, -12.0 / 3600.0),
        (-1.0 / 60.0, 5, 12.0 / 3600.0),
        (0.0, 5, 0.0),
    ],
)
def test_equal_angle_correction(error, stations, expected):
    """Validate equal distribution of angular correction among stations."""

    # Correction has the opposite sign of the closure error.
    # The total correction is distributed equally among all stations.
    assert equal_angle_correction(error, stations) == pytest.approx(expected)



def test_r001_angular_correction_pipeline():
    """Validate the complete C03 calculation using the known R001 case."""

    # The known traverse has five stations and an observed angular sum
    # of 540 degrees and 1 minute.
    stations = 5
    observed = 540.0 + 1.0 / 60.0

    # Derive each value through the public C03 operations rather than
    # hard-coding intermediate results.
    theoretical = theoretical_angle_sum(stations)
    error = angular_closure_error(observed, theoretical)
    correction = equal_angle_correction(error, stations)

    # The five-station traverse theoretically closes at 540 degrees.
    assert theoretical == pytest.approx(540.0)

    # The observed traverse exceeds theoretical closure by exactly 60 seconds.
    assert error == pytest.approx(60.0 / 3600.0)

    # Equal distribution must therefore apply -12 seconds to each station.
    assert correction == pytest.approx(-12.0 / 3600.0)
