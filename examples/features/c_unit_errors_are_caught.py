"""Feature example C: dimensional unit errors are caught.

Run from repository root:
    python examples/features/c_unit_errors_are_caught.py
"""

from eytelwein.belt_conveyor_design import minimum_belt_tension_from_sag_carry
from eytelwein.main.units import get_unit_registry


u = get_unit_registry()


def main() -> None:
    print("Feature C - Unit errors are caught")
    try:
        # Intentional unit mistake: line_load_belt should be mass/length (kg/m), not mass (kg).
        minimum_belt_tension_from_sag_carry(
            line_load_belt=18.0 * u.kilogram,
            line_load_material=62.0 * u.kilogram / u.meter,
            idler_spacing=1.2 * u.meter,
            allowable_sag=0.01 * u.dimensionless,
            unit="kilonewton",
        )
    except ValueError as exc:
        print("Caught expected ValueError:")
        print(exc)


if __name__ == "__main__":
    main()
