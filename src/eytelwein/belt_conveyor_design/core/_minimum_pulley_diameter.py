import importlib.resources

from eytelwein.belt_conveyor_design.constants import PulleyLoadFactor


def _minimum_diameter_of_group_A_pulleys(
    minimum_pulley_diameter_coefficient: int, tension_member_thickness: float
) -> float:
    """
    Calculate the minimum diameter of a group A pulley.

    Parameters
    ----------
    minimum_pulley_diameter_coefficient : int
        The minimum pulley diameter coefficient.
        B (cotton): 80
        P (polyamide): 90
        E (polyester): 108
        St (steel cords): 145
    tension_member_thickness : float
        The thickness of the load-bearing longitudinal tension member (without outer warp layer or weft,
        for example) in millimeters.

    Returns
    -------
    float
        The minimum diameter of a group A pulley in millimeters.
    """
    return minimum_pulley_diameter_coefficient * tension_member_thickness


def _pulley_load_factor(
    max_width_related_belt_tension_at_pulleys: float,
    nominal_belt_breaking_strength: float,
) -> float:
    """
    Calculate the pulley load factor.

    Parameters
    ----------
    max_width_related_belt_tension_at_pulleys : float
        The mean width-related tension at the point of maximum belt tension in the zone of Group A pulleys in the steady operating condition..
    nominal_belt_breaking_strength : float
        The nominal belt breaking strength.

    Returns
    -------
    float
        The pulley load factor as a percentage.
    """
    pulley_load_factor = (
        max_width_related_belt_tension_at_pulleys
        / nominal_belt_breaking_strength
        * 8
        * 100
    )
    return pulley_load_factor


def _minimum_diameter_of_group_A_B_C_pulleys(
    minimum_diameter_of_group_A_pulleys: int, pulley_load_factor: PulleyLoadFactor
) -> dict[str, int | None]:
    """
    Calculate the minimum diameters of group A, B, and C pulleys.
    Data is loaded from a lookup CSV shipped with the library.
    """
    minimum_diameters: dict[str, int | None] = {"A": None, "B": None, "C": None}

    # Use importlib.resources to open the CSV file from the package
    with importlib.resources.open_text(
        "eytelwein.belt_conveyor_design.data", "minimum_pulley_diameters.csv"
    ) as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(";")
            if parts[0] == str(minimum_diameter_of_group_A_pulleys) and parts[1] == str(
                pulley_load_factor
            ):
                if parts[2] == "A":
                    minimum_diameters["A"] = int(parts[3])
                elif parts[2] == "B":
                    minimum_diameters["B"] = int(parts[3])
                elif parts[2] == "C":
                    minimum_diameters["C"] = int(parts[3])
            if all(minimum_diameters.values()):
                break

    return minimum_diameters


def _get_max_width_related_tension_at_group_A_pulleys(
    nominal_belt_strength: int,
    pulley_load_factor: PulleyLoadFactor = PulleyLoadFactor.above_60_up_to_100,
) -> float:
    """
    Calculate the maximum width-related tension at the point of maximum belt tension in the zone of Group A pulleys.

    Parameters:
    pulley_load_factor (PulleyLoadFactor): The pulley load factor.
    nominal_belt_strength (int): The nominal belt strength in kilonewton.

    Returns:
    float: The maximum width-related tension at the point of maximum belt tension in the zone of Group A pulleys.
    """
    return pulley_load_factor.get_max_value() / 100 * nominal_belt_strength / 8
