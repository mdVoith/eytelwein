def _belt_safety_factor_from_splice_strength_and_belt_tension(
    splice_strength_n_per_mm: float,
    belt_tension_n_per_mm: float,
) -> float:
    """Calculate belt safety factor from splice strength and belt tension.

    Formula:
        S = T_N / T
    """
    if belt_tension_n_per_mm <= 0:
        raise ValueError(
            "belt_tension_n_per_mm must be positive to avoid division by zero"
        )

    return splice_strength_n_per_mm / belt_tension_n_per_mm


def _rating_tension_from_belt_safety_factor_and_belt_tension(
    belt_safety_factor: float,
    belt_tension_n_per_mm: float,
) -> float:
    """Calculate rating tension from belt safety factor and belt tension.

    Formula:
        T_N = S * T
    """
    return belt_safety_factor * belt_tension_n_per_mm


def _belt_tension_fromsplice_strength_and_belt_safety_factor(
    splice_strength_n_per_mm: float,
    belt_safety_factor: float,
) -> float:
    """Calculate belt tension from splice strength and belt safety factor.

    Formula:
        T = T_N / S
    """
    if belt_safety_factor <= 0:
        raise ValueError(
            "belt_safety_factor must be positive to avoid division by zero"
        )

    return splice_strength_n_per_mm / belt_safety_factor
