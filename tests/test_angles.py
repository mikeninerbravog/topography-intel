import pytest

from topography_intel.angles import decimal_to_packed, packed_to_decimal


# Validate conversion from packed DDD.MMSS notation to decimal degrees.
#
# Each fixture represents a known sexagesimal angle. The expected value is
# calculated explicitly from degrees, minutes, and seconds so the test does
# not depend on another conversion function to determine the correct result.
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
    # Use approximate comparison because decimal-degree calculations use
    # floating-point arithmetic and may contain insignificant rounding noise.
    assert packed_to_decimal(packed) == pytest.approx(expected)


# Validate the inverse conversion from decimal degrees to packed DDD.MMSS.
#
# Decimal inputs are constructed directly from their sexagesimal components.
# This keeps the expected packed values independent from packed_to_decimal().
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
    # Approximate comparison protects the test from harmless binary
    # floating-point representation differences.
    assert decimal_to_packed(decimal) == pytest.approx(expected)


# Packed DDD.MMSS notation is sexagesimal, so both the minute and second
# fields must remain within the range 00..59. These fixtures intentionally
# violate that invariant and must never be silently normalized.
@pytest.mark.parametrize(
    "packed",
    [
        132.5960,  # 59 minutes, 60 seconds.
        132.6060,  # 60 minutes, 60 seconds.
        132.9966,  # 99 minutes, 66 seconds.
    ],
)
def test_packed_to_decimal_rejects_invalid_angles(packed):
    # Invalid sexagesimal data must fail explicitly instead of producing a
    # plausible but incorrect decimal angle.
    with pytest.raises(ValueError, match="Invalid packed sexagesimal angle"):
        packed_to_decimal(packed)


# Validate bidirectional consistency of the two conversion functions.
#
# A valid packed angle must survive:
#
#     DDD.MMSS -> decimal degrees -> DDD.MMSS
#
# and return to the original packed representation.
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
    # Convert to the internal decimal-degree representation.
    decimal = packed_to_decimal(packed)

    # Convert back to the external packed representation.
    result = decimal_to_packed(decimal)

    # The recovered value must match the original angle.
    assert result == pytest.approx(packed)
