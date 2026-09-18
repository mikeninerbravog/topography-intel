import pytest

from topography_intel.horizontal_distance import horizontal_distance


@pytest.mark.parametrize(
    ("upper", "lower", "angle", "constant", "expected"),
    [
        # With zero vertical angle, cos²(0) = 1 and no horizontal
        # reduction is applied to the stadia interval.
        (1.500, 1.000, 0.0, 100.0, 50.0),

        # cos²(60°) = 0.25, reducing a 50 m stadia distance to 12.5 m.
        (1.500, 1.000, 60.0, 100.0, 12.5),

        # Squared cosine makes equal positive and negative vertical
        # angles produce the same horizontal distance.
        (1.500, 1.000, -60.0, 100.0, 12.5),

        # The stadia constant is part of the public contract and must
        # not be fixed internally to the R001 value of 100.
        (1.500, 1.000, 0.0, 50.0, 25.0),
    ],
)
def test_horizontal_distance(upper, lower, angle, constant, expected):
    """Validate horizontal-distance mathematics independently."""

    result = horizontal_distance(
        upper,
        lower,
        angle,
        stadia_constant=constant,
    )

    assert result == pytest.approx(expected)



@pytest.mark.parametrize(
    ("upper", "lower", "angle", "expected"),
    [
        # R001 preserved cases whose recorded horizontal distances agree
        # with the reconstructed stadia-distance equation.
        (1.353, 1.000, 3 + 37 / 60 + 20 / 3600, 35.16),
        (1.317, 1.000, 2 + 2 / 60 + 0 / 3600, 31.66),
        (1.045, 1.000, 0 + 17 / 60 + 0 / 3600, 4.50),
        (1.085, 1.000, 0 + 35 / 60 + 0 / 3600, 8.50),
        (1.230, 1.000, 1 + 50 / 60 + 30 / 3600, 22.98),
        (1.112, 1.000, 5 + 3 / 60 + 40 / 3600, 11.11),
    ],
)
def test_r001_horizontal_distance_fixtures(upper, lower, angle, expected):
    """Validate C06 against consistent horizontal distances preserved in R001."""

    result = horizontal_distance(upper, lower, angle)

    assert round(result, 2) == expected


@pytest.mark.parametrize(
    ("upper", "lower", "angle", "expected"),
    [
        # R001 preserved cases whose recorded horizontal distances agree
        # with the reconstructed stadia-distance equation.
        (1.353, 1.000, 3 + 37 / 60 + 20 / 3600, 35.16),
        (1.317, 1.000, 2 + 2 / 60 + 0 / 3600, 31.66),
        (1.045, 1.000, 0 + 17 / 60 + 0 / 3600, 4.50),
        (1.085, 1.000, 0 + 35 / 60 + 0 / 3600, 8.50),
        (1.230, 1.000, 1 + 50 / 60 + 30 / 3600, 22.98),
        (1.112, 1.000, 5 + 3 / 60 + 40 / 3600, 11.11),
    ],
)
def test_r001_horizontal_distance_fixtures(upper, lower, angle, expected):
    """Validate C06 against consistent horizontal distances preserved in R001."""

    result = horizontal_distance(upper, lower, angle)

    assert round(result, 2) == expected
