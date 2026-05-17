import math

# Method constants for horizontal curve calculations
CONVENTIONAL_METHOD = "conventional"
IMPROVED_METHOD = "improved"
VALID_METHODS = [CONVENTIONAL_METHOD, IMPROVED_METHOD]


def _force_component_towards_inside_curve_from_belt_tension(
    belt_tension: float, idler_spacing: float, horizontal_curve_radius: float
) -> float:
    """
    Calculate the force component towards the inside of the curve from belt tension.

    This function implements the basic horizontal curve force calculation based on
    research methodologies for belt conveyor horizontal curves. The force arises
    from the belt tension acting over the idler spacing divided by the curve radius.

    Parameters
    ----------
    belt_tension : float
        Belt tension at the location of interest [N]
    idler_spacing : float
        Distance between consecutive idler sets [m]
    horizontal_curve_radius : float
        Radius of the horizontal curve [m]

    Returns
    -------
    float
        Force component towards the inside of the curve [N]

    Notes
    -----
    Sign convention: Positive force indicates direction towards the inside of the curve.
    This follows standard mathematical conventions for centripetal forces.

    The calculation is based on the geometric relationship:
    F = T * L / R
    where:
    - F is the force component towards the curve center
    - T is the belt tension
    - L is the idler spacing
    - R is the horizontal curve radius

    Raises
    ------
    ValueError
        If horizontal_curve_radius <= 0
    """
    if horizontal_curve_radius <= 0:
        raise ValueError(
            f"horizontal_curve_radius must be positive, got {horizontal_curve_radius}"
        )
    return belt_tension * idler_spacing / horizontal_curve_radius


def _weight_force_of_belt_conventional(
    weight_force_belt_inside: float,
    weight_force_belt_center: float,
    weight_force_belt_outside: float,
) -> float:
    """
    Calculate the net lateral weight force acting on the belt - conventional method.

    This function implements the conventional methodology from Grimmer & Kessler (1987) Teil I
    for combining the weight force components from the inside wing roll,
    center section, and outside wing roll to determine the net lateral force.

    Parameters
    ----------
    weight_force_belt_inside : float
        Weight force component on the inside wing roll [N]
    weight_force_belt_center : float
        Weight force component in the center section [N]
    weight_force_belt_outside : float
        Weight force component on the outside wing roll [N]

    Returns
    -------
    float
        Net lateral weight force acting on the belt [N]

    Notes
    -----
    This implementation follows the conventional methodology from:
    Grimmer, K.-J. und F. Kessler: Teil I - Traditional calculation approaches.

    Mathematical formulation:
    F_net = F_inside + F_center - F_outside
    """
    return (
        weight_force_belt_inside + weight_force_belt_center - weight_force_belt_outside
    )


def _weight_force_belt_inside_conventional(
    total_weight_force_belt: float,
    inclination_angle: float,
    belt_width: float,
    troughing_angle: float,
    banking_angle: float,
    belt_width_on_inside_wing_roll: float,
) -> float:
    """
    Calculate the weight force component acting on the inside wing roll - conventional method.

    This function implements the conventional methodology from Grimmer & Kessler (1987) Teil I
    for calculating the weight force component that acts on the inside wing roll
    of a troughed belt conveyor in a horizontal curve.

    Parameters
    ----------
    total_weight_force_belt : float
        Total weight force acting on the belt (belt + material) [N]
    inclination_angle : float
        Inclination angle of the belt conveyor [radians]
    belt_width : float
        Total width of the belt [m]
    troughing_angle : float
        Troughing angle of the belt [radians]
    banking_angle : float
        Banking angle of the belt in the horizontal curve [radians]
    belt_width_on_inside_wing_roll : float
        Effective width of the belt supported by the inside wing roll [m]

    Returns
    -------
    float
        Weight force component acting on the inside wing roll [N]

    Notes
    -----
    This implementation follows the conventional methodology from:
    Grimmer, K.-J. und F. Kessler: Teil I - Traditional calculation approaches.

    Mathematical formulation:
    F_inside = F_total * cos(α) * (w_inside/w_total) * sin(λ + β) * cos(λ)

    Raises
    ------
    ValueError
        If belt_width <= 0
    """
    if belt_width <= 0:
        raise ValueError(f"belt_width must be positive, got {belt_width}")
    return (
        total_weight_force_belt
        * math.cos(inclination_angle)
        * (
            belt_width_on_inside_wing_roll
            / belt_width
            * math.sin(troughing_angle + banking_angle)
            * math.cos(troughing_angle)
        )
    )


def _weight_force_belt_outside_conventional(
    total_weight_force_belt: float,
    inclination_angle: float,
    belt_width: float,
    troughing_angle: float,
    banking_angle: float,
    belt_width_on_outside_wing_roll: float,
) -> float:
    """
    Calculate the weight force component acting on the outside wing roll - conventional method.

    This function implements the conventional methodology from Grimmer & Kessler (1987) Teil I
    for calculating the weight force component that acts on the outside wing roll
    of a troughed belt conveyor in a horizontal curve.

    Parameters
    ----------
    total_weight_force_belt : float
        Total weight force acting on the belt (belt + material) [N]
    inclination_angle : float
        Inclination angle of the belt conveyor [radians]
    belt_width : float
        Total width of the belt [m]
    troughing_angle : float
        Troughing angle of the belt [radians]
    banking_angle : float
        Banking angle of the belt in the horizontal curve [radians]
    belt_width_on_outside_wing_roll : float
        Effective width of the belt supported by the outside wing roll [m]

    Returns
    -------
    float
        Weight force component acting on the outside wing roll [N]

    Notes
    -----
    This implementation follows the conventional methodology from:
    Grimmer, K.-J. und F. Kessler: Teil I - Traditional calculation approaches.

    Mathematical formulation:
    F_outside = F_total * cos(α) * (w_outside/w_total) * sin(λ - β) * cos(λ)

    Raises
    ------
    ValueError
        If belt_width <= 0
    """
    if belt_width <= 0:
        raise ValueError(f"belt_width must be positive, got {belt_width}")
    return (
        total_weight_force_belt
        * math.cos(inclination_angle)
        * (
            belt_width_on_outside_wing_roll
            / belt_width
            * math.sin(troughing_angle - banking_angle)
            * math.cos(troughing_angle)
        )
    )


def _weight_force_belt_center_conventional(
    total_weight_force_belt: float,
    inclination_angle: float,
    belt_width: float,
    banking_angle: float,
    belt_width_on_center_wing_roll: float,
) -> float:
    """
    Calculate the weight force component acting on the center section - conventional method.

    This function implements the conventional methodology from Grimmer & Kessler (1987) Teil I
    for calculating the weight force component that acts on the center section
    of a troughed belt conveyor in a horizontal curve.

    Parameters
    ----------
    total_weight_force_belt : float
        Total weight force acting on the belt (belt + material) [N]
    inclination_angle : float
        Inclination angle of the belt conveyor [radians]
    belt_width : float
        Total width of the belt [m]
    banking_angle : float
        Banking angle of the belt in the horizontal curve [radians]
    belt_width_on_center_wing_roll : float
        Effective width of the belt supported by the center section [m]

    Returns
    -------
    float
        Weight force component acting on the center section [N]

    Notes
    -----
    This implementation follows the conventional methodology from:
    Grimmer, K.-J. und F. Kessler: Teil I - Traditional calculation approaches.

    Mathematical formulation:
    F_center = F_total * cos(α) * (w_center/w_total) * sin(β)

    Raises
    ------
    ValueError
        If belt_width <= 0
    """
    if belt_width <= 0:
        raise ValueError(f"belt_width must be positive, got {belt_width}")
    return (
        total_weight_force_belt
        * math.cos(inclination_angle)
        * (belt_width_on_center_wing_roll / belt_width * math.sin(banking_angle))
    )


# weight force of material
def _weight_force_material_inside_conventional(
    normal_force: float, troughing_angle: float, banking_angle: float
) -> float:
    """
    Calculate the weight force component acting on the inside wing roll - conventional method.

    This function implements the conventional methodology from Grimmer & Kessler (1987) Teil I
    for calculating the weight force component that acts on the inside wing roll
    of a troughed belt conveyor in a horizontal curve.

    Parameters
    ----------
    normal_force : float
        Normal force acting on the inside wing roll [N]
    troughing_angle : float
        Troughing angle of the belt [radians]
    banking_angle : float
        Banking angle of the belt in the horizontal curve [radians]

    Returns
    -------
    float
        Weight force component acting on the inside wing roll [N]

    Notes
    -----
    This implementation follows the conventional methodology from:
    Grimmer, K.-J. und F. Kessler: Teil I - Traditional calculation approaches.

    Mathematical formulation:
    F_inside = F_normal * tan(λ + β) * cos(λ)
    """
    return (
        normal_force
        * math.tan(troughing_angle + banking_angle)
        * math.cos(troughing_angle)
    )


def _weight_force_material_outside_conventional(
    normal_force: float, troughing_angle: float, banking_angle: float
) -> float:
    """
    Calculate the weight force component acting on the outside wing roll - conventional method.

    This function implements the conventional methodology from Grimmer & Kessler (1987) Teil I
    for calculating the weight force component that acts on the outside wing roll
    of a troughed belt conveyor in a horizontal curve.

    Parameters
    ----------
    normal_force : float
        Normal force acting on the outside wing roll [N]
    troughing_angle : float
        Troughing angle of the belt [radians]
    banking_angle : float
        Banking angle of the belt in the horizontal curve [radians]

    Returns
    -------
    float
        Weight force component acting on the outside wing roll [N]

    Notes
    -----
    This implementation follows the conventional methodology from:
    Grimmer, K.-J. und F. Kessler: Teil I - Traditional calculation approaches.

    Mathematical formulation:
    F_outside = F_normal * tan(λ - β) * cos(λ)
    """
    return (
        normal_force
        * math.tan(troughing_angle - banking_angle)
        * math.cos(troughing_angle)
    )


def _weight_force_material_center_conventional(
    normal_force: float, banking_angle: float
) -> float:
    """
    Calculate the weight force component acting on the center wing roll - conventional method.

    This function implements the conventional methodology from Grimmer & Kessler (1987) Teil I
    for calculating the weight force component that acts on the center wing roll
    of a troughed belt conveyor in a horizontal curve.

    Parameters
    ----------
    normal_force : float
        Normal force acting on the center wing roll [N]
    banking_angle : float
        Banking angle of the belt in the horizontal curve [radians]

    Returns
    -------
    float
        Weight force component acting on the center wing roll [N]

    Notes
    -----
    This implementation follows the conventional methodology from:
    Grimmer, K.-J. und F. Kessler: Teil I - Traditional calculation approaches.

    Mathematical formulation:
    F_center = F_normal * tan(β)
    """
    return normal_force * math.tan(banking_angle)


def _weight_force_of_material_conventional(
    inside_force: float, center_force: float, outside_force: float
) -> float:
    """
    Calculate the total weight force acting on the material in the horizontal curve [N]

    This is the sum of the weight force components acting on the inside, outside, and center wing rolls.
    This function implements the conventional methodology from Grimmer & Kessler (1987) Teil I
    for calculating the weight force component that acts on the center wing roll
    of a troughed belt conveyor in a horizontal curve.

    Parameters
    ----------
    inside_force : float
        Weight force acting on the inside wing roll [N]
    center_force : float
        Weight force acting on the center wing roll [N]
    outside_force : float
        Weight force acting on the outside wing roll [N]

    Returns
    -------
    float
        Total weight force acting on the material in the horizontal curve [N]
    """
    return inside_force + center_force - outside_force


def _restraining_force_from_dead_weights_towards_outside_curve_conventional(
    total_force_from_belt: float, total_force_from_material: float
) -> float:
    """Calculate the restraining force from dead weights towards the outside curve [N].

    This function implements the methodology for calculating the restraining force
    that acts on the belt due to the dead weight of the material and the belt itself
    in a horizontal curve.

    Returns
    -------
    float
        Restraining force from dead weights towards the outside curve [N]
    """
    return total_force_from_belt + total_force_from_material


def _weight_force_material_inside_improved(
    normal_force: float, troughing_angle: float, banking_angle: float
) -> float:
    """
    Calculate the weight force component acting on the inside wing roll - improved method.

    This function implements the improved methodology from Grimmer & Kessler (1987) Teil I
    for calculating the weight force component that acts on the inside wing roll
    of a troughed belt conveyor in a horizontal curve.

    Parameters
    ----------
    normal_force : float
        Normal force acting on the inside wing roll [N]
    troughing_angle : float
        Troughing angle of the belt [radians]
    banking_angle : float
        Banking angle of the belt in the horizontal curve [radians]

    Returns
    -------
    float
        Weight force component acting on the inside wing roll [N]

    Notes
    -----
    This implementation follows the improved methodology from:
    Grimmer, K.-J. und F. Kessler: Teil II.

    Mathematical formulation:
    F_inside = F_normal * tan(λ + β)
    """
    return normal_force * math.tan(troughing_angle + banking_angle)


def _weight_force_material_outside_improved(
    normal_force: float, troughing_angle: float, banking_angle: float
) -> float:
    """
    Calculate the weight force component acting on the outside wing roll - improved method.

    This function implements the improved methodology from Grimmer & Kessler (1987) Teil II
    for calculating the weight force component that acts on the outside wing roll
    of a troughed belt conveyor in a horizontal curve.

    Parameters
    ----------
    normal_force : float
        Normal force acting on the outside wing roll [N]
    troughing_angle : float
        Troughing angle of the belt [radians]
    banking_angle : float
        Banking angle of the belt in the horizontal curve [radians]

    Returns
    -------
    float
        Weight force component acting on the outside wing roll [N]

    Notes
    -----
    This implementation follows the improved methodology from:
    Grimmer, K.-J. und F. Kessler: Teil II.

    Mathematical formulation:
    F_outside = F_normal * tan(λ - β)
    """
    return normal_force * math.tan(troughing_angle - banking_angle)


def _weight_force_material_center_improved(
    normal_force: float, banking_angle: float
) -> float:
    """
    Calculate the weight force component acting on the center wing roll - improved method.

    This function implements the improved methodology from Grimmer & Kessler (1987) Teil II
    for calculating the weight force component that acts on the center wing roll
    of a troughed belt conveyor in a horizontal curve.

    Parameters
    ----------
    normal_force : float
        Normal force acting on the center wing roll [N]
    banking_angle : float
        Banking angle of the belt in the horizontal curve [radians]

    Returns
    -------
    float
        Weight force component acting on the center wing roll [N]

    Notes
    -----
    This implementation follows the improved methodology from:
    Grimmer, K.-J. und F. Kessler: Teil II - Enhanced calculation procedures.

    Mathematical formulation:
    F_center = F_normal * tan(β)
    """
    return normal_force * math.tan(banking_angle)


def _weight_force_of_material_improved(
    inside_force: float, center_force: float, outside_force: float
) -> float:
    """
    Calculate the total weight force acting on the material in the horizontal curve [N]

    This is the sum of the weight force components acting on the inside, outside, and center wing rolls.
    This function implements the improved methodology from Grimmer & Kessler (1987) Teil II
    for calculating the weight force component that acts on the center wing roll
    of a troughed belt conveyor in a horizontal curve.

    Parameters
    ----------
    inside_force : float
        Weight force acting on the inside wing roll [N]
    center_force : float
        Weight force acting on the center wing roll [N]
    outside_force : float
        Weight force acting on the outside wing roll [N]

    Returns
    -------
    float
        Total weight force acting on the material in the horizontal curve [N]
    """
    return inside_force + center_force - outside_force


def _restraining_force_from_dead_weights_towards_outside_curve_improved(
    total_force_from_belt: float, total_force_from_material: float
) -> float:
    """Calculate the restraining force from dead weights towards the outside curve [N].

    This function implements the methodology for calculating the restraining force
    that acts on the belt due to the dead weight of the material and the belt itself
    in a horizontal curve.

    Returns
    -------
    float
        Restraining force from dead weights towards the outside curve [N]
    """
    return total_force_from_belt + total_force_from_material


# === IMPROVED METHODOLOGY IMPLEMENTATIONS ===
# Based on Grimmer & Kessler (1987) Teil II - Enhanced calculation procedures


def _weight_force_belt_inside_improved(
    total_weight_force_belt: float,
    inclination_angle: float,
    wing_roll_load_factor: float,  # normally: gt 1, lt 2
    belt_width: float,
    troughing_angle: float,
    banking_angle: float,
    belt_width_on_inside_wing_roll: float,
) -> float:
    """
    Calculate the weight force component acting on the inside wing roll - improved method.

    This function implements the improved methodology from Grimmer & Kessler (1987) Teil II
    with enhanced calculation procedures that improve upon the conventional approach.

    Parameters
    ----------
    total_weight_force_belt : float
        Total weight force acting on the belt (belt + material) [N]
    inclination_angle : float
        Inclination angle of the belt conveyor [radians]
    wing_roll_load_factor : float
        Load factor for the wing roll, typically between 1.0 and 2.0 [-]
        This factor depends on the troughing angle and belt troughability.
        Higher values indicate increased load concentration on the wing roll.
        Note: The exact value should be determined by appropriate calculation
        functions that consider troughing geometry and belt characteristics.
    belt_width : float
        Total width of the belt [m]
    troughing_angle : float
        Troughing angle of the belt [radians]
    banking_angle : float
        Banking angle of the belt in the horizontal curve [radians]
    belt_width_on_inside_wing_roll : float
        Effective width of the belt supported by the inside wing roll [m]

    Returns
    -------
    float
        Weight force component acting on the inside wing roll [N]

    Notes
    -----
    This implementation follows the improved methodology from:
    Grimmer, K.-J. und F. Kessler: Teil II - Enhanced calculation procedures.

    The wing_roll_load_factor accounts for the non-uniform load distribution
    that occurs in horizontal curves, where the inside wing roll experiences
    increased loading due to belt geometry and material flow effects.

    Raises
    ------
    ValueError
        If belt_width <= 0
    """
    if belt_width <= 0:
        raise ValueError(f"belt_width must be positive, got {belt_width}")
    return (
        total_weight_force_belt
        * math.cos(inclination_angle)
        * (
            wing_roll_load_factor
            * belt_width_on_inside_wing_roll
            / belt_width
            * math.sin(troughing_angle + banking_angle)
        )
    )


def _weight_force_belt_outside_improved(
    total_weight_force_belt: float,
    inclination_angle: float,
    wing_roll_load_factor: float,  # normally: gt 1, lt 2
    belt_width: float,
    troughing_angle: float,
    banking_angle: float,
    belt_width_on_outside_wing_roll: float,
) -> float:
    """
    Calculate the weight force component acting on the outside wing roll - improved method.

    This function implements the improved methodology from Grimmer & Kessler (1987) Teil II
    with enhanced calculation procedures that improve upon the conventional approach.

    Parameters
    ----------
    total_weight_force_belt : float
        Total weight force acting on the belt (belt + material) [N]
    inclination_angle : float
        Inclination angle of the belt conveyor [radians]
    belt_width : float
        Total width of the belt [m]
    troughing_angle : float
        Troughing angle of the belt [radians]
    banking_angle : float
        Banking angle of the belt in the horizontal curve [radians]
    belt_width_on_outside_wing_roll : float
        Effective width of the belt supported by the outside wing roll [m]

    Returns
    -------
    float
        Weight force component acting on the outside wing roll [N]

    Notes
    -----
    This implementation follows the improved methodology from:
    Grimmer, K.-J. und F. Kessler: Teil II - Enhanced calculation procedures.

    The improved method for the outside wing roll follows the same enhancement pattern
    as the inside wing roll but without the load factor since the outside roll typically
    experiences reduced loading in horizontal curves due to belt geometry effects.
    The enhancement removes the cos(troughing_angle) factor present in conventional method.

    Mathematical formulation:
    F_outside = F_total * cos(α) * (w_outside/w_total) * sin(λ - β)

    Raises
    ------
    ValueError
        If belt_width <= 0
    """
    if belt_width <= 0:
        raise ValueError(f"belt_width must be positive, got {belt_width}")
    return (
        total_weight_force_belt
        * math.cos(inclination_angle)
        * (
            wing_roll_load_factor
            * belt_width_on_outside_wing_roll
            / belt_width
            * math.sin(troughing_angle - banking_angle)
        )
    )


def _weight_force_belt_center_improved(
    total_weight_force_belt: float,
    inclination_angle: float,
    center_roll_load_factor: float,  # normally: lt 1, gt 0.5
    belt_width: float,
    banking_angle: float,
    belt_width_on_center_wing_roll: float,
) -> float:
    """
    Calculate the weight force component acting on the center section - improved method.

    This function implements the improved methodology from Grimmer & Kessler (1987) Teil II
    with enhanced calculation procedures that improve upon the conventional approach.

    Parameters
    ----------
    total_weight_force_belt : float
        Total weight force acting on the belt (belt + material) [N]
    inclination_angle : float
        Inclination angle of the belt conveyor [radians]
    belt_width : float
        Total width of the belt [m]
    banking_angle : float
        Banking angle of the belt in the horizontal curve [radians]
    belt_width_on_center_wing_roll : float
        Effective width of the belt supported by the center section [m]

    Returns
    -------
    float
        Weight force component acting on the center section [N]

    Notes
    -----
    This implementation follows the improved methodology from:
    Grimmer, K.-J. und F. Kessler: Teil II - Enhanced calculation procedures.

    For the center section, the improved method is identical to the conventional method
    since the center section is not affected by troughing angle considerations that
    impact the wing rolls. The center section responds primarily to banking angle effects.

    Mathematical formulation:
    F_center = F_total * cos(α) * (w_center/w_total) * sin(β)

    Raises
    ------
    ValueError
        If belt_width <= 0
    """
    if belt_width <= 0:
        raise ValueError(f"belt_width must be positive, got {belt_width}")
    return (
        total_weight_force_belt
        * math.cos(inclination_angle)
        * (
            center_roll_load_factor
            * belt_width_on_center_wing_roll
            / belt_width
            * math.sin(banking_angle)
        )
    )


def _weight_force_of_belt_improved(
    weight_force_belt_inside: float,
    weight_force_belt_center: float,
    weight_force_belt_outside: float,
) -> float:
    """
    Calculate the net lateral weight force acting on the belt - improved method.

    This function implements the improved methodology from Grimmer & Kessler (1987) Teil II
    for combining the weight force components with enhanced calculation procedures.

    Parameters
    ----------
    weight_force_belt_inside : float
        Weight force component on the inside wing roll [N]
    weight_force_belt_center : float
        Weight force component in the center section [N]
    weight_force_belt_outside : float
        Weight force component on the outside wing roll [N]

    Returns
    -------
    float
        Net lateral weight force acting on the belt [N]

    Notes
    -----
    This implementation follows the improved methodology from:
    Grimmer, K.-J. und F. Kessler: Teil II - Enhanced calculation procedures.

    The improved method uses the same combination formula as the conventional method,
    but operates on the improved individual component calculations which include
    enhanced wing roll load distribution and modified troughing angle considerations.

    Mathematical formulation:
    F_net = F_inside + F_center - F_outside

    The improvements come from the enhanced calculation of the individual components
    rather than changes to the combination logic itself.
    """
    return (
        weight_force_belt_inside + weight_force_belt_center - weight_force_belt_outside
    )


# === TILTED IDLER FRICTION FORCE CALCULATIONS ===
# Based on Grimmer & Kessler (1987) - Material force components on conveyed material


def _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
    force_component_inside: float,
    force_component_center: float,
    force_component_outside: float,
) -> float:
    """
    Calculate the restraining force from tilted idlers towards the outside curve - conventional method.

    This function implements the conventional methodology from Grimmer & Kessler (1987) Teil I
    for combining force components in a troughed belt conveyor operating in horizontal curves.
    The calculation represents the resultant restraining/guiding force that influences
    the material's behavior on tilted idlers.

    Parameters
    ----------
    force_component_inside : float
        Force component acting on the inside wing roll [N]
    force_component_center : float
        Force component acting in the center section [N]
    force_component_outside : float
        Force component acting on the outside wing roll [N]

    Returns
    -------
    float
        Restraining force from tilted idlers towards the outside curve [N]

    Notes
    -----
    This implementation follows the conventional methodology from:
    Grimmer, K.-J. und F. Kessler: Teil I - Traditional calculation approaches.

    The restraining force calculation combines the three force components using
    the standard force balance for horizontal curve analysis. This restraining force
    acts to guide the belt towards the outside of the curve when idler rolls are suitably tilted.

    Mathematical formulation:
    F_restraining = F_inside + F_center - F_outside

    Where:
    - F_inside is the inside wing roll force component
    - F_center is the center section force component
    - F_outside is the outside wing roll force component

    The subtraction of the outside component reflects the opposing nature of forces
    in horizontal curves, where inside and center forces work together while the
    outside force opposes the resultant lateral movement towards the outside curve.

    This function can be used to combine either material weight force components
    or tilted idler friction force components, as the mathematical combination
    is identical for both cases.
    """
    return force_component_inside + force_component_center - force_component_outside


def _tilted_idler_friction_force_inside_conventional(
    total_weight_force_material: float,
    inclination_angle: float,
    belt_width: float,
    troughing_angle: float,
    banking_angle: float,
    belt_width_on_inside_wing_roll: float,
    friction_variation: float,
    friction_coefficient_tilted_idler: float,
    normal_force_on_idler_roll: float,
) -> float:
    """
    Calculate the friction force from conveyed material acting on tilted idlers at the inside wing roll - conventional method.

    This function implements the friction force calculation for material-idler interaction
    at the inside wing roll position in troughed belt conveyors operating in horizontal curves.
    The calculation considers geometric factors, material distribution, and friction characteristics.

    Parameters
    ----------
    total_weight_force_material : float
        Total weight force of the conveyed material [N]
    inclination_angle : float
        Inclination angle of the belt conveyor [radians]
    belt_width : float
        Total width of the belt [m]
    troughing_angle : float
        Troughing angle of the belt [radians]
    banking_angle : float
        Banking angle of the belt in the horizontal curve [radians]
    belt_width_on_inside_wing_roll : float
        Effective width of the belt supported by the inside wing roll [m]
    friction_variation : float
        Friction variation factor [dimensionless]
    friction_coefficient_tilted_idler : float
        Friction coefficient for material-idler interaction [dimensionless]
    normal_force_on_idler_roll : float
        Additional normal force acting on the idler roll [N]

    Returns
    -------
    float
        Friction force component from material on inside wing roll tilted idlers [N]

    Notes
    -----
    This implementation calculates the friction force arising from the interaction between
    conveyed material and tilted idlers positioned at the inside wing roll of a troughed
    belt conveyor system operating in horizontal curves.

    Mathematical formulation:
    F = f_var * μ * cos(λ) * [(w_inside/w_total) * F_material * cos(λ + β) * cos(α) + F_normal]

    Where:
    - f_var is the friction variation factor
    - μ is the friction coefficient for tilted idler interaction
    - λ is the troughing angle
    - β is the banking angle
    - α is the inclination angle
    - w_inside/w_total is the width ratio
    - F_material is the total material weight force
    - F_normal is the additional normal force on the idler roll

    Raises
    ------
    ValueError
        If belt_width <= 0
    """
    if belt_width <= 0:
        raise ValueError(f"belt_width must be positive, got {belt_width}")
    return (
        friction_variation
        * friction_coefficient_tilted_idler
        * math.cos(troughing_angle)
        * (
            belt_width_on_inside_wing_roll
            / belt_width
            * total_weight_force_material
            * math.cos(troughing_angle + banking_angle)
            * math.cos(inclination_angle)
            + normal_force_on_idler_roll
        )
    )


def _tilted_idler_friction_force_outside_conventional(
    total_weight_force_material: float,
    inclination_angle: float,
    belt_width: float,
    troughing_angle: float,
    banking_angle: float,
    belt_width_on_outside_wing_roll: float,
    friction_variation: float,
    friction_coefficient_tilted_idler: float,
    normal_force_on_idler_roll: float,
) -> float:
    """
    Calculate the friction force from conveyed material acting on tilted idlers at the outside wing roll - conventional method.

    This function implements the friction force calculation for material-idler interaction
    at the outside wing roll position in troughed belt conveyors operating in horizontal curves.
    The calculation considers geometric factors, material distribution, and friction characteristics.

    Parameters
    ----------
    total_weight_force_material : float
        Total weight force of the conveyed material [N]
    inclination_angle : float
        Inclination angle of the belt conveyor [radians]
    belt_width : float
        Total width of the belt [m]
    troughing_angle : float
        Troughing angle of the belt [radians]
    banking_angle : float
        Banking angle of the belt in the horizontal curve [radians]
    belt_width_on_outside_wing_roll : float
        Effective width of the belt supported by the outside wing roll [m]
    friction_variation : float
        Friction variation factor [dimensionless]
    friction_coefficient_tilted_idler : float
        Friction coefficient for material-idler interaction [dimensionless]
    normal_force_on_idler_roll : float
        Additional normal force acting on the idler roll [N]

    Returns
    -------
    float
        Friction force component from material on outside wing roll tilted idlers [N]

    Notes
    -----
    This implementation calculates the friction force arising from the interaction between
    conveyed material and tilted idlers positioned at the outside wing roll of a troughed
    belt conveyor system operating in horizontal curves.

    Mathematical formulation:
    F = f_var * μ * cos(λ) * [(w_outside/w_total) * F_material * cos(λ - β) * cos(α) + F_normal]

    Where:
    - f_var is the friction variation factor
    - μ is the friction coefficient for tilted idler interaction
    - λ is the troughing angle
    - β is the banking angle
    - α is the inclination angle
    - w_outside/w_total is the width ratio
    - F_material is the total material weight force
    - F_normal is the additional normal force on the idler roll

    Raises
    ------
    ValueError
        If belt_width <= 0
    """
    if belt_width <= 0:
        raise ValueError(f"belt_width must be positive, got {belt_width}")
    return (
        friction_variation
        * friction_coefficient_tilted_idler
        * math.cos(troughing_angle)
        * (
            belt_width_on_outside_wing_roll
            / belt_width
            * total_weight_force_material
            * math.cos(troughing_angle - banking_angle)
            * math.cos(inclination_angle)
            + normal_force_on_idler_roll
        )
    )


def _tilted_idler_friction_force_center_conventional(
    total_weight_force_material: float,
    inclination_angle: float,
    belt_width: float,
    troughing_angle: float,
    banking_angle: float,
    belt_width_on_center_wing_roll: float,
    belt_width_on_inside_wing_roll: float,
    belt_width_on_outside_wing_roll: float,
    friction_variation: float,
    friction_coefficient_tilted_idler: float,
    normal_force_on_idler_roll: float,
) -> float:
    """
    Calculate the friction force from conveyed material acting on tilted idlers at the center section - conventional method.

    This function implements the friction force calculation for material-idler interaction
    at the center section in troughed belt conveyors operating in horizontal curves.
    The calculation considers combined effects from all three sections (center, inside, outside)
    since the center section is influenced by the entire belt geometry.

    Parameters
    ----------
    total_weight_force_material : float
        Total weight force of the conveyed material [N]
    inclination_angle : float
        Inclination angle of the belt conveyor [radians]
    belt_width : float
        Total width of the belt [m]
    troughing_angle : float
        Troughing angle of the belt [radians]
    banking_angle : float
        Banking angle of the belt in the horizontal curve [radians]
    belt_width_on_center_wing_roll : float
        Effective width of the belt supported by the center section [m]
    belt_width_on_inside_wing_roll : float
        Effective width of the belt supported by the inside wing roll [m]
    belt_width_on_outside_wing_roll : float
        Effective width of the belt supported by the outside wing roll [m]
    friction_variation : float
        Friction variation factor [dimensionless]
    friction_coefficient_tilted_idler : float
        Friction coefficient for material-idler interaction [dimensionless]
    normal_force_on_idler_roll : float
        Additional normal force acting on the idler roll [N]

    Returns
    -------
    float
        Friction force component from material on center section tilted idlers [N]

    Notes
    -----
    This implementation calculates the friction force arising from the interaction between
    conveyed material and tilted idlers positioned at the center section of a troughed
    belt conveyor system operating in horizontal curves.

    The center section calculation is unique as it combines three components:
    1. Center component: (w_center/w_total) * F_material * cos(β) * cos(α)
    2. Inside component: (w_inside/w_total) * F_material * sin(λ + β) * sin(λ) * cos(α)
    3. Outside component: (w_outside/w_total) * F_material * sin(λ - β) * sin(λ) * cos(α)

    Mathematical formulation:
    F = f_var * μ * (F_center + F_inside + F_outside + F_normal)

    Where:
    - f_var is the friction variation factor
    - μ is the friction coefficient for tilted idler interaction
    - λ is the troughing angle
    - β is the banking angle
    - α is the inclination angle
    - w_*/w_total are the width ratios for each section
    - F_material is the total material weight force
    - F_normal is the additional normal force on the idler roll

    Raises
    ------
    ValueError
        If belt_width <= 0
    """
    if belt_width <= 0:
        raise ValueError(f"belt_width must be positive, got {belt_width}")
    center = (
        belt_width_on_center_wing_roll
        / belt_width
        * total_weight_force_material
        * math.cos(banking_angle)
        * math.cos(inclination_angle)
    )

    inside = (
        belt_width_on_inside_wing_roll
        / belt_width
        * total_weight_force_material
        * math.sin(troughing_angle + banking_angle)
        * math.sin(troughing_angle)
        * math.cos(inclination_angle)
    )

    outside = (
        belt_width_on_outside_wing_roll
        / belt_width
        * total_weight_force_material
        * math.sin(troughing_angle - banking_angle)
        * math.sin(troughing_angle)
        * math.cos(inclination_angle)
    )

    force = (
        friction_variation
        * friction_coefficient_tilted_idler
        * (inside + center + outside + normal_force_on_idler_roll)
    )

    return force


def _tilted_idler_friction_force_inside_improved(
    total_weight_force_material: float,
    inclination_angle: float,
    wing_roll_load_factor: float,
    belt_width: float,
    troughing_angle: float,
    banking_angle: float,
    belt_width_on_inside_wing_roll: float,
    friction_variation: float,
    friction_coefficient_tilted_idler: float,
    normal_force_on_idler_roll: float,
) -> float:
    """
    Calculate the friction force from conveyed material acting on tilted idlers at the inside wing roll - improved method.

    This function implements the enhanced friction force calculation for material-idler interaction
    at the inside wing roll position in troughed belt conveyors operating in horizontal curves.
    The improved method incorporates load factors and refined geometric considerations for
    enhanced accuracy in force predictions.

    Parameters
    ----------
    total_weight_force_material : float
        Total weight force of the conveyed material [N]
    inclination_angle : float
        Inclination angle of the belt conveyor [radians]
    wing_roll_load_factor : float
        Load factor for wing roll considering improved load distribution [dimensionless]
    belt_width : float
        Total width of the belt [m]
    troughing_angle : float
        Troughing angle of the belt [radians]
    banking_angle : float
        Banking angle of the belt in the horizontal curve [radians]
    belt_width_on_inside_wing_roll : float
        Effective width of the belt supported by the inside wing roll [m]
    friction_variation : float
        Friction variation factor [dimensionless]
    friction_coefficient_tilted_idler : float
        Friction coefficient for material-idler interaction [dimensionless]
    normal_force_on_idler_roll : float
        Additional normal force acting on the idler roll [N]

    Returns
    -------
    float
        Friction force component from material on inside wing roll tilted idlers [N]

    Notes
    -----
    This improved implementation enhances the conventional method by incorporating load factors
    that better represent the actual load distribution in belt conveyor systems operating
    in horizontal curves. The method provides more accurate predictions for design calculations.

    Mathematical formulation:
    F = f_var * μ * [k_wing * (w_inside/w_total) * F_material * cos(λ + β) * cos(α) + F_normal]

    Where:
    - f_var is the friction variation factor
    - μ is the friction coefficient for tilted idler interaction
    - k_wing is the wing roll load factor (improved method enhancement)
    - λ is the troughing angle
    - β is the banking angle
    - α is the inclination angle
    - w_inside/w_total is the width ratio
    - F_material is the total material weight force
    - F_normal is the additional normal force on the idler roll

    The key improvement over the conventional method is the inclusion of the wing_roll_load_factor
    which accounts for actual load distribution patterns observed in operational conveyor systems.

    References
    ----------
    Enhanced methodology based on improved understanding of load distribution
    in troughed belt conveyors operating in horizontal curves.

    Raises
    ------
    ValueError
        If belt_width <= 0
    """
    if belt_width <= 0:
        raise ValueError(f"belt_width must be positive, got {belt_width}")
    return (
        friction_variation
        * friction_coefficient_tilted_idler
        * (
            wing_roll_load_factor
            * belt_width_on_inside_wing_roll
            / belt_width
            * total_weight_force_material
            * math.cos(troughing_angle + banking_angle)
            * math.cos(inclination_angle)
            + normal_force_on_idler_roll
        )
    )


def _tilted_idler_friction_force_outside_improved(
    total_weight_force_material: float,
    inclination_angle: float,
    wing_roll_load_factor: float,
    belt_width: float,
    troughing_angle: float,
    banking_angle: float,
    belt_width_on_outside_wing_roll: float,
    friction_variation: float,
    friction_coefficient_tilted_idler: float,
    normal_force_on_idler_roll: float,
) -> float:
    """
    Calculate the friction force from conveyed material acting on tilted idlers at the outside wing roll - improved method.

    This function implements the enhanced friction force calculation for material-idler interaction
    at the outside wing roll position in troughed belt conveyors operating in horizontal curves.
    The improved method incorporates load factors and refined geometric considerations for
    enhanced accuracy in force predictions.

    Parameters
    ----------
    total_weight_force_material : float
        Total weight force of the conveyed material [N]
    inclination_angle : float
        Inclination angle of the belt conveyor [radians]
    wing_roll_load_factor : float
        Load factor for wing roll considering improved load distribution [dimensionless]
    belt_width : float
        Total width of the belt [m]
    troughing_angle : float
        Troughing angle of the belt [radians]
    banking_angle : float
        Banking angle of the belt in the horizontal curve [radians]
    belt_width_on_outside_wing_roll : float
        Effective width of the belt supported by the outside wing roll [m]
    friction_variation : float
        Friction variation factor [dimensionless]
    friction_coefficient_tilted_idler : float
        Friction coefficient for material-idler interaction [dimensionless]
    normal_force_on_idler_roll : float
        Additional normal force acting on the idler roll [N]

    Returns
    -------
    float
        Friction force component from material on outside wing roll tilted idlers [N]

    Notes
    -----
    This improved implementation enhances the conventional method by incorporating load factors
    that better represent the actual load distribution in belt conveyor systems operating
    in horizontal curves. The method provides more accurate predictions for design calculations.

    Mathematical formulation:
    F = f_var * μ * cos(λ) * [k_wing * (w_outside/w_total) * F_material * cos(λ - β) * cos(α) + F_normal]

    Where:
    - f_var is the friction variation factor
    - μ is the friction coefficient for tilted idler interaction
    - k_wing is the wing roll load factor (improved method enhancement)
    - λ is the troughing angle
    - β is the banking angle
    - α is the inclination angle
    - w_outside/w_total is the width ratio
    - F_material is the total material weight force
    - F_normal is the additional normal force on the idler roll

    The key improvement over the conventional method is the inclusion of the wing_roll_load_factor
    which accounts for actual load distribution patterns observed in operational conveyor systems.

    References
    ----------
    Enhanced methodology based on improved understanding of load distribution
    in troughed belt conveyors operating in horizontal curves.

    Raises
    ------
    ValueError
        If belt_width <= 0
    """
    if belt_width <= 0:
        raise ValueError(f"belt_width must be positive, got {belt_width}")
    return (
        friction_variation
        * friction_coefficient_tilted_idler
        * (
            wing_roll_load_factor
            * belt_width_on_outside_wing_roll
            / belt_width
            * total_weight_force_material
            * math.cos(troughing_angle - banking_angle)
            * math.cos(inclination_angle)
            + normal_force_on_idler_roll
        )
    )


def _tilted_idler_friction_force_center_improved(
    total_weight_force_material: float,
    inclination_angle: float,
    center_roll_load_factor: float,
    belt_width: float,
    troughing_angle: float,
    banking_angle: float,
    belt_width_on_center_wing_roll: float,
    belt_width_on_inside_wing_roll: float,
    belt_width_on_outside_wing_roll: float,
    friction_variation: float,
    friction_coefficient_tilted_idler: float,
    normal_force_on_idler_roll: float,
) -> float:
    """
    Calculate the friction force from conveyed material acting on tilted idlers at the center roll - improved method.

    This function implements the enhanced friction force calculation for material-idler interaction
    at the center roll position in troughed belt conveyors operating in horizontal curves.
    The improved method incorporates load factors and refined geometric considerations for
    enhanced accuracy in force predictions.

    Parameters
    ----------
    total_weight_force_material : float
        Total weight force of the conveyed material [N]
    inclination_angle : float
        Inclination angle of the belt conveyor [radians]
    center_roll_load_factor : float
        Load factor for center roll considering improved load distribution [dimensionless]
    belt_width : float
        Total width of the belt [m]
    troughing_angle : float
        Troughing angle of the belt [radians]
    banking_angle : float
        Banking angle of the belt in the horizontal curve [radians]
    belt_width_on_center_wing_roll : float
        Effective width of the belt supported by the center wing roll [m]
    belt_width_on_inside_wing_roll : float
        Effective width of the belt supported by the inside wing roll [m]
    belt_width_on_outside_wing_roll : float
        Effective width of the belt supported by the outside wing roll [m]
    friction_variation : float
        Friction variation factor [dimensionless]
    friction_coefficient_tilted_idler : float
        Friction coefficient for material-idler interaction [dimensionless]
    normal_force_on_idler_roll : float
        Additional normal force acting on the idler roll [N]

    Returns
    -------
    float
        Friction force component from material on center roll tilted idlers [N]

    Notes
    -----
    This improved implementation enhances the conventional method by incorporating load factors
    that better represent the actual load distribution in belt conveyor systems operating
    in horizontal curves. The method provides more accurate predictions for design calculations.

    Mathematical formulation:
    F = f_var * μ * [k_center * (w_center/w_total * F_material * cos(β) * cos(α)
        + w_inside/w_total * F_material * sin(λ + β) * sin(λ) * cos(α)
        + w_outside/w_total * F_material * sin(λ - β) * sin(λ) * cos(α)) + F_normal]

    Where:
    - f_var is the friction variation factor
    - μ is the friction coefficient for tilted idler interaction
    - k_center is the center roll load factor (improved method enhancement)
    - λ is the troughing angle
    - β is the banking angle
    - α is the inclination angle
    - w_center/w_total, w_inside/w_total, w_outside/w_total are the width ratios
    - F_material is the total material weight force
    - F_normal is the additional normal force on the idler roll

    The key improvement over the conventional method is the inclusion of the center_roll_load_factor
    which accounts for actual load distribution patterns observed in operational conveyor systems.

    References
    ----------
    Enhanced methodology based on improved understanding of load distribution
    in troughed belt conveyors operating in horizontal curves.

    Raises
    ------
    ValueError
        If belt_width <= 0
    """
    if belt_width <= 0:
        raise ValueError(f"belt_width must be positive, got {belt_width}")
    center = (
        center_roll_load_factor
        * belt_width_on_center_wing_roll
        / belt_width
        * total_weight_force_material
        * math.cos(banking_angle)
        * math.cos(inclination_angle)
    )

    inside = (
        center_roll_load_factor
        * belt_width_on_inside_wing_roll
        / belt_width
        * total_weight_force_material
        * math.sin(troughing_angle + banking_angle)
        * math.sin(troughing_angle)
        * math.cos(inclination_angle)
    )

    outside = (
        center_roll_load_factor
        * belt_width_on_outside_wing_roll
        / belt_width
        * total_weight_force_material
        * math.sin(troughing_angle - banking_angle)
        * math.sin(troughing_angle)
        * math.cos(inclination_angle)
    )

    force = (
        friction_variation
        * friction_coefficient_tilted_idler
        * (inside + center + outside + normal_force_on_idler_roll)
    )

    return force


def _restraining_force_from_tilted_idlers_towards_outside_curve_improved(
    force_component_inside: float,
    force_component_center: float,
    force_component_outside: float,
) -> float:
    """
    Calculate the restraining force from tilted idlers towards the outside curve - improved method.

    This function implements the improved methodology from Grimmer & Kessler (1987) Teil II
    for combining force components in a troughed belt conveyor operating in horizontal curves.
    The calculation represents the resultant restraining/guiding force that influences
    the material's behavior on tilted idlers using enhanced load distribution factors.

    Parameters
    ----------
    force_component_inside : float
        Force component acting on the inside wing roll from improved calculation [N]
    force_component_center : float
        Force component acting in the center section from improved calculation [N]
    force_component_outside : float
        Force component acting on the outside wing roll from improved calculation [N]

    Returns
    -------
    float
        Restraining force from tilted idlers towards the outside curve using improved methodology [N]

    Notes
    -----
    This implementation follows the improved methodology from:
    Grimmer, K.-J. und F. Kessler: Teil II - Enhanced calculation procedures.

    The improved method uses the same combination formula as the conventional method,
    but operates on enhanced individual component calculations that include improved
    load distribution factors and refined geometric considerations.

    Mathematical formulation:
    F_restraining = F_inside + F_center - F_outside

    Where:
    - F_inside is the enhanced inside wing roll force component
    - F_center is the enhanced center section force component
    - F_outside is the enhanced outside wing roll force component

    The improvements come from the enhanced calculation of the individual components
    rather than changes to the combination logic itself. Each component incorporates
    load factors that better represent actual load distribution patterns observed
    in operational conveyor systems.

    This function can be used to combine either material weight force components
    or tilted idler friction force components, as the mathematical combination
    is identical for both cases.

    References
    ----------
    Enhanced methodology based on improved understanding of load distribution
    in troughed belt conveyors operating in horizontal curves.
    """
    return force_component_inside + force_component_center - force_component_outside
