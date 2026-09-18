from math import cos, radians, sin


def direct_projections(azimuth: float, distance: float) -> tuple[float, float]:
    """Return east and north projections for an azimuth and distance."""

    # The public contract uses azimuth in decimal degrees, measured clockwise
    # from north. Python trigonometric functions operate in radians.
    azimuth_radians = radians(azimuth)

    # East-west displacement follows the sine component because surveying
    # azimuth is referenced to north rather than to the Cartesian x-axis.
    delta_east = distance * sin(azimuth_radians)

    # North-south displacement follows the cosine component. Component signs
    # preserve direction: positive east/north and negative west/south.
    delta_north = distance * cos(azimuth_radians)

    return delta_east, delta_north
