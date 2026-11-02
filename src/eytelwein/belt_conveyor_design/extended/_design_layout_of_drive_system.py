"""Private raw-float helpers for drive-system calculations.

These functions intentionally operate on plain floats only. Unit conversion and
unit validation are handled by the public wrappers.
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


def _effective_pulley_diameter_from_shell_diameter_and_lagging_thickness(
    shell_diameter: float, lagging_thickness: float
) -> float:
    """
    Calculate the effective pulley diameter from shell diameter and lagging thickness.

    Parameters
    ----------
    shell_diameter : float
        Pulley shell diameter in meters.
    lagging_thickness : float
        Lagging thickness in meters.

    Returns
    -------
    float
        Effective pulley diameter at the belt contact in meters.

    Notes
    -----
    D_eff = D_shell + 2 * t_lagging
    """
    return shell_diameter + 2 * lagging_thickness


def _shell_diameter_from_effective_pulley_diameter_and_lagging_thickness(
    effective_pulley_diameter: float, lagging_thickness: float
) -> float:
    """
    Calculate the pulley shell diameter from effective diameter and lagging thickness.

    Parameters
    ----------
    effective_pulley_diameter : float
        Effective pulley diameter at the belt contact in meters.
    lagging_thickness : float
        Lagging thickness in meters.

    Returns
    -------
    float
        Pulley shell diameter in meters.

    Raises
    ------
    ValueError
        If effective_pulley_diameter does not exceed twice lagging_thickness.

    Notes
    -----
    D_shell = D_eff - 2 * t_lagging
    """
    if effective_pulley_diameter <= 2 * lagging_thickness:
        raise ValueError(
            "effective_pulley_diameter must exceed twice the lagging_thickness, "
            f"got effective_pulley_diameter={effective_pulley_diameter}, "
            f"lagging_thickness={lagging_thickness}"
        )
    return effective_pulley_diameter - 2 * lagging_thickness


def _lagging_thickness_from_effective_and_shell_diameter(
    effective_pulley_diameter: float, shell_diameter: float
) -> float:
    """
    Calculate the lagging thickness from effective and shell diameters.

    Parameters
    ----------
    effective_pulley_diameter : float
        Effective pulley diameter at the belt contact in meters.
    shell_diameter : float
        Pulley shell diameter in meters.

    Returns
    -------
    float
        Lagging thickness in meters.

    Raises
    ------
    ValueError
        If effective_pulley_diameter is smaller than shell_diameter.

    Notes
    -----
    t_lagging = (D_eff - D_shell) / 2
    """
    if effective_pulley_diameter < shell_diameter:
        raise ValueError(
            "effective_pulley_diameter must be greater than or equal to "
            f"shell_diameter, got effective_pulley_diameter={effective_pulley_diameter}, "
            f"shell_diameter={shell_diameter}"
        )
    return (effective_pulley_diameter - shell_diameter) / 2


def _pulley_revolutions_from_motor_revolutions_and_gear_ratio(
    motor_revolutions: float, gear_ratio: float
) -> float:
    """
    Calculate the pulley revolutions from motor revolutions and gear ratio.

    Parameters
    ----------
    motor_revolutions : float
        Motor speed in revolutions per second.
    gear_ratio : float
        Gearbox transmission ratio i = n_motor / n_pulley (dimensionless).

    Returns
    -------
    float
        Pulley speed in revolutions per second.

    Raises
    ------
    ValueError
        If gear_ratio is zero or negative.

    Notes
    -----
    n_pulley = n_motor / i
    """
    if gear_ratio <= 0:
        raise ValueError(f"gear_ratio must be positive, got {gear_ratio}")
    return motor_revolutions / gear_ratio


def _motor_revolutions_from_pulley_revolutions_and_gear_ratio(
    pulley_revolutions: float, gear_ratio: float
) -> float:
    """
    Calculate the motor revolutions from pulley revolutions and gear ratio.

    Parameters
    ----------
    pulley_revolutions : float
        Pulley speed in revolutions per second.
    gear_ratio : float
        Gearbox transmission ratio i = n_motor / n_pulley (dimensionless).

    Returns
    -------
    float
        Motor speed in revolutions per second.

    Notes
    -----
    n_motor = n_pulley * i
    """
    return pulley_revolutions * gear_ratio


def _gear_ratio_from_motor_revolutions_and_pulley_revolutions(
    motor_revolutions: float, pulley_revolutions: float
) -> float:
    """
    Calculate the gear ratio from motor and pulley revolutions.

    Parameters
    ----------
    motor_revolutions : float
        Motor speed in revolutions per second.
    pulley_revolutions : float
        Pulley speed in revolutions per second.

    Returns
    -------
    float
        Gearbox transmission ratio (dimensionless).

    Raises
    ------
    ValueError
        If pulley_revolutions is zero or negative.

    Notes
    -----
    i = n_motor / n_pulley
    """
    if pulley_revolutions <= 0:
        raise ValueError(
            f"pulley_revolutions must be positive, got {pulley_revolutions}"
        )
    return motor_revolutions / pulley_revolutions


def _synchronous_revolutions_from_supply_frequency_and_pole_pairs(
    supply_frequency: float, pole_pairs: int
) -> float:
    """
    Calculate the synchronous revolutions from supply frequency and pole pairs.

    Parameters
    ----------
    supply_frequency : float
        Supply frequency in hertz.
    pole_pairs : int
        Number of motor pole pairs.

    Returns
    -------
    float
        Synchronous speed in revolutions per second.

    Raises
    ------
    ValueError
        If pole_pairs is zero or negative.

    Notes
    -----
    n_sync = f / p
    """
    if pole_pairs <= 0:
        raise ValueError(f"pole_pairs must be positive, got {pole_pairs}")
    return supply_frequency / pole_pairs


def _motor_revolutions_from_synchronous_revolutions_and_slip(
    synchronous_revolutions: float, slip: float
) -> float:
    """
    Calculate the motor revolutions from synchronous revolutions and slip.

    Parameters
    ----------
    synchronous_revolutions : float
        Synchronous speed in revolutions per second.
    slip : float
        Motor slip (dimensionless).

    Returns
    -------
    float
        Motor speed in revolutions per second.

    Notes
    -----
    n_motor = n_sync * (1 - s)
    """
    return synchronous_revolutions * (1 - slip)


def _slip_from_synchronous_revolutions_and_motor_revolutions(
    synchronous_revolutions: float, motor_revolutions: float
) -> float:
    """
    Calculate the motor slip from synchronous and motor revolutions.

    Parameters
    ----------
    synchronous_revolutions : float
        Synchronous speed in revolutions per second.
    motor_revolutions : float
        Motor speed in revolutions per second.

    Returns
    -------
    float
        Motor slip (dimensionless).

    Raises
    ------
    ValueError
        If synchronous_revolutions is zero or negative, or if motor_revolutions
        exceeds synchronous_revolutions.

    Notes
    -----
    s = (n_sync - n_motor) / n_sync
    """
    if synchronous_revolutions <= 0:
        raise ValueError(
            f"synchronous_revolutions must be positive, got {synchronous_revolutions}"
        )
    if motor_revolutions > synchronous_revolutions:
        raise ValueError(
            "motor_revolutions must not exceed synchronous_revolutions, "
            f"got motor_revolutions={motor_revolutions}, "
            f"synchronous_revolutions={synchronous_revolutions}"
        )
    return (synchronous_revolutions - motor_revolutions) / synchronous_revolutions


def _belt_speed_from_motor_revolutions_gear_ratio_and_pulley_diameter(
    motor_revolutions: float, gear_ratio: float, pulley_diameter: float
) -> float:
    """
    Calculate the belt speed from motor revolutions, gear ratio, and pulley diameter.

    Parameters
    ----------
    motor_revolutions : float
        Motor speed in revolutions per second.
    gear_ratio : float
        Gearbox transmission ratio i = n_motor / n_pulley (dimensionless).
    pulley_diameter : float
        Effective pulley diameter at the belt contact in meters.

    Returns
    -------
    float
        Belt speed in meters per second.

    Raises
    ------
    ValueError
        If gear_ratio is zero or negative.

    Notes
    -----
    v = pi * D_eff * n_motor / i
    """
    if gear_ratio <= 0:
        raise ValueError(f"gear_ratio must be positive, got {gear_ratio}")
    return pi * pulley_diameter * motor_revolutions / gear_ratio


def _gear_ratio_from_belt_speed_motor_revolutions_and_pulley_diameter(
    belt_speed: float, motor_revolutions: float, pulley_diameter: float
) -> float:
    """
    Calculate the gear ratio from belt speed, motor revolutions, and pulley diameter.

    Parameters
    ----------
    belt_speed : float
        Belt speed in meters per second.
    motor_revolutions : float
        Motor speed in revolutions per second.
    pulley_diameter : float
        Effective pulley diameter at the belt contact in meters.

    Returns
    -------
    float
        Gearbox transmission ratio (dimensionless).

    Raises
    ------
    ValueError
        If belt_speed is zero or negative.

    Notes
    -----
    i = pi * D_eff * n_motor / v
    """
    if belt_speed <= 0:
        raise ValueError(f"belt_speed must be positive, got {belt_speed}")
    return pi * pulley_diameter * motor_revolutions / belt_speed


def _pulley_diameter_from_belt_speed_motor_revolutions_and_gear_ratio(
    belt_speed: float, motor_revolutions: float, gear_ratio: float
) -> float:
    """
    Calculate the effective pulley diameter from belt speed, motor revolutions, and gear ratio.

    Parameters
    ----------
    belt_speed : float
        Belt speed in meters per second.
    motor_revolutions : float
        Motor speed in revolutions per second.
    gear_ratio : float
        Gearbox transmission ratio i = n_motor / n_pulley (dimensionless).

    Returns
    -------
    float
        Effective pulley diameter at the belt contact in meters.

    Raises
    ------
    ValueError
        If motor_revolutions is zero or negative.

    Notes
    -----
    D_eff = v * i / (pi * n_motor)
    """
    if motor_revolutions <= 0:
        raise ValueError(f"motor_revolutions must be positive, got {motor_revolutions}")
    return belt_speed * gear_ratio / (pi * motor_revolutions)


def _motor_revolutions_from_belt_speed_gear_ratio_and_pulley_diameter(
    belt_speed: float, gear_ratio: float, pulley_diameter: float
) -> float:
    """
    Calculate the motor revolutions from belt speed, gear ratio, and pulley diameter.

    Parameters
    ----------
    belt_speed : float
        Belt speed in meters per second.
    gear_ratio : float
        Gearbox transmission ratio i = n_motor / n_pulley (dimensionless).
    pulley_diameter : float
        Effective pulley diameter at the belt contact in meters.

    Returns
    -------
    float
        Motor speed in revolutions per second.

    Raises
    ------
    ValueError
        If pulley_diameter is zero or negative.

    Notes
    -----
    n_motor = v * i / (pi * D_eff)
    """
    if pulley_diameter <= 0:
        raise ValueError(f"pulley_diameter must be positive, got {pulley_diameter}")
    return belt_speed * gear_ratio / (pi * pulley_diameter)
