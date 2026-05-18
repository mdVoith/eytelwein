import numpy as np
from pint import Quantity
from eytelwein.main.units import get_unit_registry
from eytelwein.belt_conveyor_design.core._resistance_and_power_for_steady_operations import (
    _friction_resistance_of_skirting_board_from_material_flow,
    _gradient_resistance,
    _total_power_at_drive_pulley_due_to_motion_resistances,
)

# Get the unit registry
u = get_unit_registry()


def gradient_resistance(
    height_difference: Quantity,
    line_load_belt: Quantity,
    line_load_material: Quantity | None = None,
    unit: str = "newton",
    precision: int = 2,
) -> Quantity:
    """
    Calculate the gradient resistance of a belt conveyor.

    This function computes the gradient resistance based on the height difference,
    line load of the belt, and line load of the material.

    The gradient resistance is calculated as:

    F_St = H · g · (m'G + m'L)

    Where:
    - F_St is the gradient resistance
    - H is the height difference
    - g is the standard gravity (9.81 m/s²)
    - m'G is the line load of the belt
    - m'L is the line load of the material

    When line_load_material is None, a value of 0 kg/m is used (representing an empty belt).

    Parameters
    ----------
    height_difference : Quantity
        The height difference in the conveyor path (typically in meters).    line_load_belt : Quantity
        The line load of the belt (typically in kg/m).
    line_load_material : Optional[Quantity]
        The line load of the material (typically in kg/m).
        When None, a value of 0 kg/m is used (representing an empty belt).
    unit : str, optional
        The unit for the returned resistance. Default is "newton".
    precision : int, optional
        The number of decimal places for the result. Default is 2.

    Returns
    -------
    Quantity
        The gradient resistance with the specified unit.

    Raises
    ------
    ValueError
        If there is an error in converting units.
        If any of the input values are invalid (e.g., negative height difference).
    """
    # Create the default value using the registry
    if line_load_material is None:
        line_load_material = u.Quantity(0, u.kilogram / u.meter)

    try:
        # Convert inputs to standard units
        height_m = height_difference.to(u.meter)
        belt_load_kgpm = line_load_belt.to(u.kilogram / u.meter)
        material_load_kgpm = line_load_material.to(u.kilogram / u.meter)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Validate input values
    if height_m.magnitude < 0:
        raise ValueError(
            f"Height difference must be non-negative, got {height_difference}"
        )

    if belt_load_kgpm.magnitude < 0:
        raise ValueError(f"Belt line load must be non-negative, got {line_load_belt}")

    if material_load_kgpm.magnitude < 0:
        raise ValueError(
            f"Material line load must be non-negative, got {line_load_material}"
        )

    # Ensure the output unit is valid
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(
            f"Invalid unit: {unit}. Error: {e}"
        )  # Call the private implementation with raw values
    result = (
        _gradient_resistance(
            height_m.magnitude, belt_load_kgpm.magnitude, material_load_kgpm.magnitude
        )
        * u.newton
    )

    try:
        # Attach the appropriate unit
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(f"Error in attaching unit '{unit}': {e}")

    # Apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def gradient_resistance_sections(
    height_differences: Quantity | np.ndarray,
    line_load_belt: Quantity | np.ndarray,
    line_load_material: Quantity | np.ndarray | None = None,
    unit: str = "newton",
    precision: int = 2,
) -> Quantity:
    """
     Calculate gradient resistance for multiple conveyor sections.

     This function computes the gradient resistance based on the height differences,
     line loads of the belt, and line loads of the material for multiple sections
    , using vectorized calculations.

     The gradient resistance is calculated as:

     F_St = H · g · (m'G + m'L)

     Where:
     - F_St is the gradient resistance
     - H is the height difference
     - g is the standard gravity (9.81 m/s²)
     - m'G is the line load of the belt
     - m'L is the line load of the material

     Parameters
     ----------
     height_differences : Quantity or np.ndarray
         The height differences for each section (typically in meters).
         Can be a single Quantity or a numpy array of Quantities.
     line_load_belt : Quantity or np.ndarray
         The line load of the belt (typically in kg/m).
         Can be a single value applied to all sections or section-specific values.
     line_load_material : Optional[Quantity or np.ndarray]
         The line load of the material (typically in kg/m).
         Can be a single value, section-specific values, or None for return strands.
         When None, a value of 0 kg/m is used for all sections (representing empty belts).
     unit : str, optional
         The unit for the returned resistance array. Default is "newton".
     precision : int, optional
         The number of decimal places for the results. Default is 2.

     Returns
     -------
     Quantity
         Array of gradient resistances for each section with the specified unit.

     Raises
     ------
     ValueError
         If there is an error in converting units.
         If array dimensions don't match.
         If any input values are invalid (e.g., negative height differences).
    """
    # Create the default material load if None
    if line_load_material is None:
        if isinstance(line_load_belt, np.ndarray):
            # Create array of zeros with same shape as belt load
            material_shape = np.shape(line_load_belt)
            line_load_material = u.Quantity(
                np.zeros(material_shape), u.kilogram / u.meter
            )
        else:
            # Create single zero value
            line_load_material = u.Quantity(
                0, u.kilogram / u.meter
            )  # Convert inputs to numpy arrays
    try:
        # Convert height differences to array of meters
        if isinstance(height_differences, np.ndarray):
            heights_m = np.array([h.to(u.meter).magnitude for h in height_differences])
        else:
            heights_m = np.array([height_differences.to(u.meter).magnitude])

        # Convert belt loads to array of kg/m
        if isinstance(line_load_belt, np.ndarray):
            belt_loads_kgpm = np.array(
                [b.to(u.kilogram / u.meter).magnitude for b in line_load_belt]
            )
        else:
            # Create array with same shape as heights
            belt_loads_kgpm = np.full(
                heights_m.shape, line_load_belt.to(u.kilogram / u.meter).magnitude
            )

        # Convert material loads to array of kg/m
        if isinstance(line_load_material, np.ndarray):
            material_loads_kgpm = np.array(
                [m.to(u.kilogram / u.meter).magnitude for m in line_load_material]
            )
        else:
            # Create array with same shape as heights
            material_loads_kgpm = np.full(
                heights_m.shape, line_load_material.to(u.kilogram / u.meter).magnitude
            )
    except Exception as e:
        raise ValueError(
            f"Error in converting units to arrays: {e}"
        )  # Validate array dimensions
    if not (heights_m.shape == belt_loads_kgpm.shape == material_loads_kgpm.shape):
        raise ValueError(
            f"Inconsistent array shapes: heights {heights_m.shape}, "
            f"belt loads {belt_loads_kgpm.shape}, material loads {material_loads_kgpm.shape}"
        )

    # Validate input values - Note: we allow negative height differences as they represent downward slopes
    if np.any(belt_loads_kgpm < 0):
        raise ValueError("Belt line loads must be non-negative")

    if np.any(material_loads_kgpm < 0):
        raise ValueError("Material line loads must be non-negative")

    # Ensure the output unit is valid
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(
            f"Invalid unit: {unit}. Error: {e}"
        )  # Compute gradient resistance for each section
    vectorized_gradient_resistance = np.frompyfunc(_gradient_resistance, 3, 1)
    resistances = np.array(
        vectorized_gradient_resistance(heights_m, belt_loads_kgpm, material_loads_kgpm),
        dtype=float,
    )

    # Ensure result is a 1D array for consistency
    if resistances.ndim > 1:
        resistances = resistances.flatten()

    # Attach units to the result array
    result = resistances * u.newton

    # Convert to requested output unit
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(f"Error in converting to {unit}: {e}")

    # Apply precision if specified
    if precision is not None:
        result = np.round(result, precision)

    return result


def total_power_at_drive_pulley_due_to_motion_resistances(
    motion_resistance: Quantity,
    belt_speed: Quantity,
    unit: str = "watt",
    precision: int = 2,
) -> Quantity:
    """
    Calculate the total power at the drive pulley due to motion resistances.

    This function computes the total power required at the drive pulley based on
    the given motion resistance and belt speed.

    The power is calculated as:

    P = F_w * v

    Where:
    - P is the power at the drive pulley
    - F_w is the motion resistance
    - v is the belt speed

    Parameters
    ----------
    motion_resistance : Quantity
        The motion resistance (typically in newtons).
    belt_speed : Quantity
        The speed of the belt (typically in meters per second).
    unit : str, optional
        The unit for the returned power. Default is "watt".
    precision : int, optional
        The number of decimal places for the result. Default is 2.

    Returns
    -------
    Quantity
        The total power at the drive pulley with the specified unit.

    Raises
    ------
    ValueError
        If there is an error in converting units.
    """
    try:
        # Convert inputs to standard units
        resistance_n = motion_resistance.to(u.newton)
        speed_mps = belt_speed.to(u.meter / u.second)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Ensure the output unit is valid
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Call the private implementation with raw values
    result = (
        _total_power_at_drive_pulley_due_to_motion_resistances(
            resistance_n.magnitude, speed_mps.magnitude
        )
        * u.watt
    )

    try:
        # Convert to requested output unit
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(f"Error in attaching unit '{unit}': {e}")

    # Apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def friction_resistance_of_skirting_board_from_material_flow(
    material_mass_flow: Quantity,
    belt_velocity: Quantity,
    material_density: Quantity,
    rankine_coefficient: Quantity,
    skirting_board_width: Quantity,
    skirting_board_length: Quantity,
    central_roller_length: Quantity,
    troughing_angle: Quantity,
    friction_coefficient_material_skirting: Quantity,
    unit: str = "newton",
    precision: int | None = 2,
) -> Quantity:
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
    material_mass_flow : Quantity
        Mass flow of conveyed material (typically in kg/s)
    belt_velocity : Quantity
        Velocity of the conveyor belt (typically in m/s)
    material_density : Quantity
        Bulk material density (typically in kg/m³)
    rankine_coefficient : Quantity
        Rankine coefficient (empirical dimensionless factor)
    skirting_board_width : Quantity
        Width of the lateral skirting board (typically in m)
    skirting_board_length : Quantity
        Length of the lateral skirting board (typically in m)
    central_roller_length : Quantity
        Length of the central roller in the 3-roller idler set (typically in m)
    troughing_angle : Quantity
        Troughing angle of the conveyor belt (angle of trough formation).
        Typically in degrees or radians.
    friction_coefficient_material_skirting : Quantity
        Coefficient of friction between material and skirting surface (dimensionless)
    unit : str, optional
        The unit for the returned resistance. Default is "newton".
    precision : int or None, optional
        The number of decimal places for the result. Default is 2.
        If None, no rounding is applied.

    Returns
    -------
    Quantity
        Friction resistance force with the specified unit.

    Raises
    ------
    ValueError
        If there is an error in converting units.
        If any required parameter has incorrect dimensions.
        If any input values are physically invalid.

    See Also
    --------
    friction_resistance_per_meter_of_skirting_board_from_material_flow :
        Calculate the friction resistance per unit length (distributed force).

    Notes
    -----
    This function calculates the friction resistance between material conveyed
    and lateral chutes outside the acceleration zone of feeding points, based on
    the skirting friction formula:

    .. math::

        F_{\\text{Sch}} = c_{\\text{Rank}} \\left[ \\frac{I_m}{v \\rho} - \\frac{(b_{\\text{Sch}}^{2} - l_{M}^{2}) \\tan \\lambda}{4} \\right]^{2} \\cdot \\frac{\\rho g l_{\\text{Sch}} \\mu_2}{b_{\\text{Sch}}^{2}}

    Where:
    - :math:`F_{\\text{Sch}}` is the friction resistance [N]
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
    try:
        # Convert all inputs to standard internal units
        mass_flow_kgs = material_mass_flow.to(u.kilogram / u.second)
        velocity_ms = belt_velocity.to(u.meter / u.second)
        density_kgm3 = material_density.to(u.kilogram / u.meter**3)
        rankine_coeff = rankine_coefficient.to(u.dimensionless)
        board_width_m = skirting_board_width.to(u.meter)
        board_length_m = skirting_board_length.to(u.meter)
        roller_length_m = central_roller_length.to(u.meter)
        angle_rad = troughing_angle.to(u.radian)
        friction_coeff = friction_coefficient_material_skirting.to(u.dimensionless)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Validate input values (physical constraints)
    if mass_flow_kgs.magnitude <= 0:
        raise ValueError(
            f"Material mass flow must be positive, got {material_mass_flow}"
        )
    if velocity_ms.magnitude <= 0:
        raise ValueError(f"Belt velocity must be positive, got {belt_velocity}")
    if density_kgm3.magnitude <= 0:
        raise ValueError(f"Material density must be positive, got {material_density}")
    if board_width_m.magnitude <= 0:
        raise ValueError(
            f"Skirting board width must be positive, got {skirting_board_width}"
        )
    if board_length_m.magnitude <= 0:
        raise ValueError(
            f"Skirting board length must be positive, got {skirting_board_length}"
        )
    if roller_length_m.magnitude < 0:
        raise ValueError(
            f"Central roller length must be non-negative, got {central_roller_length}"
        )
    if friction_coeff.magnitude < 0:
        raise ValueError(
            f"Friction coefficient must be non-negative, got {friction_coefficient_material_skirting}"
        )
    if not (0 <= angle_rad.magnitude <= np.pi / 2):
        raise ValueError(
            f"Troughing angle must be between 0 and π/2 radians, got {troughing_angle}"
        )

    # Validate output unit
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Call the private implementation with raw magnitude values
    result = (
        _friction_resistance_of_skirting_board_from_material_flow(
            mass_flow_kgs.magnitude,
            velocity_ms.magnitude,
            density_kgm3.magnitude,
            rankine_coeff.magnitude,
            board_width_m.magnitude,
            board_length_m.magnitude,
            roller_length_m.magnitude,
            angle_rad.magnitude,
            friction_coeff.magnitude,
        )
        * u.newton
    )

    try:
        # Convert to requested output unit
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(f"Error in attaching unit '{unit}': {e}")

    # Apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def friction_resistance_per_meter_of_skirting_board_from_material_flow(
    material_mass_flow: Quantity,
    belt_velocity: Quantity,
    material_density: Quantity,
    rankine_coefficient: Quantity,
    skirting_board_width: Quantity,
    skirting_board_length: Quantity,
    central_roller_length: Quantity,
    troughing_angle: Quantity,
    friction_coefficient_material_skirting: Quantity,
    unit: str = "newton/meter",
    precision: int | None = 2,
) -> Quantity:
    """
    Calculate friction resistance per unit length between material and lateral skirting board.

    Computes the friction resistance force per meter of skirting board length occurring
    between conveyed material and the lateral skirting (chute) boards outside the
    acceleration zone of feeding points. This represents the distributed force intensity
    along the skirting board length.

    This calculation divides the total friction resistance by the skirting board length
    to obtain the force per unit length, which is useful for analyzing stress distribution
    and structural loading.

    Parameters
    ----------
    material_mass_flow : Quantity
        Mass flow of conveyed material (typically in kg/s)
    belt_velocity : Quantity
        Velocity of the conveyor belt (typically in m/s)
    material_density : Quantity
        Bulk material density (typically in kg/m³)
    rankine_coefficient : Quantity
        Rankine coefficient (empirical dimensionless factor)
    skirting_board_width : Quantity
        Width of the lateral skirting board (typically in m)
    skirting_board_length : Quantity
        Length of the lateral skirting board (typically in m)
    central_roller_length : Quantity
        Length of the central roller in the 3-roller idler set (typically in m)
    troughing_angle : Quantity
        Troughing angle of the conveyor belt (angle of trough formation).
        Typically in degrees or radians.
    friction_coefficient_material_skirting : Quantity
        Coefficient of friction between material and skirting surface (dimensionless)
    unit : str, optional
        The unit for the returned resistance per unit length. Default is "newton/meter".
    precision : int or None, optional
        The number of decimal places for the result. Default is 2.
        If None, no rounding is applied.

    Returns
    -------
    Quantity
        Friction resistance force per unit length with the specified unit.

    Raises
    ------
    ValueError
        If there is an error in converting units.
        If any required parameter has incorrect dimensions.
        If any input values are physically invalid.

    See Also
    --------
    friction_resistance_of_skirting_board_from_material_flow :
        Calculate the total friction resistance force.

    Notes
    -----
    This function calculates the friction resistance per unit length of skirting board
    based on the relationship:

    .. math::

        F_{\\text{Sch,lin}} = \\frac{F_{\\text{Sch}}}{l_{\\text{Sch}}}

    Where:
    - :math:`F_{\\text{Sch,lin}}` is the friction resistance per unit length [N/m]
    - :math:`F_{\\text{Sch}}` is the total friction resistance [N]
    - :math:`l_{\\text{Sch}}` is the skirting board length [m]

    The total friction resistance :math:`F_{\\text{Sch}}` is calculated using the
    the skirting friction formula (see `friction_resistance_of_skirting_board_from_material_flow`).

    Physical Interpretation:
    - Represents the distributed force intensity along the skirting board
    - Useful for structural analysis and stress calculations
    - Independent of skirting board length (normalized value)
    - Same material flow and geometry dependencies as total force

    Examples
    --------
    Calculate friction resistance per meter for typical conveyor parameters:

    >>> from eytelwein.main.units import get_unit_registry
    >>> u = get_unit_registry()
    >>> mass_flow = 100 * u.kilogram / u.second
    >>> belt_velocity = 2.5 * u.meter / u.second
    >>> material_density = 1000 * u.kilogram / u.meter**3
    >>> rankine_coefficient = 1.2 * u.dimensionless
    >>> board_width = 1.0 * u.meter
    >>> board_length = 3.0 * u.meter
    >>> roller_length = 0.8 * u.meter
    >>> troughing_angle = 30 * u.degree
    >>> friction_coeff = 0.4 * u.dimensionless
    >>> result = friction_resistance_per_meter_of_skirting_board_from_material_flow(
    ...     mass_flow, belt_velocity, material_density, rankine_coefficient,
    ...     board_width, board_length, roller_length, troughing_angle, friction_coeff
    ... )
    >>> print(f"Force per meter: {result}")  # doctest: +SKIP
    Force per meter: 0.68 newton / meter

    Calculate with different output units:

    >>> result_kn = friction_resistance_per_meter_of_skirting_board_from_material_flow(
    ...     mass_flow, belt_velocity, material_density, rankine_coefficient,
    ...     board_width, board_length, roller_length, troughing_angle, friction_coeff,
    ...     unit="kilonewton/meter", precision=6
    ... )
    >>> print(f"Force per meter: {result_kn}")  # doctest: +SKIP
    Force per meter: 0.000676 kilonewton / meter
    """
    # Calculate total friction resistance (handles all validation and unit conversion)
    total_force = friction_resistance_of_skirting_board_from_material_flow(
        material_mass_flow,
        belt_velocity,
        material_density,
        rankine_coefficient,
        skirting_board_width,
        skirting_board_length,
        central_roller_length,
        troughing_angle,
        friction_coefficient_material_skirting,
        unit="newton",
        precision=None,  # Don't round yet
    )

    # Convert skirting board length to meters for division
    try:
        board_length_m = skirting_board_length.to(u.meter)
    except Exception as e:
        raise ValueError(f"Error in converting skirting board length: {e}")

    # Divide total force by length to get force per unit length
    result = total_force / board_length_m

    # Validate output unit
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Convert to requested output unit
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(f"Error in converting to unit '{unit}': {e}")

    # Apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result
