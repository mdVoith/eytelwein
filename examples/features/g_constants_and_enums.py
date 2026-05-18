"""Feature example G: enums and constants from the public API.

Run from repository root:
    python examples/features/g_constants_and_enums.py
"""

from eytelwein.belt_conveyor_design import IdlerSets
from eytelwein.idler_design import (
    load_factor_determining_idler_roll_load_due_to_conveyor_belt,
    load_factor_determining_idler_roll_load_due_to_material,
)
from eytelwein.main.constants import PI, STANDARD_GRAVITY
from eytelwein.main.units import get_unit_registry


u = get_unit_registry()


def main() -> None:
    print("Feature G - Public enums and constants")

    print("\nAvailable IdlerSets members:")
    for member in IdlerSets:
        print(f"- {member.name} -> {member.value}")

    arrangement = IdlerSets.THREE_TROUGH
    troughing_angle = 35 * u.degree
    center_roll_length = 450 * u.millimeter
    belt_width = 1200 * u.millimeter

    f_material = load_factor_determining_idler_roll_load_due_to_material(
        idler_roll_arrangement=arrangement,
        troughing_angle=troughing_angle,
    )
    f_belt = load_factor_determining_idler_roll_load_due_to_conveyor_belt(
        idler_roll_arrangement=arrangement,
        idler_roll_length_center=center_roll_length,
        belt_width=belt_width,
    )

    print("\nIdler load factors using IdlerSets.THREE_TROUGH:")
    print(f"- Material load factor: {f_material:~P}")
    print(f"- Belt load factor:     {f_belt:~P}")

    # Use shared constants in lightweight engineering checks.
    line_load_mass = 55 * u.kilogram / u.meter
    line_load_weight = line_load_mass * STANDARD_GRAVITY

    pulley_radius = 0.25 * u.meter
    half_wrap_length = (PI * pulley_radius).to(u.meter)

    print("\nUsing shared constants:")
    print(f"- STANDARD_GRAVITY: {STANDARD_GRAVITY:~P}")
    print(f"- Weight line load from 55 kg/m: {line_load_weight.to(u.newton / u.meter):~P}")
    print(f"- Half-wrap length for r=0.25 m (pi*r): {half_wrap_length:~P}")


if __name__ == "__main__":
    main()
