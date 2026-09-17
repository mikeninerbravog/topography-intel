import pytest

from topography_intel.angles import decimal_to_packed, packed_to_decimal


@pytest.mark.parametrize(
    ("packed", "expected"),
    [
        (132.34, 132 + 34 / 60),
        (88.332, 88 + 33 / 60 + 20 / 3600),
        (92.374, 92 + 37 / 60 + 40 / 3600),
        (133.09, 133 + 9 / 60),
        (93.07, 93 + 7 / 60),
        (92.105, 92 + 10 / 60 + 50 / 3600),
    ],
)
def test_packed_to_decimal(packed, expected):
    assert packed_to_decimal(packed) == pytest.approx(expected)





@pytest.mark.parametrize(
    ("decimal", "expected"),
    [
        (132 + 34 / 60, 132.34),
        (88 + 33 / 60 + 20 / 3600, 88.332),
        (92 + 37 / 60 + 40 / 3600, 92.374),
        (133 + 9 / 60, 133.09),
        (93 + 7 / 60, 93.07),
        (92 + 10 / 60 + 50 / 3600, 92.105),
    ],
)
def test_decimal_to_packed(decimal, expected):
    assert decimal_to_packed(decimal) == pytest.approx(expected)



@pytest.mark.parametrize(
    "packed",
    [
        132.5960,
        132.6060,
        132.9966,
    ],
)
def test_packed_to_decimal_rejects_invalid_angles(packed):
    with pytest.raises(ValueError, match="Invalid packed sexagesimal angle"):
        packed_to_decimal(packed)



@pytest.mark.parametrize(
    "packed",
    [
        132.34,
        88.332,
        92.374,
        133.09,
        93.07,
        92.105,
    ],
)
def test_angle_round_trip(packed):
    decimal = packed_to_decimal(packed)
    result = decimal_to_packed(decimal)

    assert result == pytest.approx(packed)

