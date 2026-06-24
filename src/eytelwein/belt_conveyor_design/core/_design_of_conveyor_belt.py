def _belt_safety_factor_fromsplice_strength_and_belt_tension(
    splice_strength_n_per_mm: float,
    belt_tension_n_per_mm: float,
) -> float:
    """Calculate belt safety factor from splice strength and belt tension.

    Formula:
            S = k_N / k
    """
    if belt_tension_n_per_mm <= 0:
        raise ValueError(
            "belt_tension_n_per_mm must be positive to avoid division by zero"
        )

    return splice_strength_n_per_mm / belt_tension_n_per_mm


def _splice_strength_from_belt_safety_factor_and_belt_tension(
    belt_safety_factor: float,
    belt_tension_n_per_mm: float,
) -> float:
    """Calculate splice strength from belt safety factor and belt tension.

    Formula:
            k_N = S * k
    """
    return belt_safety_factor * belt_tension_n_per_mm


def _belt_tension_fromsplice_strength_and_belt_safety_factor(
    splice_strength_n_per_mm: float,
    belt_safety_factor: float,
) -> float:
    """Calculate belt tension from splice strength and belt safety factor.

    Formula:
            k = k_N / S
    """
    if belt_safety_factor <= 0:
        raise ValueError(
            "belt_safety_factor must be positive to avoid division by zero"
        )

    return splice_strength_n_per_mm / belt_safety_factor
