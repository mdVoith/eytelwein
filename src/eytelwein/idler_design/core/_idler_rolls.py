from eytelwein.belt_conveyor_design import IdlerSets
from eytelwein.main.units import get_unit_registry

# Get the unit registry
u = get_unit_registry()


def _load_factor_determining_idler_roll_load_due_to_material(
    idler_roll_arrangement: IdlerSets, troughing_angle: float
) -> float:
    """
    Load factor determining idler roll load due to material.

    :return: Load factor determining idler roll load due to material.
    """
    if idler_roll_arrangement == IdlerSets.FLAT_TROUGH:
        return 1.0
    elif idler_roll_arrangement == IdlerSets.V_TROUGH:
        return 0.5
    elif idler_roll_arrangement == IdlerSets.THREE_TROUGH:
        return 0.5 + 0.005 * troughing_angle
    else:
        raise ValueError(
            "Invalid idler roll arrangement. Must be one of: FLAT_TROUGH, V_TROUGH, THREE_TROUGH."
        )


def _load_factor_determining_idler_roll_load_due_to_conveyor_belt(
    idler_roll_arrangement: IdlerSets,
    idler_roll_length_center: float,
    belt_width: float,
) -> float:
    """
    Calculate the load factor determining idler roll load due to conveyor belt.

    This function determines the distribution factor for belt loads on idler rolls based on the
    idler arrangement type. For three-trough arrangements, the factor depends on the geometry
    of the center roll relative to the belt width.

    The load factor formula for THREE_TROUGH arrangement:
    f_belt = (l_center + 20 mm) / B

    Where:
    - f_belt is the load factor for belt loads
    - l_center is the center idler roll length in mm
    - B is the belt width in mm
    - 20 mm is a constant offset

    Args:
        idler_roll_arrangement (IdlerSets): Type of idler roll arrangement
        idler_roll_length_center (float): Length of center idler roll in millimeters
        belt_width (float): Width of the belt in millimeters

    Returns:
        float: Dimensionless load factor for belt loads on idler rolls

    Raises:
        ValueError: If idler_roll_arrangement is not a valid IdlerSets value
        ValueError: If belt_width is zero or negative (for THREE_TROUGH arrangement)
    """
    if idler_roll_arrangement == IdlerSets.FLAT_TROUGH:
        return 1.0
    elif idler_roll_arrangement == IdlerSets.V_TROUGH:
        return 0.5
    elif idler_roll_arrangement == IdlerSets.THREE_TROUGH:
        if belt_width <= 0:
            raise ValueError("belt_width must be positive")
        return (idler_roll_length_center + 20) / belt_width
    else:
        raise ValueError(
            "Invalid idler roll arrangement. Must be one of: FLAT_TROUGH, V_TROUGH, THREE_TROUGH."
        )
