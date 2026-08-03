"""Validation helpers for the Eytelwein main module.

This module provides centralized validation utilities used across multiple
domains of the Eytelwein package.
"""


def validate_positive_count(count: int, param_name: str = "count") -> None:
    """
    Validate that a discrete configuration count is a positive integer.

    This centralized helper is used for parameters like strand_count and
    quantity_of_drives that represent discrete configuration counts,
    which must be plain int (not Quantity) values.

    Parameters
    ----------
    count : int
        The count value to validate.
    param_name : str, optional
        Name of the parameter for error messages (default: "count").

    Raises
    ------
    ValueError
        If count is a bool (which is a subclass of int in Python).
    ValueError
        If count is not an integer type.
    ValueError
        If count is not >= 1.

    Notes
    -----
    Discrete configuration counts (e.g., strand_count, quantity_of_drives)
    represent architectural choices in reeving or drive design and are always
    plain integers, never Quantity objects. This is intentional: while measured
    values and dimensionless ratios use Quantity, configuration counts reflect
    the logical structure of the system, not measurements with units.
    """
    # Explicitly reject bool (which is a subclass of int in Python)
    if isinstance(count, bool):
        raise ValueError(
            f"{param_name} must be an integer, got {type(count).__name__}."
        )
    if not isinstance(count, int):
        raise ValueError(
            f"{param_name} must be an integer, got {type(count).__name__}."
        )
    if count <= 0:
        raise ValueError(f"{param_name} must be a positive integer >= 1, got {count}.")
