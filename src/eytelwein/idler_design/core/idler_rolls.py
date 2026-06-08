from pint import Quantity
from eytelwein.belt_conveyor_design import IdlerSets
from eytelwein.main.units import get_unit_registry
from eytelwein.idler_design.core._idler_rolls import (
    _load_factor_determining_idler_roll_load_due_to_material,
    _load_factor_determining_idler_roll_load_due_to_conveyor_belt,
)

# Get the unit registry
u = get_unit_registry()


def load_factor_determining_idler_roll_load_due_to_material(
    idler_roll_arrangement: IdlerSets,
    troughing_angle: Quantity,
    unit: str = "dimensionless",
    precision: int | None = None,
) -> Quantity:
    """
    Calculate the load factor determining idler roll load due to material.

    This factor is used to determine the load distribution on idler rolls based on the
    idler roll arrangement (flat, V-shaped, or three-roll trough) and the troughing angle.

    Parameters
    ----------
    idler_roll_arrangement : IdlerSets
        The arrangement of the idler rolls. Must be one of FLAT_TROUGH, V_TROUGH, or THREE_TROUGH.
    troughing_angle : Quantity
        The troughing angle of the idlers, typically in degrees.
    unit : str, optional
        The unit of the output. Must be dimensionless. Default is "dimensionless".
    precision : int | None, optional
        The number of decimal places for the result. Default is None. Use None to skip rounding and retain maximum available precision.

    Returns
    -------
    Quantity
        The load factor as a dimensionless value.

    Raises
    ------
    ValueError
        If the idler_roll_arrangement is not one of the supported types (FLAT_TROUGH, V_TROUGH, THREE_TROUGH).
        If the specified unit is not dimensionless.
        If the troughing_angle is not provided with a valid unit.
    """  # Check that the output unit is dimensionless
    try:
        test_unit = u(unit)
        if test_unit.dimensionality:  # If has any dimension, it's not dimensionless
            raise ValueError(f"The unit '{unit}' must be dimensionless.")
    except Exception as e:
        raise ValueError(f"Error checking unit '{unit}': {e}")

    # Convert troughing angle to degrees if it has a unit
    if isinstance(troughing_angle, Quantity):
        troughing_angle_deg = troughing_angle.to("degree").magnitude
    else:
        # If troughing_angle is provided without units, assume it's already in degrees
        troughing_angle_deg = float(troughing_angle)  # Call the implementation function
    result = _load_factor_determining_idler_roll_load_due_to_material(
        idler_roll_arrangement, troughing_angle_deg
    )

    # Scale result based on unit if needed (e.g., percent = dimensionless * 100)
    if unit == "percent":
        result = result * 100

    # Round only when explicitly requested and attach requested unit
    result_with_unit = result * u(unit)
    if precision is not None:
        result_with_unit = round(result_with_unit, precision)

    return result_with_unit


def load_factor_determining_idler_roll_load_due_to_conveyor_belt(
    idler_roll_arrangement: IdlerSets,
    idler_roll_length_center: Quantity,
    belt_width: Quantity,
    precision: int | None = None,
) -> float:
    """
    Calculate the load factor determining idler roll load due to conveyor belt.

    This function determines the distribution factor for belt loads on idler rolls based on the
    idler arrangement type. For three-trough arrangements, the factor depends on the geometry
    of the center roll relative to the belt width.

    The load factor formulas:
    - FLAT_TROUGH: f_belt = 1.0
    - V_TROUGH: f_belt = 0.5
    - THREE_TROUGH: f_belt = (l_center + 20 mm) / B

    Where:
    - f_belt is the dimensionless load factor for belt loads
    - l_center is the center idler roll length
    - B is the belt width
    - 20 mm is a constant offset

    Parameters
    ----------
    idler_roll_arrangement : IdlerSets
        Type of idler roll arrangement (FLAT_TROUGH, V_TROUGH, or THREE_TROUGH)
    idler_roll_length_center : Quantity
        Length of the center idler roll (typically in millimeters)
    belt_width : Quantity
        Width of the belt (typically in millimeters)
    precision : int | None, optional
        Number of decimal places for the result. Default is None. Use None to skip rounding and retain maximum available precision.

    Returns
    -------
    float
        Dimensionless load factor for belt loads on idler rolls

    Raises
    ------
    ValueError
        If there is an error in converting units or if idler_roll_arrangement is invalid
        If center idler roll length or belt width are not positive

    Examples
    --------
    >>> from eytelwein.idler_design.core.idler_rolls import load_factor_determining_idler_roll_load_due_to_conveyor_belt
    >>> from eytelwein.belt_conveyor_design import IdlerSets
    >>> from eytelwein.main.units import get_unit_registry
    >>> u = get_unit_registry()
    >>>
    >>> # Flat trough arrangement
    >>> factor = load_factor_determining_idler_roll_load_due_to_conveyor_belt(
    ...     IdlerSets.FLAT_TROUGH,
    ...     500 * u.millimeter,
    ...     1200 * u.millimeter
    ... )
    >>> print(factor)  # 1.0
    1 dimensionless
    >>>
    >>> # Three-trough arrangement
    >>> factor = load_factor_determining_idler_roll_load_due_to_conveyor_belt(
    ...     IdlerSets.THREE_TROUGH,
    ...     480 * u.millimeter,
    ...     1200 * u.millimeter,
    ...     precision=3,
    ... )
    >>> print(factor)  # 0.417 (approximately)
    0.417 dimensionless
    """
    try:
        # Convert inputs to standard units (millimeters)
        center_length_mm = idler_roll_length_center.to(u.millimeter)
        belt_width_mm = belt_width.to(u.millimeter)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Validate input values
    if center_length_mm.magnitude <= 0:
        raise ValueError(
            f"Center idler roll length must be positive, got {idler_roll_length_center}"
        )

    if belt_width_mm.magnitude <= 0:
        raise ValueError(f"Belt width must be positive, got {belt_width}")

    # Call the private implementation with raw values
    result = (
        _load_factor_determining_idler_roll_load_due_to_conveyor_belt(
            idler_roll_arrangement, center_length_mm.magnitude, belt_width_mm.magnitude
        )
        * u.dimensionless
    )

    # Apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result
