"""Feature example A: change output units for minimum belt tension.

Run from repository root:
    python examples/features/a_output_unit_minimum_tension.py
"""

from eytelwein.belt_conveyor_design import minimum_belt_tension_from_sag_carry
from eytelwein.main.units import get_unit_registry


u = get_unit_registry()


def main() -> None:
    line_load_belt = 18.0 * u.kilogram / u.meter
    line_load_material = 62.0 * u.kilogram / u.meter
    idler_spacing = 1.2 * u.meter
    allowable_sag = 0.01 * u.dimensionless

    tension_n = minimum_belt_tension_from_sag_carry(
        line_load_belt=line_load_belt,
        line_load_material=line_load_material,
        idler_spacing=idler_spacing,
        allowable_sag=allowable_sag,
        unit="newton",
    )
    tension_kn = minimum_belt_tension_from_sag_carry(
        line_load_belt=line_load_belt,
        line_load_material=line_load_material,
        idler_spacing=idler_spacing,
        allowable_sag=allowable_sag,
        unit="kilonewton",
    )

    print("Feature A - Output unit selection")
    print(f"Minimum belt tension in N:  {tension_n:~P}")
    print(f"Minimum belt tension in kN: {tension_kn:~P}")


if __name__ == "__main__":
    main()
