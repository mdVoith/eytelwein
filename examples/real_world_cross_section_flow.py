"""Real-world throughput example using Eytelwein.

This script demonstrates a compact engineering workflow with hard-coded values:
1) derive usable belt width,
2) compute loaded cross-section,
3) convert to volume and mass flow,
4) run an inverse check for required usable width.

Run from repository root:
    python examples/real_world_cross_section_flow.py
"""

from eytelwein.belt_conveyor_design import (
    cross_section_of_fill,
    mass_flow_from_volume_flow_density,
    solve_for_used_belt_width_from_cross_section,
    usable_belt_width,
    volume_flow_from_cross_section_speed,
)
from eytelwein.main.units import get_unit_registry


u = get_unit_registry()


def _print_row(label: str, value: str) -> None:
    print(f"{label:<42} {value}")


def main() -> None:
    # Hard-coded reference inputs for a typical bulk-material conveyor case.
    belt_width = 1200 * u.millimeter
    center_roll_length = 450 * u.millimeter
    troughing_angle = 35 * u.degree
    equivalent_slope_angle = 15 * u.degree
    belt_speed = 3.2 * u.meter / u.second
    bulk_density = 850 * u.kilogram / u.meter**3

    usable_width = usable_belt_width(belt_width)
    filled_cross_section = cross_section_of_fill(
        center_roll_length=center_roll_length,
        usable_belt_width=usable_width,
        troughing_angle=troughing_angle,
        equivalent_slope_angle=equivalent_slope_angle,
        unit="meter**2",
    )
    volume_flow = volume_flow_from_cross_section_speed(
        cross_section_of_fill=filled_cross_section,
        belt_speed=belt_speed,
        unit="meter**3/hour",
    )
    mass_flow = mass_flow_from_volume_flow_density(
        volume_flow=volume_flow,
        bulk_density=bulk_density,
        unit="tonne/hour",
    )

    required_usable_width = solve_for_used_belt_width_from_cross_section(
        target_cross_section=filled_cross_section,
        center_roll_length=center_roll_length,
        troughing_angle=troughing_angle,
        equivalent_slope_angle=equivalent_slope_angle,
        unit="millimeter",
    )

    print("=" * 78)
    print("Eytelwein Real-World Example: Cross-Section to Throughput")
    print("=" * 78)
    print("Inputs")
    _print_row("Belt width", f"{belt_width:~P}")
    _print_row("Center roll length", f"{center_roll_length:~P}")
    _print_row("Troughing angle", f"{troughing_angle:~P}")
    _print_row("Equivalent slope angle", f"{equivalent_slope_angle:~P}")
    _print_row("Belt speed", f"{belt_speed:~P}")
    _print_row("Bulk density", f"{bulk_density:~P}")

    print("\nResults")
    _print_row("Usable belt width", f"{usable_width:~P}")
    _print_row("Cross-section of fill", f"{filled_cross_section:~P}")
    _print_row("Volume flow", f"{volume_flow:~P}")
    _print_row("Mass flow", f"{mass_flow:~P}")
    _print_row("Inverse check: required usable width", f"{required_usable_width:~P}")
    print("=" * 78)


if __name__ == "__main__":
    main()
