def _motion_resistance_from_torque(torque: float, pulley_diameter: float) -> float:
    """
    Calculate the motion resistance from the torque and pulley diameter.

    Parameters
    ----------
    torque : float
        The torque.
    pulley_diameter : float
        The pulley diameter.

    Returns
    -------
    float
        The motion resistance.

    Raises
    ------
    ValueError
        If pulley_diameter is zero or negative.
    """
    if pulley_diameter <= 0:
        raise ValueError("pulley_diameter must be positive")
    return 2 * torque / pulley_diameter
