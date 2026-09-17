def packed_to_decimal(value: float) -> float:
    """Convert a packed DDD.MMSS angle to decimal degrees."""

    # Extract the integer part as whole degrees.
    degrees = int(value)

    # Convert the fractional MMSS part into an integer.
    # Example: 132.3420 -> 3420 -> 34 minutes, 20 seconds.
    packed = round((value - degrees) * 10000)

    # Split MMSS into minutes and seconds.
    minutes = packed // 100
    seconds = packed % 100

    # Sexagesimal notation requires both fields to be below 60.
    if minutes >= 60 or seconds >= 60:
        raise ValueError("Invalid packed sexagesimal angle")

    # Convert DDD MM SS into decimal degrees.
    return degrees + minutes / 60 + seconds / 3600

def decimal_to_packed(value: float) -> float:
    """Convert decimal degrees to a packed DDD.MMSS angle."""

    # Extract the integer part as whole degrees.
    degrees = int(value)

    # Convert the fractional degree into total minutes.
    # Example: 132.572222... -> 34.333333... minutes.
    remainder = (value - degrees) * 60

    # Extract whole minutes from the remainder.
    minutes = int(remainder)

    # Convert the remaining fractional minute into whole seconds.
    seconds = round((remainder - minutes) * 60)

    # Rounding may produce 60 seconds.
    # Carry one minute and restart the seconds field at zero.
    if seconds == 60:
        seconds = 0
        minutes += 1

    # A carried minute may produce 60 minutes.
    # Carry one degree and restart the minutes field at zero.
    if minutes == 60:
        minutes = 0
        degrees += 1

    # Pack DDD MM SS back into the DDD.MMSS numeric representation.
    return degrees + minutes / 100 + seconds / 10000
