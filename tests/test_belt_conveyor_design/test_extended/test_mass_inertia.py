"""
Tests for public Pint Quantity wrapper functions in extended mass inertia module.
These wrap private float functions with unit conversion and validation.
Tests follow strict TDD: failing tests first.
"""
import pytest
from pint import Quantity

from eytelwein.belt_conveyor_design.extended.mass_inertia import (
    belt_mass_per_strand,
    payload_mass_total,
    translating_mass_empty,
    translating_mass_full,
    pulley_radius,
    motor_shaft_inertia_total,
    inertia_per_drive,
)
from eytelwein.main.units import get_unit_registry

u = get_unit_registry()


class TestPublicBeltMassPerStrand:
    """Test public Pint wrapper for belt_mass_per_strand"""

    def test_belt_mass_per_strand_basic_kg_per_m(self):
        """Test with kg/m input"""
        linear_mass = Quantity(10.0, u.kilogram / u.meter)
        center_distance = Quantity(100.0, u.meter)
        result = belt_mass_per_strand(linear_mass, center_distance)
        assert isinstance(result, Quantity)
        assert result.units == u.kilogram
        assert result.magnitude == pytest.approx(1000.0)

    def test_belt_mass_per_strand_spec_case(self):
        """Spec test case with Pint Quantities"""
        linear_mass = Quantity(25.887500, u.kilogram / u.meter)
        center_distance = Quantity(4303.0, u.meter)
        result = belt_mass_per_strand(linear_mass, center_distance)
        assert result.magnitude == pytest.approx(111393.9125, rel=0.005)

    def test_belt_mass_per_strand_unit_conversion(self):
        """Test with non-SI units that convert to SI"""
        linear_mass = Quantity(10.0, u.gram / u.meter)
        center_distance = Quantity(100.0, u.meter)
        result = belt_mass_per_strand(linear_mass, center_distance)
        assert result.magnitude == pytest.approx(1.0, rel=0.005)  # 10g/m * 100m = 1kg

    def test_belt_mass_per_strand_invalid_linear_mass_unit(self):
        """Test with invalid unit for linear mass"""
        linear_mass = Quantity(10.0, u.meter)  # Wrong unit!
        center_distance = Quantity(100.0, u.meter)
        with pytest.raises(ValueError):
            belt_mass_per_strand(linear_mass, center_distance)

    def test_belt_mass_per_strand_invalid_center_distance_unit(self):
        """Test with invalid unit for center distance"""
        linear_mass = Quantity(10.0, u.kilogram / u.meter)
        center_distance = Quantity(100.0, u.kilogram)  # Wrong unit!
        with pytest.raises(ValueError):
            belt_mass_per_strand(linear_mass, center_distance)


class TestPublicPayloadMassTotal:
    """Test public Pint wrapper for payload_mass_total"""

    def test_payload_mass_total_basic(self):
        """Test with kg/m input"""
        mass_per_meter = Quantity(50.0, u.kilogram / u.meter)
        center_distance = Quantity(200.0, u.meter)
        result = payload_mass_total(mass_per_meter, center_distance)
        assert isinstance(result, Quantity)
        assert result.units == u.kilogram
        assert result.magnitude == pytest.approx(10000.0)

    def test_payload_mass_total_spec_case(self):
        """Spec test case with Pint Quantities"""
        mass_per_meter = Quantity(124.7, u.kilogram / u.meter)
        center_distance = Quantity(4303.0, u.meter)
        result = payload_mass_total(mass_per_meter, center_distance)
        assert result.magnitude == pytest.approx(536584.1, rel=0.005)

    def test_payload_mass_total_invalid_unit(self):
        """Test with invalid unit"""
        mass_per_meter = Quantity(50.0, u.meter)  # Wrong unit!
        center_distance = Quantity(200.0, u.meter)
        with pytest.raises(ValueError):
            payload_mass_total(mass_per_meter, center_distance)


class TestPublicTranslatingMassEmpty:
    """Test public Pint wrapper for translating_mass_empty"""

    def test_translating_mass_empty_basic(self):
        """Test basic inputs"""
        idler_upper = Quantity(100.0, u.kilogram)
        idler_lower = Quantity(50.0, u.kilogram)
        belt_mass = Quantity(25.0, u.kilogram)
        result = translating_mass_empty(idler_upper, idler_lower, belt_mass)
        assert isinstance(result, Quantity)
        assert result.units == u.kilogram
        assert result.magnitude == pytest.approx(200.0)

    def test_translating_mass_empty_spec_case(self):
        """Spec test case with Pint Quantities"""
        idler_upper = Quantity(18503.0, u.kilogram)
        idler_lower = Quantity(6168.0, u.kilogram)
        belt_mass = Quantity(111393.9125, u.kilogram)
        result = translating_mass_empty(idler_upper, idler_lower, belt_mass)
        assert result.magnitude == pytest.approx(247458.825, rel=0.005)

    def test_translating_mass_empty_unit_conversion(self):
        """Test with non-SI units"""
        idler_upper = Quantity(1000.0, u.gram)  # 1 kg
        idler_lower = Quantity(500.0, u.gram)   # 0.5 kg
        belt_mass = Quantity(250.0, u.gram)     # 0.25 kg
        result = translating_mass_empty(idler_upper, idler_lower, belt_mass)
        # 1 + 0.5 + 2*0.25 = 2 kg
        assert result.units == u.kilogram
        assert result.magnitude == pytest.approx(2.0, rel=0.005)

    def test_translating_mass_empty_invalid_unit(self):
        """Test with invalid unit"""
        idler_upper = Quantity(100.0, u.meter)  # Wrong unit!
        idler_lower = Quantity(50.0, u.kilogram)
        belt_mass = Quantity(25.0, u.kilogram)
        with pytest.raises(ValueError):
            translating_mass_empty(idler_upper, idler_lower, belt_mass)


class TestPublicTranslatingMassFull:
    """Test public Pint wrapper for translating_mass_full"""

    def test_translating_mass_full_basic(self):
        """Test basic inputs"""
        empty = Quantity(500.0, u.kilogram)
        payload = Quantity(250.0, u.kilogram)
        result = translating_mass_full(empty, payload)
        assert isinstance(result, Quantity)
        assert result.units == u.kilogram
        assert result.magnitude == pytest.approx(750.0)

    def test_translating_mass_full_spec_case(self):
        """Spec test case with Pint Quantities"""
        empty = Quantity(247458.825, u.kilogram)
        payload = Quantity(536584.1, u.kilogram)
        result = translating_mass_full(empty, payload)
        assert result.magnitude == pytest.approx(784042.925, rel=0.005)

    def test_translating_mass_full_invalid_unit(self):
        """Test with invalid unit"""
        empty = Quantity(500.0, u.meter)  # Wrong unit!
        payload = Quantity(250.0, u.kilogram)
        with pytest.raises(ValueError):
            translating_mass_full(empty, payload)


class TestPublicPulleyRadius:
    """Test public Pint wrapper for pulley_radius"""

    def test_pulley_radius_basic(self):
        """Test basic input"""
        diameter = Quantity(2.0, u.meter)
        result = pulley_radius(diameter)
        assert isinstance(result, Quantity)
        assert result.units == u.meter
        assert result.magnitude == pytest.approx(1.0)

    def test_pulley_radius_spec_case(self):
        """Spec test case with Pint Quantities"""
        diameter = Quantity(1.04, u.meter)
        result = pulley_radius(diameter)
        assert result.magnitude == pytest.approx(0.52, rel=0.005)

    def test_pulley_radius_unit_conversion(self):
        """Test with non-SI units"""
        diameter = Quantity(2000.0, u.millimeter)  # 2 m
        result = pulley_radius(diameter)
        assert result.units == u.meter
        assert result.magnitude == pytest.approx(1.0, rel=0.005)

    def test_pulley_radius_invalid_unit(self):
        """Test with invalid unit"""
        diameter = Quantity(2.0, u.kilogram)  # Wrong unit!
        with pytest.raises(ValueError):
            pulley_radius(diameter)


class TestPublicMotorShaftInertiaTotal:
    """Test public Pint wrapper for motor_shaft_inertia_total"""

    def test_motor_shaft_inertia_total_basic(self):
        """Test basic inputs"""
        mass = Quantity(1000.0, u.kilogram)
        radius = Quantity(1.0, u.meter)
        gear_ratio = Quantity(2.0, u.dimensionless)
        result = motor_shaft_inertia_total(mass, radius, gear_ratio)
        assert isinstance(result, Quantity)
        assert result.magnitude == pytest.approx(250.0)

    def test_motor_shaft_inertia_total_spec_case_empty(self):
        """Spec test case empty with Pint Quantities"""
        mass = Quantity(247458.825, u.kilogram)
        radius = Quantity(0.52, u.meter)
        gear_ratio = Quantity(11.731, u.dimensionless)
        result = motor_shaft_inertia_total(mass, radius, gear_ratio)
        assert result.magnitude == pytest.approx(486.227552, rel=0.005)

    def test_motor_shaft_inertia_total_spec_case_full(self):
        """Spec test case full with Pint Quantities"""
        mass = Quantity(784042.925, u.kilogram)
        radius = Quantity(0.52, u.meter)
        gear_ratio = Quantity(11.731, u.dimensionless)
        result = motor_shaft_inertia_total(mass, radius, gear_ratio)
        assert result.magnitude == pytest.approx(1540.552340, rel=0.005)

    def test_motor_shaft_inertia_total_invalid_mass_unit(self):
        """Test with invalid mass unit"""
        mass = Quantity(1000.0, u.meter)  # Wrong unit!
        radius = Quantity(1.0, u.meter)
        gear_ratio = Quantity(2.0, u.dimensionless)
        with pytest.raises(ValueError):
            motor_shaft_inertia_total(mass, radius, gear_ratio)

    def test_motor_shaft_inertia_total_invalid_radius_unit(self):
        """Test with invalid radius unit"""
        mass = Quantity(1000.0, u.kilogram)
        radius = Quantity(1.0, u.kilogram)  # Wrong unit!
        gear_ratio = Quantity(2.0, u.dimensionless)
        with pytest.raises(ValueError):
            motor_shaft_inertia_total(mass, radius, gear_ratio)


class TestPublicInertiaPerDrive:
    """Test public Pint wrapper for inertia_per_drive"""

    def test_inertia_per_drive_basic(self):
        """Test basic inputs"""
        inertia_total = Quantity(1000.0, u.kilogram * u.meter**2)
        motor_count = 2
        result = inertia_per_drive(inertia_total, motor_count)
        assert isinstance(result, Quantity)
        assert result.units == u.kilogram * u.meter**2
        assert result.magnitude == pytest.approx(500.0)

    def test_inertia_per_drive_spec_case_empty(self):
        """Spec test case empty with Pint Quantities"""
        inertia_total = Quantity(486.227552, u.kilogram * u.meter**2)
        motor_count = 2
        result = inertia_per_drive(inertia_total, motor_count)
        assert result.magnitude == pytest.approx(243.113776, rel=0.005)

    def test_inertia_per_drive_spec_case_full(self):
        """Spec test case full with Pint Quantities"""
        inertia_total = Quantity(1540.552340, u.kilogram * u.meter**2)
        motor_count = 2
        result = inertia_per_drive(inertia_total, motor_count)
        assert result.magnitude == pytest.approx(770.276170, rel=0.005)

    def test_inertia_per_drive_invalid_unit(self):
        """Test with invalid unit"""
        inertia_total = Quantity(1000.0, u.kilogram)  # Wrong unit!
        motor_count = 2
        with pytest.raises(ValueError):
            inertia_per_drive(inertia_total, motor_count)

    def test_inertia_per_drive_invalid_motor_count(self):
        """Test with invalid motor count (must be >= 1)"""
        inertia_total = Quantity(1000.0, u.kilogram * u.meter**2)
        motor_count = 0
        with pytest.raises(ValueError):
            inertia_per_drive(inertia_total, motor_count)

    def test_inertia_per_drive_single_motor(self):
        """Single motor case"""
        inertia_total = Quantity(1000.0, u.kilogram * u.meter**2)
        motor_count = 1
        result = inertia_per_drive(inertia_total, motor_count)
        assert result.magnitude == pytest.approx(1000.0)


class TestIntegrationPublicSpecCase:
    """Integration test: full spec case with public Pint wrappers"""

    def test_spec_case_option_b_with_public_wrappers(self):
        """
        Full spec case with Option B (areal × width) using public Pint wrappers.
        All calculations flow through public wrappers with unit handling.
        """
        # Step 1: Resolve belt linear mass from areal and width
        belt_areal_mass = Quantity(20.71, u.kilogram / u.meter**2)
        belt_width = Quantity(1.25, u.meter)
        resolved_belt_linear_mass_magnitude = (
            belt_areal_mass.magnitude * belt_width.magnitude
        )  # 25.8875
        resolved_belt_linear_mass = Quantity(resolved_belt_linear_mass_magnitude, u.kilogram / u.meter)

        # Step 2: Belt mass per strand
        center_distance = Quantity(4303.0, u.meter)
        belt_mass_per_strand_kg = belt_mass_per_strand(
            resolved_belt_linear_mass, center_distance
        )
        assert belt_mass_per_strand_kg.magnitude == pytest.approx(111393.9125, rel=0.005)

        # Step 3: Payload mass total
        payload_mass_per_meter = Quantity(124.7, u.kilogram / u.meter)
        payload_mass_total_kg = payload_mass_total(
            payload_mass_per_meter, center_distance
        )
        assert payload_mass_total_kg.magnitude == pytest.approx(536584.1, rel=0.005)

        # Step 4: Translating masses
        idler_mass_upper = Quantity(18503.0, u.kilogram)
        idler_mass_lower = Quantity(6168.0, u.kilogram)
        translating_mass_empty_kg = translating_mass_empty(
            idler_mass_upper, idler_mass_lower, belt_mass_per_strand_kg
        )
        assert translating_mass_empty_kg.magnitude == pytest.approx(247458.825, rel=0.005)

        translating_mass_full_kg = translating_mass_full(
            translating_mass_empty_kg, payload_mass_total_kg
        )
        assert translating_mass_full_kg.magnitude == pytest.approx(784042.925, rel=0.005)

        # Step 5: Pulley radius
        drive_pulley_diameter = Quantity(1.04, u.meter)
        drive_pulley_radius_m = pulley_radius(drive_pulley_diameter)
        assert drive_pulley_radius_m.magnitude == pytest.approx(0.52, rel=0.005)

        # Step 6: Motor shaft inertias
        gear_ratio = Quantity(11.731, u.dimensionless)
        motor_count = 2

        inertia_empty_total = motor_shaft_inertia_total(
            translating_mass_empty_kg, drive_pulley_radius_m, gear_ratio
        )
        assert inertia_empty_total.magnitude == pytest.approx(486.227552, rel=0.005)

        inertia_full_total = motor_shaft_inertia_total(
            translating_mass_full_kg, drive_pulley_radius_m, gear_ratio
        )
        assert inertia_full_total.magnitude == pytest.approx(1540.552340, rel=0.005)

        inertia_empty_per_drive = inertia_per_drive(inertia_empty_total, motor_count)
        assert inertia_empty_per_drive.magnitude == pytest.approx(243.113776, rel=0.005)

        inertia_full_per_drive = inertia_per_drive(inertia_full_total, motor_count)
        assert inertia_full_per_drive.magnitude == pytest.approx(770.276170, rel=0.005)
