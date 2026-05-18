"""Feature example B: imperial inputs with imperial and SI outputs.

Run from repository root:
    python examples/features/b_imperial_input_dual_output.py
"""

from eytelwein.belt_conveyor_design import volume_flow_from_cross_section_speed
from eytelwein.main.units import get_unit_registry


u = get_unit_registry()


def main() -> None:
    # Same imperial inputs for both calls.
    cross_section = 6.0 * u.foot**2
    belt_speed = 500.0 * u.foot / u.minute

    flow_imperial = volume_flow_from_cross_section_speed(
        cross_section_of_fill=cross_section,
        belt_speed=belt_speed,
        unit="foot**3/hour",
    )
    flow_si = volume_flow_from_cross_section_speed(
        cross_section_of_fill=cross_section,
        belt_speed=belt_speed,
        unit="meter**3/hour",
    )

    print("Feature B - Imperial input, dual output systems")
    print(f"Inputs: cross_section={cross_section:~P}, belt_speed={belt_speed:~P}")
    print(f"Output in imperial units: {flow_imperial:~P}")
    print(f"Output in SI units:       {flow_si:~P}")


if __name__ == "__main__":
    main()
