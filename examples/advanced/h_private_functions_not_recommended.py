"""Advanced example: direct private-function usage (not recommended).

Run from repository root:
    python examples/advanced/h_private_functions_not_recommended.py

This script demonstrates the tradeoffs of calling private helpers directly.
"""

import math

from eytelwein.belt_conveyor_design import (
    cross_section_of_fill,
    minimum_belt_tension_from_sag_carry,
    usable_belt_width,
)
from eytelwein.belt_conveyor_design.core._belt_tensions_and_takeup_forces import (
    _minimum_belt_tension_from_sag_carry,
)
from eytelwein.belt_conveyor_design.core._volume_flow_mass_flow import (
    _cross_section_of_fill,
)
from eytelwein.main.units import get_unit_registry


u = get_unit_registry()


def main() -> None:
    print("Advanced example - Private functions (not recommended)")
    print("Warnings:")
    print("- advanced")
    print("- unstable API surface")
    print("- no unit safety")
    print("- no backwards-compatibility promise")

    # Same physical inputs for public and private cross-section calculation.
    belt_width = 1200 * u.millimeter
    center_roll_length = 450 * u.millimeter
    troughing_angle = 35 * u.degree
    equivalent_slope_angle = 15 * u.degree

    used_width = usable_belt_width(belt_width)
    area_public = cross_section_of_fill(
        center_roll_length=center_roll_length,
        usable_belt_width=used_width,
        troughing_angle=troughing_angle,
        equivalent_slope_angle=equivalent_slope_angle,
        unit="meter**2",
        precision=None,
    )

    area_private_correct_mm2 = _cross_section_of_fill(
        center_roll_length.to(u.millimeter).magnitude,
        used_width.to(u.millimeter).magnitude,
        math.radians(troughing_angle.to(u.degree).magnitude),
        math.radians(equivalent_slope_angle.to(u.degree).magnitude),
    )
    area_private_correct = (area_private_correct_mm2 * u.millimeter**2).to(u.meter**2)

    # Deliberate misuse: private helper expects radians, but degrees are passed.
    area_private_wrong_mm2 = _cross_section_of_fill(
        center_roll_length.to(u.millimeter).magnitude,
        used_width.to(u.millimeter).magnitude,
        troughing_angle.to(u.degree).magnitude,
        equivalent_slope_angle.to(u.degree).magnitude,
    )
    area_private_wrong = (area_private_wrong_mm2 * u.millimeter**2).to(u.meter**2)

    print("\nPublic vs private (same intended inputs):")
    print(f"- Public API result:              {area_public:~P}")
    print(f"- Private API (correct radians):  {area_private_correct:~P}")
    print(f"- Private API (wrong degrees):    {area_private_wrong:~P}")

    delta = (area_private_correct - area_public).to(u.meter**2)
    print(f"- Public/private delta (correct): {delta:~P}")

    print("\nAllowable sag input formats:")
    tension_sag_fraction = minimum_belt_tension_from_sag_carry(
        line_load_belt=18.0 * u.kilogram / u.meter,
        line_load_material=62.0 * u.kilogram / u.meter,
        idler_spacing=1.2 * u.meter,
        allowable_sag=0.01 * u.dimensionless,
        unit="kilonewton",
        precision=None,
    )
    tension_sag_percent = minimum_belt_tension_from_sag_carry(
        line_load_belt=18.0 * u.kilogram / u.meter,
        line_load_material=62.0 * u.kilogram / u.meter,
        idler_spacing=1.2 * u.meter,
        allowable_sag=1.0 * u.percent,
        unit="kilonewton",
        precision=None,
    )
    sag_delta = (tension_sag_percent - tension_sag_fraction).to(u.kilonewton)
    print(f"- Sag as 0.01 (dimensionless): {tension_sag_fraction:~P}")
    print(f"- Sag as 1 % (percent):        {tension_sag_percent:~P}")
    print(f"- Difference:                  {sag_delta:~P}")

    print("\nValidation contrast (negative idler spacing):")
    try:
        minimum_belt_tension_from_sag_carry(
            line_load_belt=18.0 * u.kilogram / u.meter,
            line_load_material=62.0 * u.kilogram / u.meter,
            idler_spacing=-1.2 * u.meter,
            allowable_sag=0.01 * u.dimensionless,
            unit="kilonewton",
            precision=None,
        )
    except ValueError as exc:
        print(f"- Public API catches invalid input: {exc}")

    private_invalid = _minimum_belt_tension_from_sag_carry(
        line_load_belt_kg_per_m=18.0,
        line_load_material_kg_per_m=62.0,
        idler_spacing_m=-1.2,
        allowable_sag=0.01,
    )
    print(
        "- Private API returns a value for invalid input: "
        f"{(private_invalid * u.newton).to(u.kilonewton):~P}"
    )


if __name__ == "__main__":
    main()
