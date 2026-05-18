"""
Public API for horizontal curve calculations with unit handling.

This module provides the public interface for horizontal curve force calculations
with comprehensive unit validation and conversion using the Pint unit registry.
"""

from typing import Union, Optional, TYPE_CHECKING
import numpy as np

import eytelwein.main.units as u
from ._horizontal_curve_calculations import (
    _force_component_towards_inside_curve_from_belt_tension,
    _restraining_force_from_dead_weights_towards_outside_curve_conventional,
    _weight_force_belt_inside_conventional,
    _weight_force_belt_outside_conventional,
    _weight_force_belt_center_conventional,
    _weight_force_material_center_conventional,
    _weight_force_material_center_improved,
    _weight_force_material_inside_improved,
    _weight_force_material_outside_conventional,
    _weight_force_material_outside_improved,
    _weight_force_of_belt_conventional,
    _weight_force_belt_inside_improved,
    _weight_force_belt_outside_improved,
    _weight_force_belt_center_improved,
    _weight_force_of_belt_improved,
    _weight_force_material_inside_conventional,
    _tilted_idler_friction_force_inside_conventional,
    _tilted_idler_friction_force_inside_improved,
    _tilted_idler_friction_force_outside_conventional,
    _tilted_idler_friction_force_outside_improved,
    _tilted_idler_friction_force_center_conventional,
    _tilted_idler_friction_force_center_improved,
    _restraining_force_from_tilted_idlers_towards_outside_curve_conventional,
    _restraining_force_from_tilted_idlers_towards_outside_curve_improved,
    CONVENTIONAL_METHOD,
    IMPROVED_METHOD,
    VALID_METHODS,
    _weight_force_of_material_conventional,
    _weight_force_of_material_improved,
)

if TYPE_CHECKING:
    from pint import Quantity
else:
    Quantity = u.ureg.Quantity

# Default load factor values for improved methods
DEFAULT_WING_LOAD_FACTOR = 1.1
DEFAULT_CENTER_LOAD_FACTOR = 0.9

# Enhanced error message templates
ERROR_MESSAGES = {
    "unit_conversion": "Error in converting units for {param}: {error}",
    "invalid_method": "Unknown method: '{method}'. Valid options are: {valid_methods}",
    "negative_force": "Total weight force must be non-negative, got {value}",
    "invalid_width": "Belt width on section cannot exceed total belt width",
    "positive_width": "Belt width must be positive, got {value}",
    "invalid_unit": "Cannot convert result to {unit}: {error}",
}


def _get_default_load_factor(method: str, factor_type: str) -> Union[float, None]:
    """
    Get appropriate default load factor for improved methods.

    Parameters
    ----------
    method : str
        Calculation method
    factor_type : str
        Type of load factor ("wing" or "center")

    Returns
    -------
    float or None
        Default load factor value, or None for conventional method
    """
    if method != IMPROVED_METHOD:
        return None

    if factor_type == "wing":
        return DEFAULT_WING_LOAD_FACTOR
    elif factor_type == "center":
        return DEFAULT_CENTER_LOAD_FACTOR
    else:
        raise ValueError(f"Unknown factor type: {factor_type}")


def force_component_towards_inside_curve_from_belt_tension(
    belt_tension: "Quantity",
    idler_spacing: "Quantity",
    horizontal_curve_radius: "Quantity",
    unit: str = "newton",
    precision: int = 2,
) -> "Quantity":
    """
    Calculate the force component towards the inside of the curve from belt tension.

    This function provides the public API for horizontal curve force calculations
    with comprehensive unit handling and validation. It implements research-based
    methodologies for belt conveyor horizontal curve analysis.

    The force component is calculated as:

    F = T * L / R

    Where:
    - F is the force component towards the curve center
    - T is the belt tension
    - L is the idler spacing
    - R is the horizontal curve radius

    Parameters
    ----------
    belt_tension : Quantity
        Belt tension at the location of interest. Must have force dimensions [N].
    idler_spacing : Quantity
        Distance between consecutive idler sets. Must have length dimensions [m].
    horizontal_curve_radius : Quantity
        Radius of the horizontal curve. Must have length dimensions [m].
    unit : str, optional
        The unit for the returned force. Default is "newton".
    precision : int, optional
        The number of decimal places for the results. Default is 2.

    Returns
    -------
    Quantity
        Force component towards the inside of the curve with the specified unit.

    Raises
    ------
    pint.DimensionalityError
        If input quantities do not have the correct dimensions.
    ValueError
        If horizontal_curve_radius is zero or negative.
        If the output unit is invalid.

    Examples
    --------
    >>> import eytelwein.main.units as u
    >>> belt_tension = 5000 * u.ureg.newton
    >>> idler_spacing = 1.2 * u.ureg.meter
    >>> curve_radius = 50 * u.ureg.meter
    >>> force = force_component_towards_inside_curve_from_belt_tension(
    ...     belt_tension, idler_spacing, curve_radius
    ... )
    >>> print(f"Force towards curve center: {force:.1f}")
    Force towards curve center: 120.0 newton

    Notes
    -----
    Sign convention: Positive force indicates direction towards the inside of the curve,
    following standard mathematical conventions for centripetal forces.
    """
    try:
        # Convert inputs to standard units
        belt_tension_magnitude = belt_tension.to(u.ureg.newton).magnitude
        idler_spacing_magnitude = idler_spacing.to(u.ureg.meter).magnitude
        horizontal_curve_radius_magnitude = horizontal_curve_radius.to(
            u.ureg.meter
        ).magnitude
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Validate radius is positive (handle both scalars and arrays)
    if np.any(horizontal_curve_radius_magnitude <= 0):
        raise ValueError("horizontal_curve_radius must be positive")

    # Ensure the output unit is valid
    try:
        pint_unit = u.ureg.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Calculate the force component
    result_magnitude = _force_component_towards_inside_curve_from_belt_tension(
        belt_tension_magnitude,
        idler_spacing_magnitude,
        horizontal_curve_radius_magnitude,
    )

    # Attach units to the result
    result = result_magnitude * u.ureg.newton

    # Convert to requested output unit
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(f"Error in converting to {unit}: {e}")

    # Apply precision if specified
    if precision is not None:
        result = np.round(result, precision)

    return result


def force_component_towards_inside_curve_from_belt_tension_sections(
    belt_tensions: Union["Quantity", np.ndarray],
    idler_spacings: Union["Quantity", np.ndarray],
    horizontal_curve_radii: Union["Quantity", np.ndarray],
    unit: str = "newton",
    precision: int = 2,
) -> "Quantity":
    """
    Calculate force components towards the inside of curves for multiple conveyor sections.

    This function computes the force components based on belt tensions, idler spacings,
    and horizontal curve radii for multiple sections using research-based methodologies,
    with vectorized calculations for performance.

    The force component is calculated as:

    F = T * L / R

    Where:
    - F is the force component towards the curve center
    - T is the belt tension
    - L is the idler spacing
    - R is the horizontal curve radius

    Parameters
    ----------
    belt_tensions : Quantity or np.ndarray
        The belt tensions for each section (typically in newtons).
        Can be a single Quantity or a numpy array of Quantities.
    idler_spacings : Quantity or np.ndarray
        The idler spacings for each section (typically in meters).
        Can be a single value applied to all sections or section-specific values.
    horizontal_curve_radii : Quantity or np.ndarray
        The horizontal curve radii for each section (typically in meters).
        Can be a single value applied to all sections or section-specific values.
    unit : str, optional
        The unit for the returned force array. Default is "newton".
    precision : int, optional
        The number of decimal places for the results. Default is 2.

    Returns
    -------
    Quantity
        Array of force components towards the inside of curves for each section with the specified unit.

    Raises
    ------
    ValueError
        If there is an error in converting units.
        If array dimensions don't match.
        If any horizontal curve radii are zero or negative.
        If the output unit is invalid.

    Examples
    --------
    >>> import eytelwein.main.units as u
    >>> import numpy as np
    >>> belt_tensions = [3000, 4000, 5000] * u.ureg.newton
    >>> idler_spacing = 1.2 * u.ureg.meter
    >>> curve_radii = [40, 50, 60] * u.ureg.meter
    >>> forces = force_component_towards_inside_curve_from_belt_tension_sections(
    ...     belt_tensions, idler_spacing, curve_radii
    ... )
    >>> print(f"Forces: {forces:.1f}")
    Forces: [90.0 96.0 100.0] newton

    Notes
    -----
    This function supports NumPy broadcasting, allowing for flexible combinations
    of scalar and array inputs following standard mathematical conventions.
    """
    try:
        # Determine the primary array shape - use the first array and find its shape
        primary_shape = None

        # Check each input to find the first array and use its shape
        if hasattr(belt_tensions, "magnitude") and isinstance(
            belt_tensions.magnitude, np.ndarray
        ):
            primary_array = belt_tensions.magnitude
            primary_shape = primary_array.shape
        elif hasattr(idler_spacings, "magnitude") and isinstance(
            idler_spacings.magnitude, np.ndarray
        ):
            primary_array = idler_spacings.magnitude
            primary_shape = primary_array.shape
        elif hasattr(horizontal_curve_radii, "magnitude") and isinstance(
            horizontal_curve_radii.magnitude, np.ndarray
        ):
            primary_array = horizontal_curve_radii.magnitude
            primary_shape = primary_array.shape
        elif isinstance(belt_tensions, np.ndarray):
            primary_array = belt_tensions
            primary_shape = primary_array.shape
        elif isinstance(idler_spacings, np.ndarray):
            primary_array = idler_spacings
            primary_shape = primary_array.shape
        elif isinstance(horizontal_curve_radii, np.ndarray):
            primary_array = horizontal_curve_radii
            primary_shape = primary_array.shape
        else:
            # All inputs are scalars - create single element arrays
            primary_shape = (1,)

        # Convert belt tensions to array with primary shape
        if hasattr(belt_tensions, "magnitude") and isinstance(
            belt_tensions.magnitude, np.ndarray
        ):
            tensions_n = belt_tensions.to(u.ureg.newton).magnitude  # type: ignore[union-attr]
        elif isinstance(belt_tensions, np.ndarray):
            tensions_n = np.array(
                [t.to(u.ureg.newton).magnitude for t in belt_tensions]
            )
        else:
            # Create array with same shape as primary
            tensions_n = np.full(
                primary_shape,
                belt_tensions.to(u.ureg.newton).magnitude,
            )

        # Convert idler spacings to array with primary shape
        if hasattr(idler_spacings, "magnitude") and isinstance(
            idler_spacings.magnitude, np.ndarray
        ):
            spacings_m = idler_spacings.to(u.ureg.meter).magnitude  # type: ignore[union-attr]
        elif isinstance(idler_spacings, np.ndarray):
            spacings_m = np.array(
                [s.to(u.ureg.meter).magnitude for s in idler_spacings]
            )
        else:
            # Create array with same shape as primary
            spacings_m = np.full(
                primary_shape,
                idler_spacings.to(u.ureg.meter).magnitude,
            )

        # Convert curve radii to array with primary shape
        if hasattr(horizontal_curve_radii, "magnitude") and isinstance(
            horizontal_curve_radii.magnitude, np.ndarray
        ):
            radii_m = horizontal_curve_radii.to(u.ureg.meter).magnitude  # type: ignore[union-attr]
        elif isinstance(horizontal_curve_radii, np.ndarray):
            radii_m = np.array(
                [r.to(u.ureg.meter).magnitude for r in horizontal_curve_radii]
            )
        else:
            # Create array with same shape as primary
            radii_m = np.full(
                primary_shape,
                horizontal_curve_radii.to(u.ureg.meter).magnitude,
            )
    except Exception as e:
        raise ValueError(f"Error in converting units to arrays: {e}")

    # Validate array dimensions
    if not (tensions_n.shape == spacings_m.shape == radii_m.shape):
        raise ValueError(
            f"Inconsistent array shapes: tensions {tensions_n.shape}, "
            f"spacings {spacings_m.shape}, radii {radii_m.shape}"
        )

    # Validate input values
    if np.any(tensions_n < 0):
        raise ValueError("Belt tensions must be non-negative")

    if np.any(spacings_m <= 0):
        raise ValueError("Idler spacings must be positive")

    if np.any(radii_m <= 0):
        raise ValueError("Horizontal curve radii must be positive")

    # Ensure the output unit is valid
    try:
        pint_unit = u.ureg.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    vectorized_force_component = np.frompyfunc(
        _force_component_towards_inside_curve_from_belt_tension, 3, 1
    )
    forces = np.array(
        vectorized_force_component(tensions_n, spacings_m, radii_m),
        dtype=float,
    )

    # Ensure result is a 1D array for consistency
    if forces.ndim > 1:
        forces = forces.flatten()

    # Attach units to the result array
    result = forces * u.ureg.newton

    # Convert to requested output unit
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(f"Error in converting to {unit}: {e}")

    # Apply precision if specified
    if precision is not None:
        result = np.round(result, precision)

    return result


def weight_force_belt_inside(
    total_weight_force_belt: "Quantity",
    inclination_angle: "Quantity",
    belt_width: "Quantity",
    troughing_angle: "Quantity",
    banking_angle: "Quantity",
    belt_width_on_inside_wing_roll: "Quantity",
    method: str = CONVENTIONAL_METHOD,
    wing_roll_load_factor: Optional["Quantity"] = None,
    unit: str = "newton",
    precision: int = 2,
) -> "Quantity":
    """
    Calculate the weight force component acting on the inside wing roll of a troughed belt.

    This function provides a unit-aware interface for calculating the weight force
    component that acts on the inside wing roll of a troughed belt conveyor in a
    horizontal curve, with comprehensive input validation and unit conversion.

    Parameters
    ----------
    total_weight_force_belt : Quantity
        Total weight force acting on the belt (belt + material)
    inclination_angle : Quantity
        Inclination angle of the belt conveyor
    belt_width : Quantity
        Total width of the belt
    troughing_angle : Quantity
        Troughing angle of the belt
    banking_angle : Quantity
        Banking angle of the belt in the horizontal curve
    belt_width_on_inside_wing_roll : Quantity
        Effective width of the belt supported by the inside wing roll
    method : str, optional
        Calculation methodology:
        - "conventional": Standard method from Grimmer & Kessler (1987) Teil I
        - "improved": Enhanced method from Grimmer & Kessler (1987) Teil II
        Default is "conventional".
    wing_roll_load_factor : Quantity, optional
        Load factor for wing roll. Typical engineering range is 1.0 to 2.0
        for most belt conveyor applications. Values outside this range may
        be used for research or special applications.
        If None and method="improved", defaults to 1.5 * u.dimensionless.
        Ignored for conventional method.
    unit : str, optional
        Output unit for the force. Default is "newton".
    precision : int, optional
        Number of decimal places for the result. Default is 2.

    Returns
    -------
    Quantity
        Weight force component acting on the inside wing roll with specified unit.

    Raises
    ------
    ValueError
        If input parameters are invalid, method is unknown, or unit conversion fails.

    Notes
    -----
    The calculation considers the geometric distribution of weight forces in a troughed
    belt system with banking. All angle inputs are converted to radians internally.

    Available calculation methods:
    1. Conventional Method (method="conventional"):
       - Based on Grimmer & Kessler (1987) Teil I
       - Traditional calculation approaches

    2. Improved Method (method="improved"):
       - Based on Grimmer & Kessler (1987) Teil II
       - Enhanced calculation procedures with improvements to conventional methods

    Physical constraints checked:
    - Total weight force must be non-negative
    - Belt widths must be positive
    - Inside wing roll width must not exceed total belt width
    """
    # Convert inputs to standard units with enhanced error handling
    try:
        total_force_n = total_weight_force_belt.to(u.ureg.newton)
        inclination_rad = inclination_angle.to(u.ureg.radian)
        belt_width_m = belt_width.to(u.ureg.meter)
        troughing_rad = troughing_angle.to(u.ureg.radian)
        banking_rad = banking_angle.to(u.ureg.radian)
        inside_width_m = belt_width_on_inside_wing_roll.to(u.ureg.meter)
    except Exception as e:
        raise ValueError(
            ERROR_MESSAGES["unit_conversion"].format(param="input", error=e)
        )

    # Enhanced physical constraints validation
    if total_force_n.magnitude < 0:
        raise ValueError(
            ERROR_MESSAGES["negative_force"].format(value=total_force_n.magnitude)
        )

    if belt_width_m.magnitude <= 0:
        raise ValueError(
            ERROR_MESSAGES["positive_width"].format(value=belt_width_m.magnitude)
        )

    if inside_width_m.magnitude <= 0:
        raise ValueError(
            ERROR_MESSAGES["positive_width"].format(value=inside_width_m.magnitude)
        )

    if inside_width_m.magnitude > belt_width_m.magnitude:
        raise ValueError(ERROR_MESSAGES["invalid_width"])

    # Method validation
    if method not in VALID_METHODS:
        raise ValueError(
            ERROR_MESSAGES["invalid_method"].format(
                method=method, valid_methods=VALID_METHODS
            )
        )

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.ureg.parse_units(unit)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["invalid_unit"].format(unit=unit, error=e))

    # Load factor handling with defaults for improved method
    if method == IMPROVED_METHOD:
        if wing_roll_load_factor is None:
            wing_roll_load_factor = DEFAULT_WING_LOAD_FACTOR * u.ureg.dimensionless

        # Type narrowing: wing_roll_load_factor is guaranteed to be Quantity here
        assert wing_roll_load_factor is not None
        try:
            load_factor_magnitude = wing_roll_load_factor.to(
                u.ureg.dimensionless
            ).magnitude
        except Exception as e:
            raise ValueError(
                ERROR_MESSAGES["unit_conversion"].format(
                    param="wing_roll_load_factor", error=e
                )
            )

        # Add physical meaningfulness validation
        if load_factor_magnitude < 0:
            raise ValueError(
                "wing_roll_load_factor must be non-negative for physical meaningfulness"
            )

        result_magnitude = _weight_force_belt_inside_improved(
            total_force_n.magnitude,
            inclination_rad.magnitude,
            load_factor_magnitude,
            belt_width_m.magnitude,
            troughing_rad.magnitude,
            banking_rad.magnitude,
            inside_width_m.magnitude,
        )
    else:  # conventional method
        result_magnitude = _weight_force_belt_inside_conventional(
            total_force_n.magnitude,
            inclination_rad.magnitude,
            belt_width_m.magnitude,
            troughing_rad.magnitude,
            banking_rad.magnitude,
            inside_width_m.magnitude,
        )

    # Attach units and convert with enhanced error handling
    result = result_magnitude * u.ureg.newton
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["invalid_unit"].format(unit=unit, error=e))

    # Apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def weight_force_belt_outside(
    total_weight_force_belt: "Quantity",
    inclination_angle: "Quantity",
    belt_width: "Quantity",
    troughing_angle: "Quantity",
    banking_angle: "Quantity",
    belt_width_on_outside_wing_roll: "Quantity",
    method: str = CONVENTIONAL_METHOD,
    wing_roll_load_factor: "Quantity" = None,
    unit: str = "newton",
    precision: int = 2,
) -> "Quantity":
    """
    Calculate the weight force component acting on the outside wing roll of a troughed belt.

    This function provides a complete unit-aware interface for calculating the weight force
    component that acts on the outside wing roll of a troughed belt conveyor in a horizontal
    curve, with comprehensive input validation and unit conversion capabilities.

    Parameters
    ----------
    total_weight_force_belt : Quantity
        Total weight force acting on the belt (belt + material) [force]
    inclination_angle : Quantity
        Inclination angle of the belt conveyor [angle]
    belt_width : Quantity
        Total width of the belt [length]
    troughing_angle : Quantity
        Troughing angle of the belt [angle]
    banking_angle : Quantity
        Banking angle of the belt in the horizontal curve [angle]
    belt_width_on_outside_wing_roll : Quantity
        Effective width of the belt supported by the outside wing roll [length]
    method : str, optional
        Calculation methodology to use:
        - "conventional": Standard method from Grimmer & Kessler (1987) Teil I
        - "improved": Enhanced method from Grimmer & Kessler (1987) Teil II
        Default is "conventional".
    unit : str, optional
        Output unit for the force. Default is "newton".
    precision : int, optional
        Number of decimal places for the result. Default is 2.

    Returns
    -------
    Quantity
        Weight force component acting on the outside wing roll with specified unit.

    Raises
    ------
    ValueError
        If unit conversion fails, parameters are invalid, or belt width constraints are violated.

    Notes
    -----
    The calculation accounts for the geometric distribution of weight forces in a troughed
    belt system with banking. Physical constraints are enforced:
    - All forces must be non-negative
    - Outside belt width cannot exceed total belt width
    - Angles are automatically converted to radians for calculation

    Mathematical formulation:
    F_outside = F_total * cos(α) * (w_outside/w_total) * sin(λ - β) * cos(λ)

    where:
    - F_outside = weight force on outside wing roll
    - F_total = total weight force
    - α = inclination angle
    - w_outside = belt width on outside wing roll
    - w_total = total belt width
    - λ = troughing angle
    - β = banking angle
    """
    # Handle default value for wing_roll_load_factor
    if wing_roll_load_factor is None:
        wing_roll_load_factor = 1 * u.ureg.dimensionless

    try:
        # Convert inputs to standard units
        force_magnitude = total_weight_force_belt.to(u.ureg.newton).magnitude
        inclination_magnitude = inclination_angle.to(u.ureg.radian).magnitude
        width_magnitude = belt_width.to(u.ureg.meter).magnitude
        troughing_magnitude = troughing_angle.to(u.ureg.radian).magnitude
        banking_magnitude = banking_angle.to(u.ureg.radian).magnitude
        outside_width_magnitude = belt_width_on_outside_wing_roll.to(
            u.ureg.meter
        ).magnitude
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Validate inputs
    if force_magnitude < 0:
        raise ValueError("total_weight_force_belt must be non-negative")

    if width_magnitude <= 0:
        raise ValueError("belt_width must be positive")

    if outside_width_magnitude < 0:
        raise ValueError("belt_width_on_outside_wing_roll must be non-negative")

    if outside_width_magnitude > width_magnitude:
        raise ValueError(
            "belt_width_on_outside_wing_roll cannot exceed total belt width"
        )

    # Validate output unit
    try:
        pint_unit = u.ureg.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Method validation
    if method not in VALID_METHODS:
        raise ValueError(
            f"Unknown method: '{method}'. Valid options are: {VALID_METHODS}"
        )

    # Load factor handling with defaults for improved method
    if method == IMPROVED_METHOD:
        if wing_roll_load_factor is None:
            wing_roll_load_factor = DEFAULT_WING_LOAD_FACTOR * u.ureg.dimensionless

        # Type narrowing: wing_roll_load_factor is guaranteed to be Quantity here
        assert wing_roll_load_factor is not None
        try:
            load_factor_magnitude = wing_roll_load_factor.to(
                u.ureg.dimensionless
            ).magnitude
        except Exception as e:
            raise ValueError(
                ERROR_MESSAGES["unit_conversion"].format(
                    param="wing_roll_load_factor", error=e
                )
            )

        # Add physical meaningfulness validation
        if load_factor_magnitude < 0:
            raise ValueError(
                "wing_roll_load_factor must be non-negative for physical meaningfulness"
            )

    # Calculate using private function based on method
    if method == CONVENTIONAL_METHOD:
        result_magnitude = _weight_force_belt_outside_conventional(
            force_magnitude,
            inclination_magnitude,
            width_magnitude,
            troughing_magnitude,
            banking_magnitude,
            outside_width_magnitude,
        )
    elif method == IMPROVED_METHOD:
        result_magnitude = _weight_force_belt_outside_improved(
            force_magnitude,
            inclination_magnitude,
            load_factor_magnitude,
            width_magnitude,
            troughing_magnitude,
            banking_magnitude,
            outside_width_magnitude,
        )

    # Attach units and convert with enhanced error handling
    result = result_magnitude * u.ureg.newton
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["invalid_unit"].format(unit=unit, error=e))

    # Apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def weight_force_belt_center(
    total_weight_force_belt: "Quantity",
    inclination_angle: "Quantity",
    belt_width: "Quantity",
    banking_angle: "Quantity",
    belt_width_on_center_section: "Quantity",
    method: str = CONVENTIONAL_METHOD,
    center_roll_load_factor: "Quantity" = None,
    unit: str = "newton",
    precision: int = 2,
) -> "Quantity":
    """
    Calculate the weight force component acting on the center section of a troughed belt.

    This function provides a complete unit-aware interface for calculating the weight force
    component that acts on the center section of a troughed belt conveyor in a horizontal
    curve, with comprehensive input validation and unit conversion capabilities.

    Parameters
    ----------
    total_weight_force_belt : Quantity
        Total weight force acting on the belt (belt + material) [force]
    inclination_angle : Quantity
        Inclination angle of the belt conveyor [angle]
    belt_width : Quantity
        Total width of the belt [length]
    banking_angle : Quantity
        Banking angle of the belt in the horizontal curve [angle]
    belt_width_on_center_section : Quantity
        Effective width of the belt supported by the center section [length]
    method : str, optional
        Calculation methodology to use:
        - "conventional": Standard method from Grimmer & Kessler (1987) Teil I
        - "improved": Enhanced method from Grimmer & Kessler (1987) Teil II
        Default is "conventional".
    unit : str, optional
        Output unit for the force. Default is "newton".
    precision : int, optional
        Number of decimal places for the result. Default is 2.

    Returns
    -------
    Quantity
        Weight force component acting on the center section with specified unit.

    Raises
    ------
    ValueError
        If unit conversion fails, parameters are invalid, or belt width constraints are violated.

    Notes
    -----
    The calculation accounts for the weight force distribution in the center section of
    a troughed belt system with banking. Physical constraints are enforced:
    - All forces must be non-negative
    - Center belt width cannot exceed total belt width
    - Angles are automatically converted to radians for calculation

    Mathematical formulation:
    F_center = F_total * cos(α) * (w_center/w_total) * sin(β)

    where:
    - F_center = weight force on center section
    - F_total = total weight force
    - α = inclination angle
    - w_center = belt width on center section
    - w_total = total belt width
    - β = banking angle
    """
    # Handle default value for center_roll_load_factor
    if center_roll_load_factor is None:
        center_roll_load_factor = 1 * u.ureg.dimensionless

    try:
        # Convert inputs to standard units
        force_magnitude = total_weight_force_belt.to(u.ureg.newton).magnitude
        inclination_magnitude = inclination_angle.to(u.ureg.radian).magnitude
        width_magnitude = belt_width.to(u.ureg.meter).magnitude
        banking_magnitude = banking_angle.to(u.ureg.radian).magnitude
        center_width_magnitude = belt_width_on_center_section.to(u.ureg.meter).magnitude
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Validate inputs
    if force_magnitude < 0:
        raise ValueError("total_weight_force_belt must be non-negative")

    if width_magnitude <= 0:
        raise ValueError("belt_width must be positive")

    if center_width_magnitude < 0:
        raise ValueError("belt_width_on_center_section must be non-negative")

    if center_width_magnitude > width_magnitude:
        raise ValueError("belt_width_on_center_section cannot exceed total belt width")

    # Validate output unit
    try:
        pint_unit = u.ureg.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Method validation
    if method not in VALID_METHODS:
        raise ValueError(
            f"Unknown method: '{method}'. Valid options are: {VALID_METHODS}"
        )

    # Load factor handling with defaults for improved method
    if method == IMPROVED_METHOD:
        if center_roll_load_factor is None:
            center_roll_load_factor = DEFAULT_CENTER_LOAD_FACTOR * u.ureg.dimensionless

        # Type narrowing: center_roll_load_factor is guaranteed to be Quantity here
        assert center_roll_load_factor is not None
        try:
            load_factor_magnitude = center_roll_load_factor.to(
                u.ureg.dimensionless
            ).magnitude
        except Exception as e:
            raise ValueError(
                ERROR_MESSAGES["unit_conversion"].format(
                    param="center_roll_load_factor", error=e
                )
            )

        # Add physical meaningfulness validation
        if load_factor_magnitude < 0:
            raise ValueError(
                "center_roll_load_factor must be non-negative for physical meaningfulness"
            )

    # Calculate using private function based on method
    if method == CONVENTIONAL_METHOD:
        result_magnitude = _weight_force_belt_center_conventional(
            force_magnitude,
            inclination_magnitude,
            width_magnitude,
            banking_magnitude,
            center_width_magnitude,
        )
    elif method == IMPROVED_METHOD:
        result_magnitude = _weight_force_belt_center_improved(
            force_magnitude,
            inclination_magnitude,
            load_factor_magnitude,
            width_magnitude,
            banking_magnitude,
            center_width_magnitude,
        )

    # Attach units and convert with enhanced error handling
    result = result_magnitude * u.ureg.newton
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["invalid_unit"].format(unit=unit, error=e))

    # Apply precision if specified
    if precision is not None:
        result = np.round(result, precision)

    return result


def weight_force_of_belt(
    weight_force_belt_inside: "Quantity",
    weight_force_belt_center: "Quantity",
    weight_force_belt_outside: "Quantity",
    method: str = CONVENTIONAL_METHOD,
    unit: str = "newton",
    precision: int = 2,
) -> "Quantity":
    """
    Calculate the net lateral weight force acting on the belt in a horizontal curve.

    This function combines the weight force components from the inside wing roll,
    center section, and outside wing roll to determine the net lateral force
    acting on the belt due to banking and troughing effects in a horizontal curve.

    Parameters
    ----------
    weight_force_belt_inside : Quantity
        Weight force component on the inside wing roll [force units]
    weight_force_belt_center : Quantity
        Weight force component in the center section [force units]
    weight_force_belt_outside : Quantity
        Weight force component on the outside wing roll [force units]
    method : str, optional
        Calculation methodology to use:
        - "conventional": Standard method from Grimmer & Kessler (1987) Teil I
        - "improved": Enhanced method from Grimmer & Kessler (1987) Teil II
        Default is "conventional".
    unit : str, optional
        Output unit for the result (default: "newton")
    precision : int, optional
        Number of decimal places for rounding (default: 2)

    Returns
    -------
    Quantity
        Net lateral weight force acting on the belt [force units]

    Raises
    ------
    ValueError
        If input dimensions are incorrect or units are invalid

    Notes
    -----
    The calculation follows the sign convention where:
    - Inside and center forces contribute positively (toward curve center)
    - Outside force contributes negatively (away from curve center)

    Mathematical formulation:
    F_net = F_inside + F_center - F_outside

    This represents the net lateral force that must be balanced by the
    belt's resistance to lateral movement in the horizontal curve.

    Examples
    --------
    >>> import eytelwein.main.units as u
    >>> inside_force = u.ureg.Quantity(30.04, u.ureg.newton)
    >>> center_force = u.ureg.Quantity(1.572, u.ureg.newton)
    >>> outside_force = u.ureg.Quantity(27.93, u.ureg.newton)
    >>> net_force = weight_force_of_belt(inside_force, center_force, outside_force)
    >>> print(f"{net_force:.2f}")
    3.68 newton
    """
    try:
        # Convert inputs to standard units
        inside_magnitude = weight_force_belt_inside.to(u.ureg.newton).magnitude
        center_magnitude = weight_force_belt_center.to(u.ureg.newton).magnitude
        outside_magnitude = weight_force_belt_outside.to(u.ureg.newton).magnitude
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Validate output unit
    try:
        pint_unit = u.ureg.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Method validation
    if method not in VALID_METHODS:
        raise ValueError(
            f"Unknown method: '{method}'. Valid options are: {VALID_METHODS}"
        )

    # Calculate using private function based on method
    if method == CONVENTIONAL_METHOD:
        result_magnitude = _weight_force_of_belt_conventional(
            inside_magnitude,
            center_magnitude,
            outside_magnitude,
        )
    elif method == IMPROVED_METHOD:
        result_magnitude = _weight_force_of_belt_improved(
            inside_magnitude,
            center_magnitude,
            outside_magnitude,
        )

    # Attach units and convert
    result = result_magnitude * u.ureg.newton
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(f"Error in converting to {unit}: {e}")

    # Apply precision
    if precision is not None:
        result = np.round(result, precision)

    return result


def weight_force_material_inside(
    normal_force: "Quantity",
    troughing_angle: "Quantity",
    banking_angle: "Quantity",
    method: str = CONVENTIONAL_METHOD,
    unit: str = "newton",
    precision: int = 2,
) -> "Quantity":
    """
    Calculate the weight force component from material acting on the inside wing roll.

    This function provides a unit-aware interface for calculating the weight force
    component that acts on the inside wing roll due to conveyed material in a
    troughed belt conveyor horizontal curve, with comprehensive input validation.

    Parameters
    ----------
    normal_force : Quantity
        Normal force acting on the inside wing roll from the conveyed material
    troughing_angle : Quantity
        Troughing angle of the belt
    banking_angle : Quantity
        Banking angle of the belt in the horizontal curve
    method : str, optional
        Calculation methodology. Currently supports:
        - "conventional": Standard method from Grimmer & Kessler (1987) Teil I
        - "improved": Enhanced method from Grimmer & Kessler (1987) Teil II
        Default is "conventional".
    unit : str, optional
        Output unit for the force. Default is "newton".
    precision : int, optional
        Number of decimal places for the result. Default is 2.

    Returns
    -------
    Quantity
        Weight force component from material acting on the inside wing roll with specified unit.

    Raises
    ------
    ValueError
        If input parameters are invalid, method is unknown, or unit conversion fails.

    Notes
    -----
    The calculation determines the lateral force component that results from the
    material weight acting on the inclined inside wing roll of a troughed belt
    conveyor in a horizontal curve.

    Mathematical formulation:
    - Conventional method: F_inside = F_normal * tan(λ + β) * cos(λ)
    - Improved method: F_inside = F_normal * tan(λ + β)

    Where:
    - F_normal: Normal force from material on inside wing roll
    - λ: Troughing angle
    - β: Banking angle

    The key difference between methods is that the improved method removes the
    cos(λ) factor present in the conventional method, providing enhanced accuracy
    based on refined geometric considerations.

    Examples
    --------
    >>> import eytelwein.main.units as u
    >>> from eytelwein.horizontal_curves import weight_force_material_inside
    >>>
    >>> result = weight_force_material_inside(
    ...     normal_force=1000.0 * u.ureg.newton,
    ...     troughing_angle=30.0 * u.ureg.degree,
    ...     banking_angle=5.0 * u.ureg.degree,
    ...     method="conventional"
    ... )
    >>> print(f"Weight force: {result:.2f}")
    Weight force: 606.40 newton

    References
    ----------
    Grimmer, K.-J. und F. Kessler: Teil I - Traditional calculation approaches.
    Grimmer, K.-J. und F. Kessler: Teil II - Enhanced calculation procedures.
    """
    # Convert inputs to standard units with enhanced error handling
    try:
        normal_force_n = normal_force.to(u.ureg.newton)
        troughing_rad = troughing_angle.to(u.ureg.radian)
        banking_rad = banking_angle.to(u.ureg.radian)
    except Exception as e:
        raise ValueError(
            ERROR_MESSAGES["unit_conversion"].format(param="input", error=e)
        )

    # Enhanced physical constraints validation
    if normal_force_n.magnitude < 0:
        raise ValueError(
            ERROR_MESSAGES["negative_force"].format(value=normal_force_n.magnitude)
        )

    # Method validation
    if method not in VALID_METHODS:
        raise ValueError(
            ERROR_MESSAGES["invalid_method"].format(
                method=method, valid_methods=VALID_METHODS
            )
        )

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.ureg.parse_units(unit)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["invalid_unit"].format(unit=unit, error=e))

    # Calculate using the appropriate private implementation
    if method == CONVENTIONAL_METHOD:
        result_magnitude = _weight_force_material_inside_conventional(
            normal_force_n.magnitude,
            troughing_rad.magnitude,
            banking_rad.magnitude,
        )
    elif method == IMPROVED_METHOD:
        result_magnitude = _weight_force_material_inside_improved(
            normal_force_n.magnitude,
            troughing_rad.magnitude,
            banking_rad.magnitude,
        )

    # Attach units and convert with enhanced error handling
    result = result_magnitude * u.ureg.newton
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["invalid_unit"].format(unit=unit, error=e))

    # Apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def weight_force_material_outside(
    normal_force: "Quantity",
    troughing_angle: "Quantity",
    banking_angle: "Quantity",
    method: str = CONVENTIONAL_METHOD,
    unit: str = "newton",
    precision: int = 2,
) -> "Quantity":
    """
    Calculate the weight force component from material acting on the outside wing roll.

    This function provides a unit-aware interface for calculating the weight force
    component that acts on the outside wing roll due to conveyed material in a
    troughed belt conveyor horizontal curve, with comprehensive input validation.

    Parameters
    ----------
    normal_force : Quantity
        Normal force acting on the outside wing roll from the conveyed material
    troughing_angle : Quantity
        Troughing angle of the belt
    banking_angle : Quantity
        Banking angle of the belt in the horizontal curve
    method : str, optional
        Calculation methodology. Currently supports:
        - "conventional": Standard method from Grimmer & Kessler (1987) Teil I
        - "improved": Enhanced method from Grimmer & Kessler (1987) Teil II
        Default is "conventional".
    unit : str, optional
        Output unit for the force. Default is "newton".
    precision : int, optional
        Number of decimal places for the result. Default is 2.

    Returns
    -------
    Quantity
        Weight force component from material acting on the outside wing roll with specified unit.

    Raises
    ------
    ValueError
        If input parameters are invalid, method is unknown, or unit conversion fails.

    Notes
    -----
    The calculation determines the lateral force component that results from the
    material weight acting on the inclined outside wing roll of a troughed belt
    conveyor in a horizontal curve.

    Mathematical formulation:
    - Conventional method: F_outside = F_normal * tan(λ - β) * cos(λ)
    - Improved method: F_outside = F_normal * tan(λ - β)

    Where:
    - F_normal: Normal force from material on outside wing roll
    - λ: Troughing angle
    - β: Banking angle

    The key difference from the inside wing roll is the subtraction of banking angle
    (λ - β) instead of addition (λ + β), reflecting the opposite geometry effect.

    The improved method removes the cos(λ) factor present in the conventional method,
    providing enhanced accuracy based on refined geometric considerations.

    Examples
    --------
    >>> import eytelwein.main.units as u
    >>> from eytelwein.horizontal_curves import weight_force_material_outside
    >>>
    >>> result = weight_force_material_outside(
    ...     normal_force=1000.0 * u.ureg.newton,
    ...     troughing_angle=30.0 * u.ureg.degree,
    ...     banking_angle=5.0 * u.ureg.degree,
    ...     method="conventional"
    ... )
    >>> print(f"Weight force: {result:.2f}")
    Weight force: 403.83 newton

    References
    ----------
    Grimmer, K.-J. und F. Kessler: Teil I - Traditional calculation approaches.
    Grimmer, K.-J. und F. Kessler: Teil II - Enhanced calculation procedures.
    """
    # Convert inputs to standard units with enhanced error handling
    try:
        normal_force_n = normal_force.to(u.ureg.newton)
        troughing_rad = troughing_angle.to(u.ureg.radian)
        banking_rad = banking_angle.to(u.ureg.radian)
    except Exception as e:
        raise ValueError(
            ERROR_MESSAGES["unit_conversion"].format(param="input", error=e)
        )

    # Enhanced physical constraints validation
    if normal_force_n.magnitude < 0:
        raise ValueError(
            ERROR_MESSAGES["negative_force"].format(value=normal_force_n.magnitude)
        )

    # Method validation
    if method not in VALID_METHODS:
        raise ValueError(
            ERROR_MESSAGES["invalid_method"].format(
                method=method, valid_methods=VALID_METHODS
            )
        )

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.ureg.parse_units(unit)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["invalid_unit"].format(unit=unit, error=e))

    # Calculate using the appropriate private implementation
    if method == CONVENTIONAL_METHOD:
        result_magnitude = _weight_force_material_outside_conventional(
            normal_force_n.magnitude,
            troughing_rad.magnitude,
            banking_rad.magnitude,
        )
    elif method == IMPROVED_METHOD:
        result_magnitude = _weight_force_material_outside_improved(
            normal_force_n.magnitude,
            troughing_rad.magnitude,
            banking_rad.magnitude,
        )

    # Attach units and convert with enhanced error handling
    result = result_magnitude * u.ureg.newton
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["invalid_unit"].format(unit=unit, error=e))

    # Apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def weight_force_material_center(
    normal_force: "Quantity",
    banking_angle: "Quantity",
    method: str = CONVENTIONAL_METHOD,
    unit: str = "newton",
    precision: int = 2,
) -> "Quantity":
    """
    Calculate the weight force component from material acting on the center section.

    This function provides a unit-aware interface for calculating the weight force
    component that acts on the center section due to conveyed material in a
    troughed belt conveyor horizontal curve, with comprehensive input validation.

    Parameters
    ----------
    normal_force : Quantity
        Normal force acting on the center section from the conveyed material
    banking_angle : Quantity
        Banking angle of the belt in the horizontal curve
    method : str, optional
        Calculation methodology. Currently supports:
        - "conventional": Standard method from Grimmer & Kessler (1987) Teil I
        - "improved": Enhanced method from Grimmer & Kessler (1987) Teil II
        Default is "conventional".
    unit : str, optional
        Output unit for the force. Default is "newton".
    precision : int, optional
        Number of decimal places for the result. Default is 2.

    Returns
    -------
    Quantity
        Weight force component from material acting on the center section with specified unit.

    Raises
    ------
    ValueError
        If input parameters are invalid, method is unknown, or unit conversion fails.

    Notes
    -----
    The calculation determines the lateral force component that results from the
    material weight acting on the center section of a troughed belt conveyor
    in a horizontal curve. The center section is only affected by banking angle,
    not troughing angle, since it remains horizontal.

    Mathematical formulation for both methods:
    F_center = F_normal * tan(β)

    Where:
    - F_normal: Normal force from material on center section
    - β: Banking angle

    The center section calculation is simpler than wing roll calculations because
    it's not influenced by troughing geometry - only by the banking of the entire
    belt cross-section. Both conventional and improved methods use the same formula
    for the center section since geometric considerations remain unchanged.

    Examples
    --------
    >>> import eytelwein.main.units as u
    >>> from eytelwein.horizontal_curves import weight_force_material_center
    >>>
    >>> result = weight_force_material_center(
    ...     normal_force=1000.0 * u.ureg.newton,
    ...     banking_angle=5.0 * u.ureg.degree,
    ...     method="conventional"
    ... )
    >>> print(f"Weight force: {result:.2f}")
    Weight force: 87.49 newton

    References
    ----------
    Grimmer, K.-J. und F. Kessler: Teil I - Traditional calculation approaches.
    Grimmer, K.-J. und F. Kessler: Teil II - Enhanced calculation procedures.
    """
    # Convert inputs to standard units with enhanced error handling
    try:
        normal_force_n = normal_force.to(u.ureg.newton)
        banking_rad = banking_angle.to(u.ureg.radian)
    except Exception as e:
        raise ValueError(
            ERROR_MESSAGES["unit_conversion"].format(param="input", error=e)
        )

    # Enhanced physical constraints validation
    if normal_force_n.magnitude < 0:
        raise ValueError(
            ERROR_MESSAGES["negative_force"].format(value=normal_force_n.magnitude)
        )

    # Method validation
    if method not in VALID_METHODS:
        raise ValueError(
            ERROR_MESSAGES["invalid_method"].format(
                method=method, valid_methods=VALID_METHODS
            )
        )

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.ureg.parse_units(unit)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["invalid_unit"].format(unit=unit, error=e))

    # Calculate using the appropriate private implementation
    if method == CONVENTIONAL_METHOD:
        result_magnitude = _weight_force_material_center_conventional(
            normal_force_n.magnitude,
            banking_rad.magnitude,
        )
    elif method == IMPROVED_METHOD:
        result_magnitude = _weight_force_material_center_improved(
            normal_force_n.magnitude,
            banking_rad.magnitude,
        )

    # Attach units and convert with enhanced error handling
    result = result_magnitude * u.ureg.newton
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["invalid_unit"].format(unit=unit, error=e))

    # Apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def weight_force_of_material(
    inside_force: "Quantity",
    center_force: "Quantity",
    outside_force: "Quantity",
    method: str = CONVENTIONAL_METHOD,
    unit: str = "newton",
    precision: int = 2,
) -> "Quantity":
    """
    Calculate the net lateral weight force acting on conveyed material in horizontal curves.

    This function provides a unit-aware interface for combining the weight force
    components from inside wing roll, center section, and outside wing roll to
    determine the resultant lateral force acting on conveyed material in a
    troughed belt conveyor horizontal curve.

    Parameters
    ----------
    inside_force : Quantity
        Weight force component from material acting on the inside wing roll
    center_force : Quantity
        Weight force component from material acting in the center section
    outside_force : Quantity
        Weight force component from material acting on the outside wing roll
    method : str, optional
        Calculation methodology. Currently supports:
        - "conventional": Standard method from Grimmer & Kessler (1987) Teil I
        - "improved": Enhanced method from Grimmer & Kessler (1987) Teil II
        Default is "conventional".
    unit : str, optional
        Output unit for the force. Default is "newton".
    precision : int, optional
        Number of decimal places for the result. Default is 2.

    Returns
    -------
    Quantity
        Net lateral weight force acting on conveyed material with specified unit.

    Raises
    ------
    ValueError
        If input parameters are invalid, method is unknown, or unit conversion fails.

    Notes
    -----
    The calculation combines the three weight force components using the standard
    force balance methodology for horizontal curve analysis. The net lateral force
    represents the resultant effect of material weight distribution on belt behavior
    in horizontal curves.

    Mathematical formulation:
    F_net = F_inside + F_center - F_outside

    Where:
    - F_inside: Weight force component on inside wing roll
    - F_center: Weight force component in center section
    - F_outside: Weight force component on outside wing roll

    The subtraction of the outside component reflects the opposing nature of forces
    in horizontal curves, where inside and center forces work together while the
    outside force opposes the resultant lateral movement toward the curve center.

    Physical interpretation:
    - Positive result: Net force toward inside of curve
    - Negative result: Net force toward outside of curve
    - Zero result: Balanced forces, no net lateral effect

    Examples
    --------
    >>> import eytelwein.main.units as u
    >>> from eytelwein.horizontal_curves import weight_force_of_material
    >>>
    >>> result = weight_force_of_material(
    ...     inside_force=530.29 * u.ureg.newton,
    ...     center_force=87.49 * u.ureg.newton,
    ...     outside_force=433.01 * u.ureg.newton,
    ...     method="conventional"
    ... )
    >>> print(f"Net material weight force: {result:.2f}")
    Net material weight force: 184.77 newton

    References
    ----------
    Grimmer, K.-J. und F. Kessler: Teil I - Traditional calculation approaches.
    Grimmer, K.-J. und F. Kessler: Teil II - Enhanced calculation procedures.
    """
    # Convert inputs to standard units with enhanced error handling
    try:
        inside_force_n = inside_force.to(u.ureg.newton)
        center_force_n = center_force.to(u.ureg.newton)
        outside_force_n = outside_force.to(u.ureg.newton)
    except Exception as e:
        raise ValueError(
            ERROR_MESSAGES["unit_conversion"].format(param="input", error=e)
        )

    # Method validation
    if method not in VALID_METHODS:
        raise ValueError(
            ERROR_MESSAGES["invalid_method"].format(
                method=method, valid_methods=VALID_METHODS
            )
        )

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.ureg.parse_units(unit)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["invalid_unit"].format(unit=unit, error=e))

    # Calculate using the appropriate private implementation
    if method == CONVENTIONAL_METHOD:
        result_magnitude = _weight_force_of_material_conventional(
            inside_force_n.magnitude,
            center_force_n.magnitude,
            outside_force_n.magnitude,
        )
    elif method == IMPROVED_METHOD:
        # Note: Both methods use the same combination formula
        # The difference is in how the individual components are calculated
        result_magnitude = _weight_force_of_material_improved(
            inside_force_n.magnitude,
            center_force_n.magnitude,
            outside_force_n.magnitude,
        )

    # Attach units and convert with enhanced error handling
    result = result_magnitude * u.ureg.newton
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["invalid_unit"].format(unit=unit, error=e))

    # Apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def restraining_force_from_dead_weights(
    total_force_from_belt: "Quantity",
    total_force_from_material: "Quantity",
    method: str = CONVENTIONAL_METHOD,
    unit: str = "newton",
    precision: int = 2,
) -> "Quantity":
    """
    Calculate the total restraining force from dead weights acting toward the outside curve.

    This function provides a unit-aware interface for calculating the combined restraining
    force that acts toward the outside of horizontal curves due to the dead weights of
    the belt and conveyed material. This force opposes the centripetal force required
    for the belt to follow the curved path and must be balanced by appropriate belt
    tension and guiding forces.

    Parameters
    ----------
    total_force_from_belt : Quantity
        Total lateral force component from belt weight acting toward outside curve
    total_force_from_material : Quantity
        Total lateral force component from material weight acting toward outside curve
    method : str, optional
        Calculation methodology. Currently supports:
        - "conventional": Standard method from Grimmer & Kessler (1987) Teil I
        - "improved": Enhanced method from Grimmer & Kessler (1987) Teil II
        Default is "conventional".
    unit : str, optional
        Output unit for the force. Default is "newton".
    precision : int, optional
        Number of decimal places for the result. Default is 2.

    Returns
    -------
    Quantity
        Total restraining force from dead weights acting toward outside curve with specified unit.

    Raises
    ------
    ValueError
        If input parameters are invalid, method is unknown, or unit conversion fails.

    Notes
    -----
    The calculation combines the lateral force components from belt and material weights
    that act toward the outside of horizontal curves. These forces arise from the natural
    tendency of dead weights to move radially outward in curved paths due to inertia.

    Mathematical formulation:
    F_restraining = F_belt + F_material

    Where:
    - F_belt: Total lateral force from belt weight toward outside curve
    - F_material: Total lateral force from material weight toward outside curve

    Physical interpretation:
    - This force represents the total centrifugal effect of dead weights
    - Must be balanced by belt tension and guiding forces for stable operation
    - Positive values indicate force magnitude toward outside curve
    - Critical for determining required belt tension and curve radius limits

    The restraining force is fundamental to horizontal curve design as it determines:
    1. Minimum required belt tension to maintain belt path
    2. Maximum allowable curve radius for given operating conditions
    3. Guiding force requirements for stable belt tracking

    Examples
    --------
    >>> import eytelwein.main.units as u
    >>> from eytelwein.horizontal_curves import restraining_force_from_dead_weights
    >>>
    >>> result = restraining_force_from_dead_weights(
    ...     total_force_from_belt=450.25 * u.ureg.newton,
    ...     total_force_from_material=184.77 * u.ureg.newton,
    ...     method="conventional"
    ... )
    >>> print(f"Total restraining force: {result:.2f}")
    Total restraining force: 635.02 newton

    References
    ----------
    Grimmer, K.-J. und F. Kessler: Teil I - Traditional calculation approaches.
    Grimmer, K.-J. und F. Kessler: Teil II - Enhanced calculation procedures.
    """
    # Convert inputs to standard units with enhanced error handling
    try:
        belt_force_n = total_force_from_belt.to(u.ureg.newton)
        material_force_n = total_force_from_material.to(u.ureg.newton)
    except Exception as e:
        raise ValueError(
            ERROR_MESSAGES["unit_conversion"].format(param="input", error=e)
        )

    # Enhanced physical constraints validation
    if belt_force_n.magnitude < 0:
        raise ValueError(
            ERROR_MESSAGES["negative_force"].format(value=belt_force_n.magnitude)
        )

    if material_force_n.magnitude < 0:
        raise ValueError(
            ERROR_MESSAGES["negative_force"].format(value=material_force_n.magnitude)
        )

    # Method validation
    if method not in VALID_METHODS:
        raise ValueError(
            ERROR_MESSAGES["invalid_method"].format(
                method=method, valid_methods=VALID_METHODS
            )
        )

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.ureg.parse_units(unit)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["invalid_unit"].format(unit=unit, error=e))

    # Calculate using the appropriate private implementation
    if method == CONVENTIONAL_METHOD:
        result_magnitude = (
            _restraining_force_from_dead_weights_towards_outside_curve_conventional(
                belt_force_n.magnitude,
                material_force_n.magnitude,
            )
        )
    elif method == IMPROVED_METHOD:
        # Note: Both methods use the same combination formula
        # The difference is in how the individual components are calculated
        result_magnitude = (
            _restraining_force_from_dead_weights_towards_outside_curve_conventional(
                belt_force_n.magnitude,
                material_force_n.magnitude,
            )
        )

    # Attach units and convert with enhanced error handling
    result = result_magnitude * u.ureg.newton
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["invalid_unit"].format(unit=unit, error=e))

    # Apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def tilted_idler_friction_force_inside(
    total_weight_force_material: "Quantity",
    inclination_angle: "Quantity",
    belt_width: "Quantity",
    troughing_angle: "Quantity",
    banking_angle: "Quantity",
    belt_width_on_inside_wing_roll: "Quantity",
    friction_variation: "Quantity",
    friction_coefficient_tilted_idler: "Quantity",
    normal_force_on_idler_roll: "Quantity",
    wing_roll_load_factor: Optional["Quantity"] = None,
    method: str = CONVENTIONAL_METHOD,
    unit: str = "newton",
    precision: int = 2,
) -> "Quantity":
    """
    Calculate the friction force from conveyed material acting on tilted idlers at the inside wing roll.

    This function provides a unit-aware interface for calculating the friction force
    component that results from conveyed material acting on tilted idlers positioned
    at the inside wing roll of a troughed belt conveyor operating in a horizontal curve.

    Parameters
    ----------
    total_weight_force_material : Quantity
        Total weight force of the conveyed material
    inclination_angle : Quantity
        Inclination angle of the belt conveyor
    belt_width : Quantity
        Total width of the belt
    troughing_angle : Quantity
        Troughing angle of the belt
    banking_angle : Quantity
        Banking angle of the belt in the horizontal curve
    belt_width_on_inside_wing_roll : Quantity
        Effective width of the belt supported by the inside wing roll
    friction_variation : Quantity
        Friction variation factor (dimensionless)
    friction_coefficient_tilted_idler : Quantity
        Friction coefficient for material-idler interaction (dimensionless)
    normal_force_on_idler_roll : Quantity
        Additional normal force acting on the idler roll
    wing_roll_load_factor : Quantity, optional
        Load factor for enhanced calculation accuracy in improved method.
        Default is 1.1 if not provided.
    method : str, optional
        Calculation method to use. Either "conventional" or "improved".
        Default is "conventional".
    unit : str, optional
        Output unit for the force. Default is "newton".
    precision : int, optional
        Number of decimal places for the result. Default is 2.

    Returns
    -------
    Quantity
        Friction force component from material on inside wing roll tilted idlers.

    Raises
    ------
    ValueError
        If input parameters are invalid or unit conversion fails.

    Notes
    -----
    This calculation considers the interaction between conveyed material and tilted
    idlers in the inside wing roll position of a troughed belt conveyor system
    operating in horizontal curves.

    The friction force arises from the normal force of material on the tilted idlers
    combined with geometric factors including troughing angle, banking angle, and
    belt width distribution.

    Physical constraints checked:
    - All force inputs must be non-negative
    - Belt widths must be positive
    - Inside wing roll width must not exceed total belt width
    - Friction coefficients must be non-negative

    Examples
    --------
    >>> import eytelwein.main.units as u
    >>> from eytelwein.horizontal_curves import tilted_idler_friction_force_inside
    >>> force = tilted_idler_friction_force_inside(
    ...     total_weight_force_material=156.71 * u.ureg.newton,
    ...     inclination_angle=0 * u.ureg.degree,
    ...     belt_width=0.8 * u.ureg.meter,
    ...     troughing_angle=30 * u.ureg.degree,
    ...     banking_angle=1.46 * u.ureg.degree,
    ...     belt_width_on_inside_wing_roll=0.3025 * u.ureg.meter,
    ...     friction_variation=0.7 * u.ureg.dimensionless,
    ...     friction_coefficient_tilted_idler=0.416183 * u.ureg.dimensionless,
    ...     normal_force_on_idler_roll=0 * u.ureg.newton
    ... )
    >>> print(f"Friction force: {force:.2f}")
    Friction force: 12.75 newton
    """
    # Convert inputs to standard units with enhanced error handling
    try:
        total_force_n = total_weight_force_material.to(u.ureg.newton)
        inclination_rad = inclination_angle.to(u.ureg.radian)
        belt_width_m = belt_width.to(u.ureg.meter)
        troughing_rad = troughing_angle.to(u.ureg.radian)
        banking_rad = banking_angle.to(u.ureg.radian)
        inside_width_m = belt_width_on_inside_wing_roll.to(u.ureg.meter)
        friction_var = friction_variation.to(u.ureg.dimensionless)
        friction_coeff = friction_coefficient_tilted_idler.to(u.ureg.dimensionless)
        normal_force_n = normal_force_on_idler_roll.to(u.ureg.newton)
    except Exception as e:
        raise ValueError(
            ERROR_MESSAGES["unit_conversion"].format(param="input", error=e)
        )

    # Handle default wing_roll_load_factor for improved method
    if wing_roll_load_factor is None:
        wing_roll_load_factor = DEFAULT_WING_LOAD_FACTOR * u.ureg.dimensionless

    # Type narrowing: wing_roll_load_factor is guaranteed to be Quantity here
    assert wing_roll_load_factor is not None
    try:
        load_factor_magnitude = wing_roll_load_factor.to(u.ureg.dimensionless).magnitude
    except Exception as e:
        raise ValueError(
            ERROR_MESSAGES["unit_conversion"].format(
                param="wing_roll_load_factor", error=e
            )
        )

    if load_factor_magnitude < 0:
        raise ValueError(
            "wing_roll_load_factor must be non-negative for physical meaningfulness"
        )

    # Enhanced physical constraints validation
    if total_force_n.magnitude < 0:
        raise ValueError(
            ERROR_MESSAGES["negative_force"].format(value=total_force_n.magnitude)
        )

    if normal_force_n.magnitude < 0:
        raise ValueError(
            f"Normal force must be non-negative, got {normal_force_n.magnitude}"
        )

    if belt_width_m.magnitude <= 0:
        raise ValueError(
            ERROR_MESSAGES["positive_width"].format(value=belt_width_m.magnitude)
        )

    if inside_width_m.magnitude <= 0:
        raise ValueError(
            ERROR_MESSAGES["positive_width"].format(value=inside_width_m.magnitude)
        )

    if inside_width_m.magnitude > belt_width_m.magnitude:
        raise ValueError(ERROR_MESSAGES["invalid_width"])

    if friction_var.magnitude < 0:
        raise ValueError(
            f"Friction variation must be non-negative, got {friction_var.magnitude}"
        )

    if friction_coeff.magnitude < 0:
        raise ValueError(
            f"Friction coefficient must be non-negative, got {friction_coeff.magnitude}"
        )

    # Validate method parameter
    if method not in VALID_METHODS:
        raise ValueError(
            ERROR_MESSAGES["invalid_method"].format(
                method=method, valid_methods=VALID_METHODS
            )
        )

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.ureg.parse_units(unit)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["invalid_unit"].format(unit=unit, error=e))

    # Call the appropriate private implementation based on method
    if method == CONVENTIONAL_METHOD:
        result_magnitude = _tilted_idler_friction_force_inside_conventional(
            total_force_n.magnitude,
            inclination_rad.magnitude,
            belt_width_m.magnitude,
            troughing_rad.magnitude,
            banking_rad.magnitude,
            inside_width_m.magnitude,
            friction_var.magnitude,
            friction_coeff.magnitude,
            normal_force_n.magnitude,
        )
    elif method == IMPROVED_METHOD:
        result_magnitude = _tilted_idler_friction_force_inside_improved(
            total_force_n.magnitude,
            inclination_rad.magnitude,
            load_factor_magnitude,
            belt_width_m.magnitude,
            troughing_rad.magnitude,
            banking_rad.magnitude,
            inside_width_m.magnitude,
            friction_var.magnitude,
            friction_coeff.magnitude,
            normal_force_n.magnitude,
        )

    # Attach units and convert with enhanced error handling
    result = result_magnitude * u.ureg.newton
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["invalid_unit"].format(unit=unit, error=e))

    # Apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def tilted_idler_friction_force_outside(
    total_weight_force_material: "Quantity",
    inclination_angle: "Quantity",
    belt_width: "Quantity",
    troughing_angle: "Quantity",
    banking_angle: "Quantity",
    belt_width_on_outside_wing_roll: "Quantity",
    friction_variation: "Quantity",
    friction_coefficient_tilted_idler: "Quantity",
    normal_force_on_idler_roll: "Quantity",
    wing_roll_load_factor: Optional["Quantity"] = None,
    method: str = CONVENTIONAL_METHOD,
    unit: str = "newton",
    precision: int = 2,
) -> "Quantity":
    """
    Calculate the friction force from conveyed material acting on tilted idlers at the outside wing roll.

    This function provides a unit-aware interface for calculating the friction force
    component that results from conveyed material acting on tilted idlers positioned
    at the outside wing roll of a troughed belt conveyor operating in a horizontal curve.

    Parameters
    ----------
    total_weight_force_material : Quantity
        Total weight force of the conveyed material
    inclination_angle : Quantity
        Inclination angle of the belt conveyor
    belt_width : Quantity
        Total width of the belt
    troughing_angle : Quantity
        Troughing angle of the belt
    banking_angle : Quantity
        Banking angle of the belt in the horizontal curve
    belt_width_on_outside_wing_roll : Quantity
        Effective width of the belt supported by the outside wing roll
    friction_variation : Quantity
        Friction variation factor (dimensionless)
    friction_coefficient_tilted_idler : Quantity
        Friction coefficient for material-idler interaction (dimensionless)
    normal_force_on_idler_roll : Quantity
        Additional normal force acting on the idler roll
    wing_roll_load_factor : Quantity, optional
        Load factor for wing roll considering improved load distribution (dimensionless).
        Default is 1.1. Only used for improved method.
    method : str, optional
        Calculation method to use. Must be one of ['conventional', 'improved'].
        Default is 'conventional'.
    unit : str, optional
        Output unit for the force. Default is "newton".
    precision : int, optional
        Number of decimal places for the result. Default is 2.

    Returns
    -------
    Quantity
        Friction force component from material on outside wing roll tilted idlers.

    Raises
    ------
    ValueError
        If input parameters are invalid or unit conversion fails.

    Notes
    -----
    This calculation considers the interaction between conveyed material and tilted
    idlers in the outside wing roll position of a troughed belt conveyor system
    operating in horizontal curves.

    The friction force arises from the normal force of material on the tilted idlers
    combined with geometric factors including troughing angle, banking angle, and
    belt width distribution.

    Physical constraints checked:
    - All force inputs must be non-negative
    - Belt widths must be positive
    - Outside wing roll width must not exceed total belt width
    - Friction coefficients must be non-negative

    Examples
    --------
    >>> import eytelwein.main.units as u
    >>> from eytelwein.horizontal_curves import tilted_idler_friction_force_outside
    >>> force = tilted_idler_friction_force_outside(
    ...     total_weight_force_material=156.71 * u.ureg.newton,
    ...     inclination_angle=0 * u.ureg.degree,
    ...     belt_width=0.8 * u.ureg.meter,
    ...     troughing_angle=30 * u.ureg.degree,
    ...     banking_angle=1.46 * u.ureg.degree,
    ...     belt_width_on_outside_wing_roll=0.1825 * u.ureg.meter,
    ...     friction_variation=0.7 * u.ureg.dimensionless,
    ...     friction_coefficient_tilted_idler=0.216 * u.ureg.dimensionless,
    ...     normal_force_on_idler_roll=0 * u.ureg.newton
    ... )
    >>> print(f"Friction force: {force:.2f}")
    Friction force: 4.11 newton
    """
    # Convert inputs to standard units with enhanced error handling
    try:
        total_force_n = total_weight_force_material.to(u.ureg.newton)
        inclination_rad = inclination_angle.to(u.ureg.radian)
        belt_width_m = belt_width.to(u.ureg.meter)
        troughing_rad = troughing_angle.to(u.ureg.radian)
        banking_rad = banking_angle.to(u.ureg.radian)
        outside_width_m = belt_width_on_outside_wing_roll.to(u.ureg.meter)
        friction_var = friction_variation.to(u.ureg.dimensionless)
        friction_coeff = friction_coefficient_tilted_idler.to(u.ureg.dimensionless)
        normal_force_n = normal_force_on_idler_roll.to(u.ureg.newton)
    except Exception as e:
        raise ValueError(
            ERROR_MESSAGES["unit_conversion"].format(param="input", error=e)
        )

    # Enhanced physical constraints validation
    if total_force_n.magnitude < 0:
        raise ValueError(
            ERROR_MESSAGES["negative_force"].format(value=total_force_n.magnitude)
        )

    if normal_force_n.magnitude < 0:
        raise ValueError(
            f"Normal force must be non-negative, got {normal_force_n.magnitude}"
        )

    if belt_width_m.magnitude <= 0:
        raise ValueError(
            ERROR_MESSAGES["positive_width"].format(value=belt_width_m.magnitude)
        )

    if outside_width_m.magnitude <= 0:
        raise ValueError(
            ERROR_MESSAGES["positive_width"].format(value=outside_width_m.magnitude)
        )

    if outside_width_m.magnitude > belt_width_m.magnitude:
        raise ValueError(ERROR_MESSAGES["invalid_width"])

    if friction_var.magnitude < 0:
        raise ValueError(
            f"Friction variation must be non-negative, got {friction_var.magnitude}"
        )

    if friction_coeff.magnitude < 0:
        raise ValueError(
            f"Friction coefficient must be non-negative, got {friction_coeff.magnitude}"
        )

    # Validate method parameter
    if method not in VALID_METHODS:
        raise ValueError(f"Invalid method '{method}'. Must be one of {VALID_METHODS}")

    # Handle wing_roll_load_factor for improved method
    if wing_roll_load_factor is None:
        wing_roll_load_factor = DEFAULT_WING_LOAD_FACTOR * u.ureg.dimensionless

    try:
        wing_load_factor = wing_roll_load_factor.to(u.ureg.dimensionless)
    except Exception as e:
        raise ValueError(
            ERROR_MESSAGES["unit_conversion"].format(
                param="wing_roll_load_factor", error=e
            )
        )

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.ureg.parse_units(unit)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["invalid_unit"].format(unit=unit, error=e))

    # Method dispatch
    if method == CONVENTIONAL_METHOD:
        result_magnitude = _tilted_idler_friction_force_outside_conventional(
            total_force_n.magnitude,
            inclination_rad.magnitude,
            belt_width_m.magnitude,
            troughing_rad.magnitude,
            banking_rad.magnitude,
            outside_width_m.magnitude,
            friction_var.magnitude,
            friction_coeff.magnitude,
            normal_force_n.magnitude,
        )
    elif method == IMPROVED_METHOD:
        result_magnitude = _tilted_idler_friction_force_outside_improved(
            total_force_n.magnitude,
            inclination_rad.magnitude,
            wing_load_factor.magnitude,
            belt_width_m.magnitude,
            troughing_rad.magnitude,
            banking_rad.magnitude,
            outside_width_m.magnitude,
            friction_var.magnitude,
            friction_coeff.magnitude,
            normal_force_n.magnitude,
        )
    else:
        raise ValueError(f"Unsupported method: {method}")

    # Attach units and convert with enhanced error handling
    result = result_magnitude * u.ureg.newton
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["invalid_unit"].format(unit=unit, error=e))

    # Apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def tilted_idler_friction_force_outside_improved(
    total_weight_force_material: "Quantity",
    inclination_angle: "Quantity",
    wing_roll_load_factor: "Quantity",
    belt_width: "Quantity",
    troughing_angle: "Quantity",
    banking_angle: "Quantity",
    belt_width_on_outside_wing_roll: "Quantity",
    friction_variation: "Quantity",
    friction_coefficient_tilted_idler: "Quantity",
    normal_force_on_idler_roll: Optional["Quantity"] = None,
    unit: str = "newton",
    precision: int = 2,
) -> "Quantity":
    """
    Calculate the friction force from conveyed material acting on tilted idlers at the outside wing roll - improved method.

    This function provides a dedicated interface for the improved calculation method
    of friction force component that results from conveyed material acting on tilted idlers
    positioned at the outside wing roll of a troughed belt conveyor operating in a horizontal curve.

    Parameters
    ----------
    total_weight_force_material : Quantity
        Total weight force of the conveyed material
    inclination_angle : Quantity
        Inclination angle of the belt conveyor
    wing_roll_load_factor : Quantity
        Load factor for wing roll considering improved load distribution (dimensionless)
    belt_width : Quantity
        Total width of the belt
    troughing_angle : Quantity
        Troughing angle of the belt
    banking_angle : Quantity
        Banking angle of the belt in the horizontal curve
    belt_width_on_outside_wing_roll : Quantity
        Effective width of the belt supported by the outside wing roll
    friction_variation : Quantity
        Friction variation factor (dimensionless)
    friction_coefficient_tilted_idler : Quantity
        Friction coefficient for material-idler interaction (dimensionless)
    normal_force_on_idler_roll : Quantity, optional
        Additional normal force acting on the idler roll. Default is 0 N.
    unit : str, optional
        Output unit for the force. Default is "newton".
    precision : int, optional
        Number of decimal places for the result. Default is None.

    Returns
    -------
    Quantity
        Friction force component from material on outside wing roll tilted idlers (improved method).

    Examples
    --------
    >>> import eytelwein.main.units as u
    >>> force = tilted_idler_friction_force_outside_improved(
    ...     total_weight_force_material=156.71 * u.ureg.newton,
    ...     inclination_angle=0 * u.ureg.degree,
    ...     wing_roll_load_factor=1.1 * u.ureg.dimensionless,
    ...     belt_width=0.8 * u.ureg.meter,
    ...     troughing_angle=30 * u.ureg.degree,
    ...     banking_angle=1.46 * u.ureg.degree,
    ...     belt_width_on_outside_wing_roll=0.1825 * u.ureg.meter,
    ...     friction_variation=0.7 * u.ureg.dimensionless,
    ...     friction_coefficient_tilted_idler=0.216 * u.ureg.dimensionless,
    ...     normal_force_on_idler_roll=0 * u.ureg.newton
    ... )
    >>> print(f"Friction force: {force:.2f}")
    Friction force: 5.22 newton
    """
    # Set default normal force if not provided
    if normal_force_on_idler_roll is None:
        normal_force_on_idler_roll = 0 * u.ureg.newton

    # Use the unified function with improved method
    return tilted_idler_friction_force_outside(
        total_weight_force_material=total_weight_force_material,
        inclination_angle=inclination_angle,
        belt_width=belt_width,
        troughing_angle=troughing_angle,
        banking_angle=banking_angle,
        belt_width_on_outside_wing_roll=belt_width_on_outside_wing_roll,
        friction_variation=friction_variation,
        friction_coefficient_tilted_idler=friction_coefficient_tilted_idler,
        normal_force_on_idler_roll=normal_force_on_idler_roll,
        wing_roll_load_factor=wing_roll_load_factor,
        method=IMPROVED_METHOD,
        unit=unit,
        precision=precision,
    )


def tilted_idler_friction_force_center(
    total_weight_force_material: "Quantity",
    inclination_angle: "Quantity",
    belt_width: "Quantity",
    troughing_angle: "Quantity",
    banking_angle: "Quantity",
    belt_width_on_center_wing_roll: "Quantity",
    belt_width_on_inside_wing_roll: "Quantity",
    belt_width_on_outside_wing_roll: "Quantity",
    friction_variation: "Quantity",
    friction_coefficient_tilted_idler: "Quantity",
    normal_force_on_idler_roll: "Quantity" = None,
    method: str = CONVENTIONAL_METHOD,
    center_roll_load_factor: Optional["Quantity"] = None,
    unit: str = "newton",
    precision: int = 2,
) -> "Quantity":
    """
    Calculate the friction force from conveyed material acting on tilted idlers at the center section.

    This function calculates the friction force arising from the interaction between
    conveyed material and tilted idlers positioned at the center section of a troughed
    belt conveyor system operating in horizontal curves. The center section calculation
    uniquely combines effects from all three belt sections (center, inside, outside).

    Parameters
    ----------
    total_weight_force_material : Quantity
        Total weight force of the conveyed material
    inclination_angle : Quantity
        Inclination angle of the belt conveyor
    belt_width : Quantity
        Total width of the belt
    troughing_angle : Quantity
        Troughing angle of the belt
    banking_angle : Quantity
        Banking angle of the belt in the horizontal curve
    belt_width_on_center_wing_roll : Quantity
        Effective width of the belt supported by the center section
    belt_width_on_inside_wing_roll : Quantity
        Effective width of the belt supported by the inside wing roll
    belt_width_on_outside_wing_roll : Quantity
        Effective width of the belt supported by the outside wing roll
    friction_variation : Quantity
        Friction variation factor (dimensionless)
    friction_coefficient_tilted_idler : Quantity
        Friction coefficient for material-idler interaction (dimensionless)
    normal_force_on_idler_roll : Quantity, optional
        Additional normal force acting on the idler roll. Default is 0.0 * u.newton.
    method : str, optional
        Calculation methodology. Currently supports:
        - "conventional": Standard method from Grimmer & Kessler (1987) Teil I
        - "improved": Enhanced method from Grimmer & Kessler (1987) Teil II
        Default is "conventional".
    center_roll_load_factor : Quantity, optional
        Load factor for center roll. If None and method="improved", defaults to 0.9.
        Ignored for conventional method.
    unit : str, optional
        The unit for the returned force. Default is "newton".
    precision : int, optional
        Number of decimal places to round the result to. If None, no rounding is applied.

    Returns
    -------
    Quantity
        Friction force component from material on center section tilted idlers with specified units.

    Raises
    ------
    ValueError
        If unit conversion fails, if belt widths are invalid, if weights are negative,
        or if calculation parameters are outside valid ranges.

    Notes
    -----
    The center section friction force calculation is unique as it considers the combined
    influence of all three belt sections. This comprehensive approach accounts for the
    complex load distribution that occurs in horizontal curves.

    Mathematical formulation combines three components:
    1. Center component: (w_center/w_total) * F_material * cos(β) * cos(α)
    2. Inside component: (w_inside/w_total) * F_material * sin(λ + β) * sin(λ) * cos(α)
    3. Outside component: (w_outside/w_total) * F_material * sin(λ - β) * sin(λ) * cos(α)

    Final calculation: F = f_var * μ * (F_center + F_inside + F_outside + F_normal)

    Where:
    - f_var is the friction variation factor
    - μ is the friction coefficient for tilted idler interaction
    - λ is the troughing angle, β is the banking angle, α is the inclination angle
    - w_*/w_total are the width ratios for each section
    - F_material is the total material weight force
    - F_normal is the additional normal force on the idler roll

    Examples
    --------
    >>> import eytelwein.main.units as u
    >>> from eytelwein.horizontal_curves import tilted_idler_friction_force_center
    >>>
    >>> # Basic calculation with SI units
    >>> force = tilted_idler_friction_force_center(
    ...     total_weight_force_material=200.0 * u.ureg.newton,
    ...     inclination_angle=0.0 * u.ureg.radian,
    ...     belt_width=1.0 * u.ureg.meter,
    ...     troughing_angle=20.0 * u.ureg.degree,
    ...     banking_angle=2.0 * u.ureg.degree,
    ...     belt_width_on_center_wing_roll=0.4 * u.ureg.meter,
    ...     belt_width_on_inside_wing_roll=0.3 * u.ureg.meter,
    ...     belt_width_on_outside_wing_roll=0.3 * u.ureg.meter,
    ...     friction_variation=1.0 * u.ureg.dimensionless,
    ...     friction_coefficient_tilted_idler=0.3 * u.ureg.dimensionless
    ... )
    >>> print(f"Center friction force: {force:.2f}")
    Center friction force: 28.19 newton

    References
    ----------
    Grimmer, K.-J. und F. Kessler: Teil I - Traditional calculation approaches.
    Grimmer, K.-J. und F. Kessler: Teil II - Enhanced calculation procedures.
    """
    # Handle default value for normal_force_on_idler_roll
    if normal_force_on_idler_roll is None:
        normal_force_on_idler_roll = 0.0 * u.ureg.newton

    # Convert inputs to standard units with enhanced error handling
    try:
        material_force_n = total_weight_force_material.to(u.ureg.newton)
        inclination_rad = inclination_angle.to(u.ureg.radian)
        belt_width_m = belt_width.to(u.ureg.meter)
        troughing_rad = troughing_angle.to(u.ureg.radian)
        banking_rad = banking_angle.to(u.ureg.radian)
        center_width_m = belt_width_on_center_wing_roll.to(u.ureg.meter)
        inside_width_m = belt_width_on_inside_wing_roll.to(u.ureg.meter)
        outside_width_m = belt_width_on_outside_wing_roll.to(u.ureg.meter)
        friction_var = friction_variation.to(u.ureg.dimensionless)
        friction_coeff = friction_coefficient_tilted_idler.to(u.ureg.dimensionless)
        normal_force_n = normal_force_on_idler_roll.to(u.ureg.newton)
    except Exception as e:
        raise ValueError(
            ERROR_MESSAGES["unit_conversion"].format(param="input", error=e)
        )

    # Enhanced physical constraints validation
    if material_force_n.magnitude < 0:
        raise ValueError(
            ERROR_MESSAGES["negative_force"].format(value=material_force_n.magnitude)
        )

    if belt_width_m.magnitude <= 0:
        raise ValueError(
            ERROR_MESSAGES["positive_width"].format(value=belt_width_m.magnitude)
        )

    if normal_force_n.magnitude < 0:
        raise ValueError(
            f"Normal force must be non-negative, got {normal_force_n.magnitude}"
        )

    # Width validation
    if (
        center_width_m.magnitude > belt_width_m.magnitude
        or inside_width_m.magnitude > belt_width_m.magnitude
        or outside_width_m.magnitude > belt_width_m.magnitude
    ):
        raise ValueError(ERROR_MESSAGES["invalid_width"])

    if friction_var.magnitude < 0:
        raise ValueError(
            f"Friction variation must be non-negative, got {friction_var.magnitude}"
        )

    if friction_coeff.magnitude < 0:
        raise ValueError(
            f"Friction coefficient must be non-negative, got {friction_coeff.magnitude}"
        )

    # Method validation
    if method not in VALID_METHODS:
        raise ValueError(
            ERROR_MESSAGES["invalid_method"].format(
                method=method, valid_methods=VALID_METHODS
            )
        )

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.ureg.parse_units(unit)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["invalid_unit"].format(unit=unit, error=e))

    # Load factor handling with defaults for improved method
    if method == IMPROVED_METHOD:
        if center_roll_load_factor is None:
            center_roll_load_factor = DEFAULT_CENTER_LOAD_FACTOR * u.ureg.dimensionless

        # Type narrowing: center_roll_load_factor is guaranteed to be Quantity here
        assert center_roll_load_factor is not None
        try:
            load_factor_magnitude = center_roll_load_factor.to(
                u.ureg.dimensionless
            ).magnitude
        except Exception as e:
            raise ValueError(
                ERROR_MESSAGES["unit_conversion"].format(
                    param="center_roll_load_factor", error=e
                )
            )

        # Add physical meaningfulness validation
        if load_factor_magnitude < 0:
            raise ValueError(
                "center_roll_load_factor must be non-negative for physical meaningfulness"
            )

    # Call the appropriate private implementation based on method
    if method == CONVENTIONAL_METHOD:
        result_magnitude = _tilted_idler_friction_force_center_conventional(
            material_force_n.magnitude,
            inclination_rad.magnitude,
            belt_width_m.magnitude,
            troughing_rad.magnitude,
            banking_rad.magnitude,
            center_width_m.magnitude,
            inside_width_m.magnitude,
            outside_width_m.magnitude,
            friction_var.magnitude,
            friction_coeff.magnitude,
            normal_force_n.magnitude,
        )
    elif method == IMPROVED_METHOD:
        result_magnitude = _tilted_idler_friction_force_center_improved(
            material_force_n.magnitude,
            inclination_rad.magnitude,
            load_factor_magnitude,
            belt_width_m.magnitude,
            troughing_rad.magnitude,
            banking_rad.magnitude,
            center_width_m.magnitude,
            inside_width_m.magnitude,
            outside_width_m.magnitude,
            friction_var.magnitude,
            friction_coeff.magnitude,
            normal_force_n.magnitude,
        )

    # Attach units and convert with enhanced error handling
    result = result_magnitude * u.ureg.newton
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["invalid_unit"].format(unit=unit, error=e))

    # Apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def restraining_force_from_tilted_idlers(
    force_component_inside: "Quantity",
    force_component_center: "Quantity",
    force_component_outside: "Quantity",
    method: str = CONVENTIONAL_METHOD,
    unit: str = "newton",
    precision: int = 2,
) -> "Quantity":
    """
    Calculate the restraining force from tilted idlers towards the outside curve.

    This function provides a unified interface for calculating the resultant restraining force
    that acts to guide the belt towards the outside of horizontal curves when idler rolls are
    suitably tilted. It supports both conventional and improved methodologies with
    comprehensive unit handling and validation.

    Parameters
    ----------
    force_component_inside : Quantity
        Force component acting on the inside wing roll from tilted idler friction [force]
    force_component_center : Quantity
        Force component acting in the center section from tilted idler friction [force]
    force_component_outside : Quantity
        Force component acting on the outside wing roll from tilted idler friction [force]
    method : str, optional
        Calculation methodology:
        - "conventional": Standard method from Grimmer & Kessler (1987) Teil I
        - "improved": Enhanced method from Grimmer & Kessler (1987) Teil II
        Default is "conventional".
    unit : str, optional
        Output unit for the force. Default is "newton".
    precision : int, optional
        Number of decimal places for the result. Default is 2.

    Returns
    -------
    Quantity
        Net restraining force from tilted idler friction effects with specified unit.

    Raises
    ------
    ValueError
        If input parameters are invalid, method is unknown, or unit conversion fails.

    Notes
    -----
    This function implements the Method A architectural pattern with method parameter
    dispatch, providing a unified interface that dispatches to the appropriate
    private implementation based on the specified method.

    The calculation combines force components from tilted idler friction effects following
    the standard force balance methodology for horizontal curve analysis:

    F_net = F_inside + F_center - F_outside

    Where the subtraction of the outside component reflects the opposing nature
    of forces in horizontal curves.

    Available calculation methods:
    1. Conventional Method (method="conventional"):
       - Based on Grimmer & Kessler (1987) Teil I
       - Traditional calculation approaches

    2. Improved Method (method="improved"):
       - Based on Grimmer & Kessler (1987) Teil II
       - Enhanced calculation procedures with improvements to conventional methods

    Examples
    --------
    >>> import eytelwein.main.units as u
    >>> from eytelwein.horizontal_curves import restraining_force_from_tilted_idlers
    >>>
    >>> result = restraining_force_from_tilted_idlers(
    ...     force_component_inside=530.29 * u.ureg.newton,
    ...     force_component_center=87.49 * u.ureg.newton,
    ...     force_component_outside=433.01 * u.ureg.newton,
    ...     method="conventional"
    ... )
    >>> print(f"Net restraining force from tilted idlers: {result:.2f}")
    Net restraining force from tilted idlers: 184.77 newton

    References
    ----------
    Grimmer, K.-J. und F. Kessler: Teil I - Traditional calculation approaches.
    Grimmer, K.-J. und F. Kessler: Teil II - Enhanced calculation procedures.
    """
    # Convert inputs to standard units with enhanced error handling
    try:
        inside_force_n = force_component_inside.to(u.ureg.newton)
        center_force_n = force_component_center.to(u.ureg.newton)
        outside_force_n = force_component_outside.to(u.ureg.newton)
    except Exception as e:
        raise ValueError(
            ERROR_MESSAGES["unit_conversion"].format(param="input", error=e)
        )

    # Method validation
    if method not in VALID_METHODS:
        raise ValueError(
            ERROR_MESSAGES["invalid_method"].format(
                method=method, valid_methods=VALID_METHODS
            )
        )

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.ureg.parse_units(unit)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["invalid_unit"].format(unit=unit, error=e))

    # Calculate using the appropriate private implementation based on method
    if method == CONVENTIONAL_METHOD:
        result_magnitude = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                inside_force_n.magnitude,
                center_force_n.magnitude,
                outside_force_n.magnitude,
            )
        )
    elif method == IMPROVED_METHOD:
        result_magnitude = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_improved(
                inside_force_n.magnitude,
                center_force_n.magnitude,
                outside_force_n.magnitude,
            )
        )

    # Attach units and convert with enhanced error handling
    result = result_magnitude * u.ureg.newton
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(ERROR_MESSAGES["invalid_unit"].format(unit=unit, error=e))

    # Apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result
