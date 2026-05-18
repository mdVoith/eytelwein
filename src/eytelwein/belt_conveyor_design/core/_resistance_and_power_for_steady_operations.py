import numpy as np

from eytelwein.main.constants import STANDARD_GRAVITY_VALUE


def _friction_resistance_of_skirting_board_from_material_flow(
    material_mass_flow: float,
    belt_velocity: float,
    material_density: float,
    rankine_coefficient: float,
    skirting_board_width: float,
    skirting_board_length: float,
    central_roller_length: float,
    troughing_angle: float,
    friction_coefficient_material_skirting: float,
) -> float:
    """
    Calculate friction resistance between material and lateral skirting board.

    Computes the friction resistance force occurring between conveyed material
    and the lateral skirting (chute) boards outside the acceleration zone of
    feeding points. This force arises from the material's inertia and friction
    with the skirting surface as material flows through the troughed conveyor.

    This calculation is based on the friction resistance formula,
    which accounts for complex interactions between material velocity, geometry,
    and friction properties.

    Parameters
    ----------
    material_mass_flow : float
        Mass flow of conveyed material [kg/s]
    belt_velocity : float
        Velocity of the conveyor belt [m/s]
    material_density : float
        Bulk material density [kg/m³]
    rankine_coefficient : float
        Rankine coefficient (empirical dimensionless factor) []
    skirting_board_width : float
        Width of the lateral skirting board [m]
    skirting_board_length : float
        Length of the lateral skirting board [m]
    central_roller_length : float
        Length of the central roller in the 3-roller idler set [m]
    troughing_angle : float
        Troughing angle of the conveyor belt (angle of trough formation) [radians]
    friction_coefficient_material_skirting : float
        Coefficient of friction between material and skirting surface [] (μ₂)

    Returns
    -------
    float
        Friction resistance force [N]

    Raises
    ------
    ValueError
        If any required parameter is negative or zero
    ValueError
        If troughing_angle is outside physical range (0 <= λ <= π/2 radians)

    Notes
    -----
    This function calculates the friction resistance between material conveyed
    and lateral chutes outside the acceleration zone of feeding points, based on
    the skirting friction formula:

    .. math::

        F_{\\text{Sch}} = c_{\\text{Rank}} \\left[ \\frac{I_m}{v \\rho} - \\frac{(b_{\\text{Sch}}^{2} - l_{M}^{2}) \\tan \\lambda}{4} \\right]^{2} \\cdot \\frac{\\rho g l_{\\text{Sch}} \\mu_2}{b_{\\text{Sch}}^{2}}

    Where:
    - :math:`F_{\\text{Sch}}` is the friction resistance between material conveyed and lateral chutes outside the acceleration zone of feeding points [N]
    - :math:`c_{\\text{Rank}}` is the Rankine coefficient []
    - :math:`I_m` is the material mass flow [kg/s]
    - :math:`v` is the belt velocity [m/s]
    - :math:`\\rho` is the bulk material density [kg/m³]
    - :math:`b_{\\text{Sch}}` is the skirting board width [m]
    - :math:`l_M` is the central roller length [m]
    - :math:`\\lambda` is the troughing angle [radians]
    - :math:`g` is gravitational acceleration [m/s²]
    - :math:`l_{\\text{Sch}}` is the skirting board length [m]
    - :math:`\\mu_2` is the friction coefficient []

    The formula consists of two main components:
    1. A complex term involving material dynamics and geometry (squared)
    2. A term accounting for normal force and friction on the skirting surface

    Physical Interpretation:
    - Higher material flow → higher resistance
    - Higher belt velocity → lower resistance (dilution effect)
    - Larger troughing angle → reduces the dynamic component
    - Longer/wider skirting → increases resistance from friction
    """
    # Input validation
    if material_mass_flow <= 0:
        raise ValueError("material_mass_flow must be positive")
    if belt_velocity <= 0:
        raise ValueError("belt_velocity must be positive")
    if material_density <= 0:
        raise ValueError("material_density must be positive")
    if skirting_board_width <= 0:
        raise ValueError("skirting_board_width must be positive")
    if skirting_board_length <= 0:
        raise ValueError("skirting_board_length must be positive")
    if central_roller_length < 0:
        raise ValueError("central_roller_length must be non-negative")
    if friction_coefficient_material_skirting < 0:
        raise ValueError("friction_coefficient_material_skirting must be non-negative")
    if not (0 <= troughing_angle <= np.pi / 2):
        raise ValueError("troughing_angle must be between 0 and π/2 radians")

    # Calculate dynamic component: [Im / (v * ρ) - (b_Sch² - l_M²) * tan(λ) / 4]²
    velocity_density_term = material_mass_flow / (belt_velocity * material_density)
    geometric_term = (
        (skirting_board_width**2 - central_roller_length**2)
        * np.tan(troughing_angle)
        / 4
    )
    dynamic_factor = (velocity_density_term - geometric_term) ** 2

    # Calculate friction component: ρ * g * l_Sch * μ₂ / b_Sch²
    friction_factor = (
        material_density
        * STANDARD_GRAVITY_VALUE
        * skirting_board_length
        * friction_coefficient_material_skirting
    ) / (skirting_board_width**2)

    # Calculate total friction resistance: F_Sch = c_Rank * dynamic_factor * friction_factor
    friction_resistance = rankine_coefficient * dynamic_factor * friction_factor

    return friction_resistance


def _total_power_at_drive_pulley_due_to_motion_resistances(
    motion_resistance: float, belt_speed: float
) -> float:
    """
    Calculate the total power at the drive pulley due to motion resistances.

    This function computes the total power required at the drive pulley based on the given motion resistance and belt speed.

    Parameters:
    motion_resistance (float): The motion resistance in Newtons (N).
    belt_speed (float): The speed of the belt in meters per second (m/s).

    Returns:
    float: The total power at the drive pulley in Watts (W).
    """
    total_power = motion_resistance * belt_speed
    return total_power


def _gradient_resistance(
    height_difference: float, line_load_belt: float, line_load_material: float
) -> float:
    """
    Calculate the gradient resistance of a belt conveyor.

    This function computes the gradient resistance based on the height difference, line load of the belt, and line load of the material.

    Parameters:
    height_difference (float): The height difference in meters (m).
    line_load_belt (float): The line load of the belt in kilogram per meter (kg/m).
    line_load_material (float): The line load of the material in kilogram per meter (kg/m).

    Returns:
    float: The gradient resistance in Newtons (N).
    """
    gradient_resistance = (
        height_difference
        * STANDARD_GRAVITY_VALUE
        * (line_load_belt + line_load_material)
    )
    return gradient_resistance
