import math


def _resulting_force_from_belt_tensions_and_wrap_angle(
    belt_tension_upper: float, belt_tension_lower: float, wrap_angle: float
) -> float:
    """
    Calculate resulting force at pulley from belt tensions and wrap angle.

    This is a magnitude-only calculation using the vector resultant of two
    perpendicular components derived from the belt tensions and wrap angle.

    Parameters
    ----------
    belt_tension_upper : float
        Upper (tight side) belt tension in Newtons.
    belt_tension_lower : float
        Lower (slack side) belt tension in Newtons.
    wrap_angle : float
        Wrap angle in radians.

    Returns
    -------
    float
        Resulting force magnitude in Newtons.

    Notes
    -----
    Equation: F_T = sqrt((T1 - T2*cos(alpha))^2 + (T2*sin(alpha))^2)

    where:
    - T1 = belt_tension_upper
    - T2 = belt_tension_lower
    - alpha = wrap_angle
    """
    cos_alpha = math.cos(wrap_angle)
    sin_alpha = math.sin(wrap_angle)

    term1 = belt_tension_upper - belt_tension_lower * cos_alpha
    term2 = belt_tension_lower * sin_alpha

    return math.sqrt(term1**2 + term2**2)
