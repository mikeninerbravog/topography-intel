def theoretical_angle_sum(stations: int) -> float:
    """Return the theoretical interior-angle sum for a closed traverse."""

    # A closed polygon with n stations has an interior-angle sum of
    # (n - 2) * 180 degrees.
    return (stations - 2) * 180.0



def angular_closure_error(observed: float, theoretical: float) -> float:
    """Return the angular closure error in decimal degrees."""

    # Closure error is the signed difference between the observed angle sum
    # and the theoretical sum. A positive value represents an excess in the
    # observed angles; a negative value represents a deficit.
    return observed - theoretical


def equal_angle_correction(error: float, stations: int) -> float:
    """Return the equal angular correction per station in decimal degrees."""

    # The correction must oppose the closure error so that applying the same
    # correction to every observed angle removes the total angular misclosure.
    return -error / stations
