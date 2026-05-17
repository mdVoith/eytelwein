"""
Extended functions for design layout of drive system calculations.

Internal Note on Angle Units:
Internal calculations use radians for mathematical correctness.
Public functions default to returning degrees for usability.
"""

from math import pi
import math


def _mechanical_torque_from_belt_force(
    belt_force: float, pulley_diameter: float
) -> float:
    """
    Calculate the mechanical torque from the belt force and pulley diameter.

    Parameters
    ----------
    belt_force : float
        The belt force.
    pulley_diameter : float
        The pulley diameter.

    Returns
    -------
    float
        The mechanical torque.
    """
    return belt_force * pulley_diameter / 2


def _mechanical_power_from_torque_and_belt_speed(
    torque: float, belt_speed: float, pulley_diameter: float
) -> float:
    """
    Calculate the mechanical power from the torque and speed.

    Parameters
    ----------
    torque : float
        The torque.
    belt_speed : float
        The conveying speed of the belt.
    pulley_diameter : float
        The pulley diameter.

    Returns
    -------
    float
        The mechanical power.

    Raises
    ------
    ValueError
        If pulley_diameter is zero or negative.
    """
    if pulley_diameter <= 0:
        raise ValueError("pulley_diameter must be positive")
    return 2 * torque * belt_speed / pulley_diameter


def _number_of_revolutions_from_translatory_speed(
    translatory_speed: float, radius: float
) -> float:
    """
    Calculate the number of revolutions from the translatory speed.

    Parameters
    ----------
    translatory_speed : float
        The translatory speed.
    radius : float
        The radius.

    Returns
    -------
    float
        The number of revolutions.
    """
    try:
        n = translatory_speed / (2 * pi * radius)
    except ZeroDivisionError:
        raise ValueError("The radius cannot be zero.")

    return n


def _pulley_revolutions_from_belt_speed(
    belt_speed: float, pulley_diameter: float
) -> float:
    """
    Calculate the pulley revolutions from the belt speed.

    Parameters
    ----------
    belt_speed : float
        The belt speed.
    pulley_diameter : float
        The pulley diameter.

    Returns
    -------
    float
        The pulley revolutions.
    """
    revolutions = _number_of_revolutions_from_translatory_speed(
        belt_speed, pulley_diameter / 2
    )
    return revolutions


def _translatory_speed_from_number_of_revolutions(
    revolutions: float, radius: float
) -> float:
    """
    Calculate the translatory speed from the number of revolutions.

    Parameters
    ----------
    revolutions : float
        The number of revolutions.
    radius : float
        The radius.

    Returns
    -------
    float
        The translatory speed.
    """
    return 2 * pi * radius * revolutions


def _belt_speed_from_pulley_revolutions(
    pulley_revolutions: float, pulley_diameter: float
) -> float:
    """
    Calculate the belt speed from the pulley revolutions.

    Parameters
    ----------
    pulley_revolutions : float
        The pulley revolutions.
    pulley_diameter : float
        The pulley diameter.

    Returns
    -------
    float
        The belt speed.
    """
    return _translatory_speed_from_number_of_revolutions(
        pulley_revolutions, pulley_diameter / 2
    )


def _mechanical_power_from_torque_and_revolutions(
    torque: float, revolutions: float
) -> float:
    """
    Calculate the mechanical power from the torque and revolutions.

    Parameters
    ----------
    torque : float
        The torque.
    revolutions : float
        The number of revolutions.

    Returns
    -------
    float
        The mechanical power.
    """
    return 2 * pi * torque * revolutions


def _torque_from_mechanical_power_and_revolutions(
    power: float, revolutions: float
) -> float:
    """
    Calculate the torque from the mechanical power and revolutions.

    Parameters
    ----------
    power : float
        The mechanical power.
    revolutions : float
        The number of revolutions.

    Returns
    -------
    float
        The torque.

    Raises
    ------
    ValueError
        If revolutions is zero or negative.
    """
    if revolutions <= 0:
        raise ValueError("revolutions must be positive")
    return power / (2 * pi * revolutions)


def _revolutions_from_mechanical_power_and_torque(power: float, torque: float) -> float:
    """
    Calculate the revolutions from the mechanical power and torque.

    Parameters
    ----------
    power : float
        The mechanical power.
    torque : float
        The torque.

    Returns
    -------
    float
        The number of revolutions.

    Raises
    ------
    ValueError
        If torque is zero or negative.
    """
    if torque <= 0:
        raise ValueError("torque must be positive")
    return power / (2 * pi * torque)


def _angle_of_inclination_from_horizontal_length_and_lift(
    horizontal_length: float, lift: float
) -> float:
    """
    Calculate the angle of inclination from horizontal length and lift.

    Parameters
    ----------
    horizontal_length : float
        The horizontal length.
    lift : float
        The lift.

    Returns
    -------
    float
        The angle of inclination in radians.
    """
    if horizontal_length == 0:
        raise ValueError("Horizontal length cannot be zero.")

    return math.atan2(lift, horizontal_length)


def _radius_from_translatory_speed_and_revolutions(
    translatory_speed: float, revolutions: float
) -> float:
    """
    Calculate the radius from the translatory speed and revolutions.

    Parameters
    ----------
    translatory_speed : float
        The translatory speed.
    revolutions : float
        The number of revolutions.

    Returns
    -------
    float
        The radius.

    Raises
    ------
    ValueError
        If revolutions is zero or negative.
    """
    if revolutions <= 0:
        raise ValueError("revolutions must be positive")

    return translatory_speed / (2 * pi * revolutions)


def _pulley_diameter_from_belt_speed_and_revolutions(
    belt_speed: float, revolutions: float
) -> float:
    """
    Calculate the pulley diameter from the belt speed and revolutions.

    Parameters
    ----------
    belt_speed : float
        The belt speed.
    revolutions : float
        The number of revolutions.

    Returns
    -------
    float
        The pulley diameter.

    Raises
    ------
    ValueError
        If revolutions is zero or if the calculated diameter is negative.
    """
    diameter = 2 * _radius_from_translatory_speed_and_revolutions(
        belt_speed, revolutions
    )
    if diameter <= 0:
        raise ValueError("Pulley diameter must be greater than zero.")
    return diameter
