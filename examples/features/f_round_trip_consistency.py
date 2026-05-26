"""Feature example F: forward/inverse round-trip consistency checks.

Run from repository root:
    python examples/features/f_round_trip_consistency.py
"""

from eytelwein.belt_conveyor_design import (
    cross_section_from_volume_flow_speed,
    mass_flow_from_volume_flow_density,
    volume_flow_from_cross_section_speed,
    volume_flow_from_mass_flow_density,
)
from eytelwein.main.units import get_unit_registry


u = get_unit_registry()


def _status(ok: bool) -> str:
    return "PASS" if ok else "FAIL"


def main() -> None:
    print("Feature F - Round-trip consistency checks")

    # Round trip 1: volume flow -> mass flow -> volume flow.
    density = 900.0 * u.kilogram / u.meter**3
    volume_in = 240.0 * u.meter**3 / u.hour
    mass = mass_flow_from_volume_flow_density(
        volume_flow=volume_in,
        bulk_density=density,
        unit="tonne/hour",
        precision=None,
    )
    volume_back = volume_flow_from_mass_flow_density(
        m_flow=mass,
        bulk_density=density,
        unit="meter**3/hour",
        precision=None,
    )
    delta_volume = (volume_back - volume_in.to(u.meter**3 / u.hour)).to(
        u.meter**3 / u.hour
    )
    tol_volume = 1e-9
    ok_volume = abs(delta_volume.magnitude) <= tol_volume

    # Round trip 2: cross-section -> volume flow -> cross-section.
    cross_section_in = 0.175 * u.meter**2
    belt_speed = 3.2 * u.meter / u.second
    volume_flow = volume_flow_from_cross_section_speed(
        cross_section_of_fill=cross_section_in,
        belt_speed=belt_speed,
        unit="meter**3/second",
        precision=None,
    )
    cross_section_back = cross_section_from_volume_flow_speed(
        volume_flow=volume_flow,
        belt_speed=belt_speed,
        unit="meter**2",
        precision=None,
    )
    delta_cross_section = (cross_section_back - cross_section_in.to(u.meter**2)).to(
        u.meter**2
    )
    tol_cross_section = 1e-12
    ok_cross_section = abs(delta_cross_section.magnitude) <= tol_cross_section

    print(
        "[1] volume -> mass -> volume: "
        f"delta={delta_volume:~P}, tol={tol_volume} m^3/h, {_status(ok_volume)}"
    )
    print(
        "[2] area -> volume -> area:   "
        f"delta={delta_cross_section:~P}, tol={tol_cross_section} m^2, {_status(ok_cross_section)}"
    )

    if not (ok_volume and ok_cross_section):
        raise SystemExit("Round-trip consistency check failed.")


if __name__ == "__main__":
    main()
