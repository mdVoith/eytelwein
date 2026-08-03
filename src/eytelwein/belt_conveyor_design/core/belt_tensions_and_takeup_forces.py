"""Public API for belt tensions and takeup forces calculations.

This module provides the Quantity-based public interface for calculations
in the belt-tensions-and-takeup-forces domain. Each public function wraps
the corresponding private helper with unit conversion, validation, and
output formatting.
"""

from dataclasses import dataclass
from pint import Quantity
from eytelwein.belt_conveyor_design.core._belt_tensions_and_takeup_forces import (
    _minimum_belt_tension_from_sag_carry,
    _takeup_weight_force_from_takeup_weight,
    _takeup_weight_from_takeup_weight_force,
    _rope_travel_from_takeup_travel,
    _takeup_travel_from_rope_travel,
    _effort_force_from_load_force,
    _load_force_from_effort_force,
)
from eytelwein.main.units import get_unit_registry
from eytelwein.main.validation import validate_positive_count

# Get the unit registry
u = get_unit_registry()


def minimum_belt_tension_from_sag_carry(
    line_load_belt: Quantity,
    line_load_material: Quantity,
    idler_spacing: Quantity,
    allowable_sag: Quantity,
    unit: str = "kilonewton",
    precision: int | None = None,
) -> Quantity:
    """
    Calculate minimum belt tension from sag during carry run.

    This function applies the relationship between belt tension,
    belt and material line loads, idler spacing, and allowable sag.
    All inputs must be strict Quantity objects with explicit units.

    Parameters
    ----------
    line_load_belt : Quantity
        Belt line load (mass per unit length) in kg/m or equivalent units.
    line_load_material : Quantity
        Material line load (mass per unit length) in kg/m or equivalent units.
    idler_spacing : Quantity
        Distance between consecutive idlers (e.g., 1.5 meter).
    allowable_sag : Quantity
        Allowable sag as a dimensionless fraction of idler spacing
        (e.g., 0.01 for 1%). Must be a Quantity with dimensionless units.
    unit : str, optional
        Output unit for tension result (default: "kilonewton").
        Common values: "newton", "kilonewton".
        Must be a force unit.
    precision : int or None, optional
        Decimal places to round the result to (default: None).
        If None, no rounding is applied.

    Returns
    -------
    Quantity
        Minimum belt tension in the specified output unit.

    Raises
    ------
    ValueError
        If unit conversion fails due to incompatible input units.
    ValueError
        If line_load_belt is negative.
    ValueError
        If line_load_material is negative.
    ValueError
        If idler_spacing is negative.
    ValueError
        If allowable_sag is not positive or invalid.

    Examples
    --------
    >>> from pint import Quantity
    >>> from eytelwein.main.units import get_unit_registry
    >>> u = get_unit_registry()
    >>> result = minimum_belt_tension_from_sag_carry(
    ...     line_load_belt=Quantity(5.0, u.kilogram / u.meter),
    ...     line_load_material=Quantity(10.0, u.kilogram / u.meter),
    ...     idler_spacing=Quantity(1.5, u.meter),
    ...     allowable_sag=Quantity(0.01, u.dimensionless),
    ... )
    >>> result  # doctest: +SKIP
    2.75812... kilonewton
    """
    try:
        # Convert inputs to standard working units
        line_load_belt_kg_m = line_load_belt.to(u.kilogram / u.meter)
        line_load_material_kg_m = line_load_material.to(u.kilogram / u.meter)
        idler_spacing_m = idler_spacing.to(u.meter)

        # Convert allowable_sag to dimensionless
        sag_percent_val = allowable_sag.to(u.dimensionless).magnitude
    except Exception as e:
        raise ValueError(f"Error in unit conversion: {e}")

    # Validate physical constraints after unit conversion
    if line_load_belt_kg_m.magnitude < 0:
        raise ValueError(
            f"line_load_belt cannot be negative, got {line_load_belt_kg_m}"
        )

    if line_load_material_kg_m.magnitude < 0:
        raise ValueError(
            f"line_load_material cannot be negative, got {line_load_material_kg_m}"
        )

    if idler_spacing_m.magnitude < 0:
        raise ValueError(f"idler_spacing cannot be negative, got {idler_spacing_m}")

    # Ensure the output unit is valid
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Call private implementation with magnitude values
    tension_newtons = _minimum_belt_tension_from_sag_carry(
        line_load_belt_kg_per_m=line_load_belt_kg_m.magnitude,
        line_load_material_kg_per_m=line_load_material_kg_m.magnitude,
        idler_spacing_m=idler_spacing_m.magnitude,
        allowable_sag=sag_percent_val,
    )

    # Attach units to result (newtons)
    result = tension_newtons * u.newton

    # Convert to requested output unit
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(f"Error in attaching unit '{unit}': {e}")

    # Apply precision rounding if specified
    if precision is not None:
        result = round(result, precision)

    return result


def takeup_weight_force_from_takeup_weight(
    takeup_weight: Quantity,
    unit: str = "kilonewton",
    precision: int | None = None,
) -> Quantity:
    """
    Calculate takeup weight force from takeup weight.

    This function converts a mass-based takeup weight to a force quantity
    using the standard gravitational acceleration constant.
    All inputs must be strict Quantity objects with explicit units.

    Parameters
    ----------
    takeup_weight : Quantity
        Takeup weight in kg or equivalent mass units.
    unit : str, optional
        Output unit for force result (default: "kilonewton").
        Common values: "newton", "kilonewton".
        Must be a force unit.
    precision : int or None, optional
        Decimal places to round the result to (default: None).
        If None, no rounding is applied.

    Returns
    -------
    Quantity
        Takeup weight force in the specified output unit.

    Raises
    ------
    ValueError
        If unit conversion fails due to incompatible input units.
    ValueError
        If takeup_weight is negative.
    ValueError
        If unit is invalid or incompatible with force.

    Examples
    --------
    >>> from pint import Quantity
    >>> from eytelwein.main.units import get_unit_registry
    >>> u = get_unit_registry()
    >>> result = takeup_weight_force_from_takeup_weight(
    ...     takeup_weight=Quantity(3000.0, u.kilogram)
    ... )
    >>> result  # doctest: +SKIP
    29.41995... kilonewton
    """
    try:
        # Convert input to standard working units (kg)
        takeup_weight_kg = takeup_weight.to(u.kilogram)
    except Exception as e:
        raise ValueError(f"Error in unit conversion: {e}")

    # Validate physical constraints after unit conversion
    # Handle both scalar and array magnitudes
    magnitude = takeup_weight_kg.magnitude
    try:
        import numpy as np

        if isinstance(magnitude, np.ndarray):
            if np.any(magnitude < 0):
                raise ValueError(
                    f"takeup_weight cannot be negative, got {takeup_weight_kg}"
                )
        elif magnitude < 0:
            raise ValueError(
                f"takeup_weight cannot be negative, got {takeup_weight_kg}"
            )
    except (ImportError, TypeError):
        # Fall back to simple comparison if numpy not available or comparison fails
        # Normalize any comparison error to ValueError for consistent behavior
        try:
            if magnitude < 0:
                raise ValueError(
                    f"takeup_weight cannot be negative, got {takeup_weight_kg}"
                )
        except TypeError:
            raise ValueError(
                f"takeup_weight cannot be negative, got {takeup_weight_kg}"
            )

    # Ensure the output unit is valid
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Call private implementation with magnitude value
    force_newtons = _takeup_weight_force_from_takeup_weight(
        takeup_weight_kg=takeup_weight_kg.magnitude
    )

    # Attach units to result (newtons)
    result = force_newtons * u.newton

    # Convert to requested output unit
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(f"Error in attaching unit '{unit}': {e}")

    # Apply precision rounding if specified
    if precision is not None:
        result = round(result, precision)

    return result


def takeup_weight_from_takeup_weight_force(
    takeup_weight_force: Quantity,
    unit: str = "kilogram",
    precision: int | None = None,
) -> Quantity:
    """
    Calculate takeup weight from takeup weight force.

    This function converts a force-based takeup weight force to a mass quantity
    using the standard gravitational acceleration constant.
    All inputs must be strict Quantity objects with explicit units.

    Parameters
    ----------
    takeup_weight_force : Quantity
        Takeup weight force in newtons or equivalent force units.
    unit : str, optional
        Output unit for mass result (default: "kilogram").
        Common values: "kilogram", "gram".
        Must be a mass unit.
    precision : int or None, optional
        Decimal places to round the result to (default: None).
        If None, no rounding is applied.

    Returns
    -------
    Quantity
        Takeup weight in the specified output unit.

    Raises
    ------
    ValueError
        If unit conversion fails due to incompatible input units.
    ValueError
        If takeup_weight_force is negative.
    ValueError
        If unit is invalid or incompatible with mass.

    Examples
    --------
    >>> from pint import Quantity
    >>> from eytelwein.main.units import get_unit_registry
    >>> u = get_unit_registry()
    >>> result = takeup_weight_from_takeup_weight_force(
    ...     takeup_weight_force=Quantity(29419.95, u.newton)
    ... )
    >>> result  # doctest: +SKIP
    3000.0... kilogram
    """
    try:
        # Convert input to standard working units (newtons)
        takeup_weight_force_n = takeup_weight_force.to(u.newton)
    except Exception as e:
        raise ValueError(f"Error in unit conversion: {e}")

    # Validate physical constraints after unit conversion
    # Handle both scalar and array magnitudes
    magnitude = takeup_weight_force_n.magnitude
    try:
        import numpy as np

        if isinstance(magnitude, np.ndarray):
            if np.any(magnitude < 0):
                raise ValueError(
                    f"takeup_weight_force cannot be negative, got {takeup_weight_force_n}"
                )
        elif magnitude < 0:
            raise ValueError(
                f"takeup_weight_force cannot be negative, got {takeup_weight_force_n}"
            )
    except (ImportError, TypeError):
        # Fall back to simple comparison if numpy not available or comparison fails
        # Normalize any comparison error to ValueError for consistent behavior
        try:
            if magnitude < 0:
                raise ValueError(
                    f"takeup_weight_force cannot be negative, got {takeup_weight_force_n}"
                )
        except TypeError:
            raise ValueError(
                f"takeup_weight_force cannot be negative, got {takeup_weight_force_n}"
            )

    # Ensure the output unit is valid
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Call private implementation with magnitude value
    weight_kg = _takeup_weight_from_takeup_weight_force(
        takeup_weight_force_n=takeup_weight_force_n.magnitude
    )

    # Attach units to result (kg)
    result = weight_kg * u.kilogram

    # Convert to requested output unit
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(f"Error in attaching unit '{unit}': {e}")

    # Apply precision rounding if specified
    if precision is not None:
        result = round(result, precision)

    return result


def effort_force_from_load_force(
    load_force: Quantity,
    strand_count: int = 1,
    unit: str = "kilonewton",
    precision: int | None = None,
) -> Quantity:
    """
    Calculate effort force from load force using ideal reeving.

    This function converts a load force to an effort force using the ideal
    reeving relationship where effort = load / strand_count.
    All inputs must be strict Quantity objects with explicit units.

    Parameters
    ----------
    load_force : Quantity
        Load force in newtons or equivalent force units.
    strand_count : int, optional
        Number of strands in ideal reeving system (default: 1).
        Must be a positive integer >= 1.
        This is a plain integer configuration parameter, not a Quantity.
    unit : str, optional
        Output unit for effort force result (default: "kilonewton").
        Common values: "newton", "kilonewton".
        Must be a force unit.
    precision : int or None, optional
        Decimal places to round the result to (default: None).
        If None, no rounding is applied.

    Returns
    -------
    Quantity
        Effort force in the specified output unit.

    Raises
    ------
    ValueError
        If unit conversion fails due to incompatible input units.
    ValueError
        If load_force is negative.
    ValueError
        If unit is invalid or incompatible with force.
    ValueError
        If strand_count is not a positive integer.

    Examples
    --------
    >>> from pint import Quantity
    >>> from eytelwein.main.units import get_unit_registry
    >>> u = get_unit_registry()
    >>> result = effort_force_from_load_force(
    ...     load_force=Quantity(2000.0, u.newton), strand_count=2
    ... )
    >>> result  # doctest: +SKIP
    1.0 kilonewton
    """
    # Validate strand_count using centralized helper
    validate_positive_count(strand_count, "strand_count")

    try:
        # Convert input to standard working units (newtons)
        load_force_n = load_force.to(u.newton)
    except Exception as e:
        raise ValueError(f"Error in unit conversion: {e}")

    # Validate physical constraints after unit conversion
    magnitude = load_force_n.magnitude
    try:
        import numpy as np

        if isinstance(magnitude, np.ndarray):
            if np.any(magnitude < 0):
                raise ValueError(f"load_force cannot be negative, got {load_force_n}")
        elif magnitude < 0:
            raise ValueError(f"load_force cannot be negative, got {load_force_n}")
    except (ImportError, TypeError):
        try:
            if magnitude < 0:
                raise ValueError(f"load_force cannot be negative, got {load_force_n}")
        except TypeError:
            raise ValueError(f"load_force cannot be negative, got {load_force_n}")

    # Ensure the output unit is valid
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Call private implementation with magnitude value and strand_count
    effort_newtons = _effort_force_from_load_force(
        load_force_n=load_force_n.magnitude, strand_count=strand_count
    )

    # Attach units to result (newtons)
    result = effort_newtons * u.newton

    # Convert to requested output unit
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(f"Error in attaching unit '{unit}': {e}")

    # Apply precision rounding if specified
    if precision is not None:
        result = round(result, precision)

    return result


def load_force_from_effort_force(
    effort_force: Quantity,
    strand_count: int = 1,
    unit: str = "kilonewton",
    precision: int | None = None,
) -> Quantity:
    """
    Calculate load force from effort force using ideal reeving.

    This function converts an effort force to a load force using the ideal
    reeving relationship where load = effort * strand_count.
    All inputs must be strict Quantity objects with explicit units.

    Parameters
    ----------
    effort_force : Quantity
        Effort force in newtons or equivalent force units.
    strand_count : int, optional
        Number of strands in ideal reeving system (default: 1).
        Must be a positive integer >= 1.
        This is a plain integer configuration parameter, not a Quantity.
    unit : str, optional
        Output unit for load force result (default: "kilonewton").
        Common values: "newton", "kilonewton".
        Must be a force unit.
    precision : int or None, optional
        Decimal places to round the result to (default: None).
        If None, no rounding is applied.

    Returns
    -------
    Quantity
        Load force in the specified output unit.

    Raises
    ------
    ValueError
        If unit conversion fails due to incompatible input units.
    ValueError
        If effort_force is negative.
    ValueError
        If unit is invalid or incompatible with force.
    ValueError
        If strand_count is not a positive integer.

    Examples
    --------
    >>> from pint import Quantity
    >>> from eytelwein.main.units import get_unit_registry
    >>> u = get_unit_registry()
    >>> result = load_force_from_effort_force(
    ...     effort_force=Quantity(1000.0, u.newton), strand_count=2
    ... )
    >>> result  # doctest: +SKIP
    2.0 kilonewton
    """
    # Validate strand_count using centralized helper
    validate_positive_count(strand_count, "strand_count")

    try:
        # Convert input to standard working units (newtons)
        effort_force_n = effort_force.to(u.newton)
    except Exception as e:
        raise ValueError(f"Error in unit conversion: {e}")

    # Validate physical constraints after unit conversion
    magnitude = effort_force_n.magnitude
    try:
        import numpy as np

        if isinstance(magnitude, np.ndarray):
            if np.any(magnitude < 0):
                raise ValueError(
                    f"effort_force cannot be negative, got {effort_force_n}"
                )
        elif magnitude < 0:
            raise ValueError(f"effort_force cannot be negative, got {effort_force_n}")
    except (ImportError, TypeError):
        try:
            if magnitude < 0:
                raise ValueError(
                    f"effort_force cannot be negative, got {effort_force_n}"
                )
        except TypeError:
            raise ValueError(f"effort_force cannot be negative, got {effort_force_n}")

    # Ensure the output unit is valid
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Call private implementation with magnitude value and strand_count
    load_newtons = _load_force_from_effort_force(
        effort_force_n=effort_force_n.magnitude, strand_count=strand_count
    )

    # Attach units to result (newtons)
    result = load_newtons * u.newton

    # Convert to requested output unit
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(f"Error in attaching unit '{unit}': {e}")

    # Apply precision rounding if specified
    if precision is not None:
        result = round(result, precision)

    return result


def rope_travel_from_takeup_travel(
    takeup_travel: Quantity,
    strand_count: int = 1,
    unit: str = "meter",
    precision: int | None = None,
) -> Quantity:
    """
    Calculate rope travel from takeup travel in an ideal reeving system.

    This function converts a takeup travel distance to a rope travel distance
    using the ideal reeving relationship. For ideal reeving, the rope travels
    a distance equal to the takeup travel multiplied by the strand count.
    All inputs must be strict Quantity objects with explicit units.

    Parameters
    ----------
    takeup_travel : Quantity
        Takeup travel distance in meters or equivalent length units.
    strand_count : int, optional
        Number of strands in ideal reeving system (default: 1).
        Must be a positive integer >= 1.
        This is a plain integer configuration parameter, not a Quantity.
    unit : str, optional
        Output unit for travel result (default: "meter").
        Common values: "meter", "millimeter".
        Must be a length unit.
    precision : int or None, optional
        Decimal places to round the result to (default: None).
        If None, no rounding is applied.

    Returns
    -------
    Quantity
        Rope travel distance in the specified output unit.

    Raises
    ------
    ValueError
        If unit conversion fails due to incompatible input units.
    ValueError
        If takeup_travel is negative.
    ValueError
        If unit is invalid or incompatible with length.
    ValueError
        If strand_count is not a positive integer.

    Notes
    -----
    **Why strand_count is plain int, not Quantity:**
    Discrete configuration counts like strand_count represent the logical
    structure of a reeving system (2-part, 4-part, etc.), not measured values.
    They are always plain integers, while measured travel distances and
    dimensionless computed ratios use Quantity objects.

    **Field-error prevention:**
    The coupled force/travel transforms help prevent a common design error:
    if a load calculation divides force by strand_count for mechanical
    advantage while forgetting the reciprocal travel penalty (multiplying
    by strand_count), the system appears to gain energy. Using coupled
    APIs ensures both transforms are applied correctly.

    Examples
    --------
    >>> from pint import Quantity
    >>> from eytelwein.main.units import get_unit_registry
    >>> u = get_unit_registry()
    >>> result = rope_travel_from_takeup_travel(
    ...     takeup_travel=Quantity(1.5, u.meter), strand_count=2
    ... )
    >>> result  # doctest: +SKIP
    3.0 meter
    """
    # Validate strand_count using centralized helper
    validate_positive_count(strand_count, "strand_count")

    try:
        # Convert input to standard working units (meters)
        takeup_travel_m = takeup_travel.to(u.meter)
    except Exception as e:
        raise ValueError(f"Error in unit conversion: {e}")

    # Validate physical constraints after unit conversion
    # Handle both scalar and array magnitudes
    magnitude = takeup_travel_m.magnitude
    try:
        import numpy as np

        if isinstance(magnitude, np.ndarray):
            if np.any(magnitude < 0):
                raise ValueError(
                    f"takeup_travel cannot be negative, got {takeup_travel_m}"
                )
        elif magnitude < 0:
            raise ValueError(f"takeup_travel cannot be negative, got {takeup_travel_m}")
    except (ImportError, TypeError):
        # Fall back to simple comparison if numpy not available or comparison fails
        try:
            if magnitude < 0:
                raise ValueError(
                    f"takeup_travel cannot be negative, got {takeup_travel_m}"
                )
        except TypeError:
            raise ValueError(f"takeup_travel cannot be negative, got {takeup_travel_m}")

    # Ensure the output unit is valid
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Call private implementation with magnitude value and strand_count
    travel_m = _rope_travel_from_takeup_travel(
        takeup_travel_m=takeup_travel_m.magnitude, strand_count=strand_count
    )

    # Attach units to result (meters)
    result = travel_m * u.meter

    # Convert to requested output unit
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(f"Error in attaching unit '{unit}': {e}")

    # Apply precision rounding if specified
    if precision is not None:
        result = round(result, precision)

    return result


def takeup_travel_from_rope_travel(
    rope_travel: Quantity,
    strand_count: int = 1,
    unit: str = "meter",
    precision: int | None = None,
) -> Quantity:
    """
    Calculate takeup travel from rope travel in an ideal reeving system (inverse).

    This function converts a rope travel distance to a takeup travel distance
    using the inverse ideal reeving relationship. For ideal reeving, the takeup
    travel is the rope travel divided by the strand count.
    All inputs must be strict Quantity objects with explicit units.

    Parameters
    ----------
    rope_travel : Quantity
        Rope travel distance in meters or equivalent length units.
    strand_count : int, optional
        Number of strands in ideal reeving system (default: 1).
        Must be a positive integer >= 1.
        This is a plain integer configuration parameter, not a Quantity.
    unit : str, optional
        Output unit for travel result (default: "meter").
        Common values: "meter", "millimeter".
        Must be a length unit.
    precision : int or None, optional
        Decimal places to round the result to (default: None).
        If None, no rounding is applied.

    Returns
    -------
    Quantity
        Takeup travel distance in the specified output unit.

    Raises
    ------
    ValueError
        If unit conversion fails due to incompatible input units.
    ValueError
        If rope_travel is negative.
    ValueError
        If unit is invalid or incompatible with length.
    ValueError
        If strand_count is not a positive integer.

    Notes
    -----
    **Why strand_count is plain int, not Quantity:**
    Discrete configuration counts like strand_count represent the logical
    structure of a reeving system (2-part, 4-part, etc.), not measured values.
    They are always plain integers, while measured travel distances and
    dimensionless computed ratios use Quantity objects.

    **Field-error prevention:**
    The coupled force/travel transforms help prevent a common design error:
    if a load calculation divides force by strand_count for mechanical
    advantage while forgetting the reciprocal travel penalty (multiplying
    by strand_count), the system appears to gain energy. Using coupled
    APIs ensures both transforms are applied correctly.

    Examples
    --------
    >>> from pint import Quantity
    >>> from eytelwein.main.units import get_unit_registry
    >>> u = get_unit_registry()
    >>> result = takeup_travel_from_rope_travel(
    ...     rope_travel=Quantity(3.0, u.meter), strand_count=2
    ... )
    >>> result  # doctest: +SKIP
    1.5 meter
    """
    # Validate strand_count using centralized helper
    validate_positive_count(strand_count, "strand_count")

    try:
        # Convert input to standard working units (meters)
        rope_travel_m = rope_travel.to(u.meter)
    except Exception as e:
        raise ValueError(f"Error in unit conversion: {e}")

    # Validate physical constraints after unit conversion
    # Handle both scalar and array magnitudes
    magnitude = rope_travel_m.magnitude
    try:
        import numpy as np

        if isinstance(magnitude, np.ndarray):
            if np.any(magnitude < 0):
                raise ValueError(f"rope_travel cannot be negative, got {rope_travel_m}")
        elif magnitude < 0:
            raise ValueError(f"rope_travel cannot be negative, got {rope_travel_m}")
    except (ImportError, TypeError):
        # Fall back to simple comparison if numpy not available or comparison fails
        try:
            if magnitude < 0:
                raise ValueError(f"rope_travel cannot be negative, got {rope_travel_m}")
        except TypeError:
            raise ValueError(f"rope_travel cannot be negative, got {rope_travel_m}")

    # Ensure the output unit is valid
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Call private implementation with magnitude value and strand_count
    travel_m = _takeup_travel_from_rope_travel(
        rope_travel_m=rope_travel_m.magnitude, strand_count=strand_count
    )

    # Attach units to result (meters)
    result = travel_m * u.meter

    # Convert to requested output unit
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(f"Error in attaching unit '{unit}': {e}")

    # Apply precision rounding if specified
    if precision is not None:
        result = round(result, precision)

    return result


@dataclass(frozen=True)
class EffortForceAndRopeTravel:
    """Coupled result of effort-side force and rope travel transformations.

    This result type pairs effort-side force and rope travel to prevent design errors
    where one transform is applied but the other is forgotten.

    Attributes
    ----------
    effort_force : Quantity
        Effort-side force quantity (usually in kilonewton).
    rope_travel : Quantity
        Rope-side travel distance (usually in meter).
    """

    effort_force: Quantity
    rope_travel: Quantity


@dataclass(frozen=True)
class LoadForceAndTravel:
    """Coupled result of load-side force and takeup travel transformations.

    This result type pairs load-side force and takeup travel to prevent design errors
    where one transform is applied but the other is forgotten.

    Attributes
    ----------
    load_force : Quantity
        Load-side force quantity (usually in kilonewton).
    takeup_travel : Quantity
        Takeup-side travel distance (usually in meter).
    """

    load_force: Quantity
    takeup_travel: Quantity


def effort_force_and_rope_travel_from_load_force_and_takeup_travel(
    load_force: Quantity,
    takeup_travel: Quantity,
    strand_count: int = 1,
    force_unit: str = "kilonewton",
    travel_unit: str = "meter",
    precision: int | None = None,
) -> EffortForceAndRopeTravel:
    """Calculate coupled effort-side force and rope travel from load-side force and takeup travel.

    This coupled transform operates on force (not weight) with explicit effort/load terminology.
    It prevents field errors by returning both the force and travel transformations together.
    In ideal reeving, applying only one without the other violates energy conservation.

    Parameters
    ----------
    load_force : Quantity
        Load-side force in newtons or equivalent force units.
    takeup_travel : Quantity
        Takeup-side travel distance in meters or equivalent length units.
    strand_count : int, optional
        Number of strands in ideal reeving system (default: 1).
        Must be a positive integer >= 1.
    force_unit : str, optional
        Output unit for effort force result (default: "kilonewton").
        Must be a force unit.
    travel_unit : str, optional
        Output unit for rope travel result (default: "meter").
        Must be a length unit.
    precision : int or None, optional
        Decimal places to round the results to (default: None).
        If None, no rounding is applied.

    Returns
    -------
    EffortForceAndRopeTravel
        Frozen dataclass with effort_force and rope_travel Quantity fields.

    Raises
    ------
    ValueError
        If unit conversion fails, physical constraints are violated, or
        strand_count is not a positive integer.

    Examples
    --------
    >>> from pint import Quantity
    >>> from eytelwein.main.units import get_unit_registry
    >>> u = get_unit_registry()
    >>> result = effort_force_and_rope_travel_from_load_force_and_takeup_travel(
    ...     load_force=Quantity(29419.95, u.newton),
    ...     takeup_travel=Quantity(1.5, u.meter),
    ...     strand_count=2,
    ... )
    >>> result.effort_force  # doctest: +SKIP
    14.709975... kilonewton
    >>> result.rope_travel  # doctest: +SKIP
    3.0 meter
    """
    validate_positive_count(strand_count, "strand_count")

    effort_force = effort_force_from_load_force(
        load_force=load_force,
        strand_count=strand_count,
        unit=force_unit,
        precision=precision,
    )
    rope_travel = rope_travel_from_takeup_travel(
        takeup_travel=takeup_travel,
        strand_count=strand_count,
        unit=travel_unit,
        precision=precision,
    )
    return EffortForceAndRopeTravel(effort_force=effort_force, rope_travel=rope_travel)


def load_force_and_takeup_travel_from_effort_force_and_rope_travel(
    effort_force: Quantity,
    rope_travel: Quantity,
    strand_count: int = 1,
    force_unit: str = "kilonewton",
    travel_unit: str = "meter",
    precision: int | None = None,
) -> LoadForceAndTravel:
    """Calculate coupled load-side force and takeup travel from effort-side force and rope travel (inverse).

    This coupled inverse transform operates on force (not weight) with explicit effort/load terminology.
    It prevents field errors by returning both the force and travel transformations together.
    In ideal reeving, applying only one without the other violates energy conservation.

    Parameters
    ----------
    effort_force : Quantity
        Effort-side force in newtons or equivalent force units.
    rope_travel : Quantity
        Rope-side travel distance in meters or equivalent length units.
    strand_count : int, optional
        Number of strands in ideal reeving system (default: 1).
        Must be a positive integer >= 1.
    force_unit : str, optional
        Output unit for load force result (default: "kilonewton").
        Must be a force unit.
    travel_unit : str, optional
        Output unit for takeup travel result (default: "meter").
        Must be a length unit.
    precision : int or None, optional
        Decimal places to round the results to (default: None).
        If None, no rounding is applied.

    Returns
    -------
    LoadForceAndTravel
        Frozen dataclass with load_force and takeup_travel Quantity fields.

    Raises
    ------
    ValueError
        If unit conversion fails, physical constraints are violated, or
        strand_count is not a positive integer.

    Examples
    --------
    >>> from pint import Quantity
    >>> from eytelwein.main.units import get_unit_registry
    >>> u = get_unit_registry()
    >>> result = load_force_and_takeup_travel_from_effort_force_and_rope_travel(
    ...     effort_force=Quantity(14709.975, u.newton),
    ...     rope_travel=Quantity(3.0, u.meter),
    ...     strand_count=2,
    ...     force_unit="newton",
    ... )
    >>> result.load_force  # doctest: +SKIP
    29419.95 newton
    >>> result.takeup_travel  # doctest: +SKIP
    1.5 meter
    """
    validate_positive_count(strand_count, "strand_count")

    load_force = load_force_from_effort_force(
        effort_force=effort_force,
        strand_count=strand_count,
        unit=force_unit,
        precision=precision,
    )
    takeup_travel = takeup_travel_from_rope_travel(
        rope_travel=rope_travel,
        strand_count=strand_count,
        unit=travel_unit,
        precision=precision,
    )
    return LoadForceAndTravel(load_force=load_force, takeup_travel=takeup_travel)


# End of belt_tensions_and_takeup_forces module
