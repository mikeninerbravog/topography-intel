from math import cos, radians


def horizontal_distance(
    upper_reading: float,
    lower_reading: float,
    vertical_angle: float,
    stadia_constant: float = 100.0,
) -> float:
    """Return horizontal distance from stadia readings and vertical angle."""

    # The stadia interval is the difference between the upper and lower
    # staff readings. The R001 instrument uses a stadia constant of 100,
    # exposed as a parameter so the calculation remains generally reusable.
    staff_interval = upper_reading - lower_reading

    # Python trigonometric functions operate in radians, while the public
    # contract of this module expresses surveying angles in decimal degrees.
    angle_radians = radians(vertical_angle)

    # Reduce the stadia distance to the horizontal plane using the squared
    # cosine of the vertical angle.
    return stadia_constant * staff_interval * cos(angle_radians) ** 2

