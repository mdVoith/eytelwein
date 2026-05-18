"""Feature example E: change output precision.

Run from repository root:
    python examples/features/e_output_precision_control.py
"""

from eytelwein.belt_conveyor_design import minimum_belt_tension_from_sag_carry
from eytelwein.main.units import get_unit_registry


u = get_unit_registry()


def main() -> None:
    line_load_belt = 18.0 * u.kilogram / u.meter
    line_load_material = 62.0 * u.kilogram / u.meter
    idler_spacing = 1.2 * u.meter
    allowable_sag = 0.01 * u.dimensionless

    tension_default = minimum_belt_tension_from_sag_carry(
        line_load_belt=line_load_belt,
        line_load_material=line_load_material,
        idler_spacing=idler_spacing,
        allowable_sag=allowable_sag,
        unit="kilonewton",
    )
    tension_precision_2 = minimum_belt_tension_from_sag_carry(
        line_load_belt=line_load_belt,
        line_load_material=line_load_material,
        idler_spacing=idler_spacing,
        allowable_sag=allowable_sag,
        unit="kilonewton",
        precision=2,
    )
    tension_unrounded = minimum_belt_tension_from_sag_carry(
        line_load_belt=line_load_belt,
        line_load_material=line_load_material,
        idler_spacing=idler_spacing,
        allowable_sag=allowable_sag,
        unit="kilonewton",
        precision=None,
    )

    print("Feature E - Output precision control")
    print(f"Default precision (5): {tension_default:~P}")
    print(f"Custom precision (2):  {tension_precision_2:~P}")
    print(f"No rounding:           {tension_unrounded:~P}")


if __name__ == "__main__":
    main()
