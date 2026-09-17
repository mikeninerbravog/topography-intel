def packed_to_decimal(value: float) -> float:
    """Convert a packed DDD.MMSS angle to decimal degrees."""
    degrees = int(value)
    packed = round((value - degrees) * 10000)

    minutes = packed // 100
    seconds = packed % 100

    if minutes >= 60 or seconds >= 60:
        raise ValueError("Invalid packed sexagesimal angle")

    return degrees + minutes / 60 + seconds / 3600


def decimal_to_packed(value: float) -> float:
    """Convert decimal degrees to a packed DDD.MMSS angle."""
    degrees = int(value)
    remainder = (value - degrees) * 60

    minutes = int(remainder)
    seconds = round((remainder - minutes) * 60)

    if seconds == 60:
        seconds = 0
        minutes += 1

    if minutes == 60:
        minutes = 0
        degrees += 1

    return degrees + minutes / 100 + seconds / 10000

