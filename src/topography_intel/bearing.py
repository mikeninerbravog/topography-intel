def azimuth_to_bearing(azimuth: float) -> tuple[float, str]:
    """Convert an azimuth in decimal degrees to a quadrant bearing."""

    # Normalize the input independently so this module can accept any angle
    # representing a direction without depending on the azimuth module.
    azimuth = azimuth % 360.0

    # Exact cardinal axes do not belong to a quadrant.
    if azimuth == 0.0:
        return 0.0, "N"
    if azimuth == 90.0:
        return 0.0, "E"
    if azimuth == 180.0:
        return 0.0, "S"
    if azimuth == 270.0:
        return 0.0, "W"

    # Convert each azimuth quadrant into its acute bearing angle and
    # corresponding north/south and east/west orientation.
    if azimuth < 90.0:
        return azimuth, "NE"
    if azimuth < 180.0:
        return 180.0 - azimuth, "SE"
    if azimuth < 270.0:
        return azimuth - 180.0, "SW"

    return 360.0 - azimuth, "NW"

