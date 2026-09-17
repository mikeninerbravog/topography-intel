import pytest

from topography_intel.angles import packed_to_decimal
from topography_intel.horizontal_angles import sum_horizontal_angles


# Validate the horizontal-angle sum using a known five-station traverse.
#
# Test values are expressed directly in decimal degrees from their
# degrees-minutes-seconds components. This isolates C02 from C01 and proves
# that this module performs only horizontal-angle arithmetic.
def test_sum_horizontal_angles():
    angles = [
        132 + 34 / 60,
        88 + 33 / 60 + 20 / 3600,
        92 + 37 / 60 + 40 / 3600,
        133 + 9 / 60,
        93 + 7 / 60,
    ]

    # The five observed angles total 540 degrees and 1 minute.
    expected = 540 + 1 / 60

    # Approximate comparison accounts for floating-point representation noise.
    assert sum_horizontal_angles(angles) == pytest.approx(expected)



# An empty collection has no horizontal-angle contribution.
# The additive identity therefore requires the sum to be zero degrees.
def test_sum_horizontal_angles_empty():
    assert sum_horizontal_angles([]) == 0





# Validate the integration boundary between C01 and C02.
#
# Packed DDD.MMSS values are converted by the angle-conversion module before
# C02 receives them. C02 remains unaware of the external packed representation.
def test_sum_horizontal_angles_from_packed_values():
    packed_angles = [
        132.34,
        88.332,
        92.374,
        133.09,
        93.07,
    ]

    # C01 owns representation conversion.
    decimal_angles = [packed_to_decimal(value) for value in packed_angles]

    # C02 owns horizontal-angle arithmetic.
    result = sum_horizontal_angles(decimal_angles)

    # The complete traverse totals 540 degrees and 1 minute.
    expected = 540 + 1 / 60

    assert result == pytest.approx(expected)

