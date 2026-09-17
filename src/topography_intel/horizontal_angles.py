def sum_horizontal_angles(angles) -> float:
    """Return the sum of horizontal angles expressed in decimal degrees."""

    # Horizontal-angle arithmetic is performed in decimal degrees.
    # Representation conversion, such as packed DDD.MMSS, belongs to the
    # angle-conversion module and must occur before values reach this function.
    return sum(angles)

