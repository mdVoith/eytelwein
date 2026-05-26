"""Feature example D: physically invalid inputs are rejected.

Run from repository root:
    python examples/features/d_physically_invalid_inputs_are_caught.py
"""

from eytelwein.belt_conveyor_design import minimum_belt_tension_from_sag_carry
from eytelwein.main.units import get_unit_registry


u = get_unit_registry()


def main() -> None:
    print("Feature D - Physically invalid calculations are caught")
    try:
        # Intentional physics violation: negative idler spacing is not physically meaningful.
        minimum_belt_tension_from_sag_carry(
            line_load_belt=18.0 * u.kilogram / u.meter,
            line_load_material=62.0 * u.kilogram / u.meter,
            idler_spacing=-1.2 * u.meter,
            allowable_sag=0.01 * u.dimensionless,
            unit="kilonewton",
        )
    except ValueError as exc:
        print("Caught expected ValueError:")
        print(exc)


if __name__ == "__main__":
    main()
