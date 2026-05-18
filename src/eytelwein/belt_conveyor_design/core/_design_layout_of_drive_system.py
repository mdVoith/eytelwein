from math import asin, sin


def _height_difference_from_section_length_and_inclination_angle(
    section_length: float, inclination_angle: float
) -> float:
    """
    Calculate the height difference from the section length and inclination angle.

    Parameters
    ----------
    section_length : float
        The length of the section.
    inclination_angle : float
        The angle of inclination in radians.

    Returns
    -------
    float
        The height difference.
    """
    return section_length * sin(inclination_angle)


def _angle_of_inclination_from_height_difference_and_section_length(
    height_difference: float, section_length: float
) -> float:
    """
    Calculate the inclination angle from the height difference and section length.

    Parameters
    ----------
    height_difference : float
        The height difference.
    section_length : float
        The length of the section.

    Returns
    -------
    float
        The angle of inclination in radians.

    Raises
    ------
    ValueError
        If section_length is zero or negative.
    """
    if section_length <= 0:
        raise ValueError("section_length must be positive")
    return asin(height_difference / section_length)


def _section_length_from_height_difference_and_inclination_angle(
    height_difference: float, inclination_angle: float
) -> float:
    """
    Calculate the section length from the height difference and inclination angle.

    Parameters
    ----------
    height_difference : float
        The height difference.
    inclination_angle : float
        The angle of inclination in radians.

    Returns
    -------
    float
        The length of the section.

    Raises
    ------
    ValueError
        If sin(inclination_angle) is zero.
    """
    sin_value = sin(inclination_angle)
    if abs(sin_value) < 1e-10:
        raise ValueError("sin(inclination_angle) cannot be zero")
    return height_difference / sin_value
