def normalize_azimuth(value: float) -> float:
    """Normalize an angle to the azimuth interval [0, 360) degrees."""

    # Azimuth is represented clockwise from north within one complete turn.
    # Modulo normalization handles negative angles and values equal to or
    # greater than 360 degrees without conditional branches.
    return value % 360.0



def next_azimuth(previous_azimuth: float, corrected_angle: float) -> float:
    """Return the next traverse azimuth in decimal degrees."""

    # For the observed closed-traverse convention, propagate the azimuth by
    # combining the previous azimuth with the corrected interior angle and
    # subtracting the straight angle between consecutive traverse directions.
    raw_azimuth = previous_azimuth + corrected_angle - 180.0

    # Keep the resulting direction within the canonical azimuth interval.
    return normalize_azimuth(raw_azimuth)
