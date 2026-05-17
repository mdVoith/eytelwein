"""
Tests for private raw float functions in extended mass inertia module.
Tests follow strict TDD: failing tests first.
"""
import pytest
from eytelwein.belt_conveyor_design.extended._mass_inertia import (
    belt_mass_per_strand,
    payload_mass_total,
    translating_mass_empty,
    translating_mass_full,
    pulley_radius,
    motor_shaft_inertia_total,
    inertia_per_drive,
)


class TestBeltMassPerStrand:
    """Test belt_mass_per_strand = belt_linear_mass_kg_per_m * center_distance_m"""

    def test_belt_mass_per_strand_basic(self):
        """Basic test: 10 kg/m * 100 m = 1000 kg"""
        result = belt_mass_per_strand(10.0, 100.0)
        assert result == pytest.approx(1000.0)

    def test_belt_mass_per_strand_spec_case(self):
        """Spec test case: 25.887500 kg/m * 4303.0 m = 111393.9125 kg"""
        result = belt_mass_per_strand(25.887500, 4303.0)
        assert result == pytest.approx(111393.9125, rel=0.005)

    def test_belt_mass_per_strand_zero_linear_mass(self):
        """Belt with zero linear mass should give zero strand mass"""
        result = belt_mass_per_strand(0.0, 100.0)
        assert result == 0.0

    def test_belt_mass_per_strand_small_values(self):
        """Test with small decimal values"""
        result = belt_mass_per_strand(0.5, 10.0)
        assert result == pytest.approx(5.0)


class TestPayloadMassTotal:
    """Test payload_mass_total = payload_mass_per_meter_kg_per_m * center_distance_m"""

    def test_payload_mass_total_basic(self):
        """Basic test: 50 kg/m * 200 m = 10000 kg"""
        result = payload_mass_total(50.0, 200.0)
        assert result == pytest.approx(10000.0)

    def test_payload_mass_total_spec_case(self):
        """Spec test case: 124.7 kg/m * 4303.0 m = 536584.1 kg"""
        result = payload_mass_total(124.7, 4303.0)
        assert result == pytest.approx(536584.1, rel=0.005)

    def test_payload_mass_total_zero_payload(self):
        """Empty conveyor should have zero payload mass"""
        result = payload_mass_total(0.0, 100.0)
        assert result == 0.0

    def test_payload_mass_total_decimal(self):
        """Test with decimal payload mass"""
        result = payload_mass_total(12.5, 80.0)
        assert result == pytest.approx(1000.0)


class TestTranslatingMassEmpty:
    """Test translating_mass_empty = idler_upper + idler_lower + 2*belt_mass"""

    def test_translating_mass_empty_basic(self):
        """Basic test: 100 + 50 + 2*25 = 200 kg"""
        result = translating_mass_empty(100.0, 50.0, 25.0)
        assert result == pytest.approx(200.0)

    def test_translating_mass_empty_spec_case(self):
        """Spec test case: 18503 + 6168 + 2*111393.9125 = 247458.825 kg"""
        result = translating_mass_empty(18503.0, 6168.0, 111393.9125)
        assert result == pytest.approx(247458.825, rel=0.005)

    def test_translating_mass_empty_zero_idlers(self):
        """With zero idler masses: 0 + 0 + 2*100 = 200 kg"""
        result = translating_mass_empty(0.0, 0.0, 100.0)
        assert result == pytest.approx(200.0)

    def test_translating_mass_empty_zero_belt(self):
        """With zero belt mass: 50 + 30 + 0 = 80 kg"""
        result = translating_mass_empty(50.0, 30.0, 0.0)
        assert result == pytest.approx(80.0)


class TestTranslatingMassFull:
    """Test translating_mass_full = translating_mass_empty + payload_mass_total"""

    def test_translating_mass_full_basic(self):
        """Basic test: 500 + 250 = 750 kg"""
        result = translating_mass_full(500.0, 250.0)
        assert result == pytest.approx(750.0)

    def test_translating_mass_full_spec_case(self):
        """Spec test case: 247458.825 + 536584.1 = 784042.925 kg"""
        result = translating_mass_full(247458.825, 536584.1)
        assert result == pytest.approx(784042.925, rel=0.005)

    def test_translating_mass_full_no_payload(self):
        """Without payload: 400 + 0 = 400 kg"""
        result = translating_mass_full(400.0, 0.0)
        assert result == pytest.approx(400.0)


class TestPulleyRadius:
    """Test pulley_radius = drive_pulley_diameter_m / 2"""

    def test_pulley_radius_basic(self):
        """Basic test: diameter 2 m -> radius 1 m"""
        result = pulley_radius(2.0)
        assert result == pytest.approx(1.0)

    def test_pulley_radius_spec_case(self):
        """Spec test case: diameter 1.04 m -> radius 0.52 m"""
        result = pulley_radius(1.04)
        assert result == pytest.approx(0.52)

    def test_pulley_radius_small_diameter(self):
        """Test with small diameter"""
        result = pulley_radius(0.5)
        assert result == pytest.approx(0.25)

    def test_pulley_radius_large_diameter(self):
        """Test with large diameter"""
        result = pulley_radius(10.0)
        assert result == pytest.approx(5.0)


class TestMotorShaftInertiaTotal:
    """Test inertia = translating_mass * radius^2 / gear_ratio^2"""

    def test_motor_shaft_inertia_total_basic(self):
        """Basic test: 1000 * 1^2 / 2^2 = 250 kg·m²"""
        result = motor_shaft_inertia_total(1000.0, 1.0, 2.0)
        assert result == pytest.approx(250.0)

    def test_motor_shaft_inertia_total_spec_case_empty(self):
        """Spec test case empty: 247458.825 * 0.52^2 / 11.731^2 = 486.227552"""
        result = motor_shaft_inertia_total(247458.825, 0.52, 11.731)
        assert result == pytest.approx(486.227552, rel=0.005)

    def test_motor_shaft_inertia_total_spec_case_full(self):
        """Spec test case full: 784042.925 * 0.52^2 / 11.731^2 = 1540.552340"""
        result = motor_shaft_inertia_total(784042.925, 0.52, 11.731)
        assert result == pytest.approx(1540.552340, rel=0.005)

    def test_motor_shaft_inertia_total_zero_mass(self):
        """Zero mass should give zero inertia"""
        result = motor_shaft_inertia_total(0.0, 1.0, 2.0)
        assert result == pytest.approx(0.0)

    def test_motor_shaft_inertia_total_high_gear_ratio(self):
        """High gear ratio should reduce inertia"""
        result = motor_shaft_inertia_total(1000.0, 1.0, 10.0)
        assert result == pytest.approx(10.0)


class TestInertiaPerDrive:
    """Test inertia_per_drive = inertia_total / motor_count"""

    def test_inertia_per_drive_basic(self):
        """Basic test: 1000 / 2 = 500 kg·m²"""
        result = inertia_per_drive(1000.0, 2)
        assert result == pytest.approx(500.0)

    def test_inertia_per_drive_spec_case_empty(self):
        """Spec test case empty: 486.227552 / 2 = 243.113776"""
        result = inertia_per_drive(486.227552, 2)
        assert result == pytest.approx(243.113776, rel=0.005)

    def test_inertia_per_drive_spec_case_full(self):
        """Spec test case full: 1540.552340 / 2 = 770.276170"""
        result = inertia_per_drive(1540.552340, 2)
        assert result == pytest.approx(770.276170, rel=0.005)

    def test_inertia_per_drive_single_motor(self):
        """Single motor: equivalent to total inertia"""
        result = inertia_per_drive(1000.0, 1)
        assert result == pytest.approx(1000.0)

    def test_inertia_per_drive_multiple_motors(self):
        """Multiple motors: divide by count"""
        result = inertia_per_drive(3000.0, 3)
        assert result == pytest.approx(1000.0)


class TestSpecCaseOptionBArealTimesWidth:
    """Integration test: Option B (areal + width) through motor shaft inertia"""

    def test_spec_case_option_b_full_calculation(self):
        """
        Full spec case with Option B (areal × width) for belt mass.
        Inputs:
        - centerDistanceM: 4303.0
        - beltArealMassKgPerM2: 20.71
        - beltWidthM: 1.25
        - payloadMassPerMeterKgPerM: 124.7
        - idlerMassUpperTotalKg: 18503
        - idlerMassLowerTotalKg: 6168
        - drivePulleyDiameterM: 1.04
        - gearRatioMotorToPulley: 11.731
        - motorCount: 2

        Expected outputs (with <=0.5% tolerance):
        - resolvedBeltLinearMassKgPerM: 25.887500
        - beltMassPerStrandKg: 111393.912500
        - payloadMassTotalKg: 536584.100000
        - translatingMassEmptyKg: 247458.825000
        - translatingMassFullKg: 784042.925000
        - inertiaEmptyTotalMotorShaft: 486.227552
        - inertiaFullTotalMotorShaft: 1540.552340
        - inertiaEmptyPerDriveMotorShaft: 243.113776
        - inertiaFullPerDriveMotorShaft: 770.276170
        """
        # Step 1: Resolve belt linear mass
        center_distance_m = 4303.0
        belt_areal_mass_kg_per_m2 = 20.71
        belt_width_m = 1.25
        resolved_belt_linear_mass = belt_areal_mass_kg_per_m2 * belt_width_m  # 25.8875
        assert resolved_belt_linear_mass == pytest.approx(25.887500, rel=0.005)

        # Step 2: Belt mass per strand
        belt_mass_per_strand_kg = belt_mass_per_strand(
            resolved_belt_linear_mass, center_distance_m
        )
        assert belt_mass_per_strand_kg == pytest.approx(111393.912500, rel=0.005)

        # Step 3: Payload mass total
        payload_mass_per_meter_kg_per_m = 124.7
        payload_mass_total_kg = payload_mass_total(
            payload_mass_per_meter_kg_per_m, center_distance_m
        )
        assert payload_mass_total_kg == pytest.approx(536584.100000, rel=0.005)

        # Step 4: Translating masses
        idler_mass_upper_total_kg = 18503.0
        idler_mass_lower_total_kg = 6168.0
        translating_mass_empty_kg = translating_mass_empty(
            idler_mass_upper_total_kg, idler_mass_lower_total_kg, belt_mass_per_strand_kg
        )
        assert translating_mass_empty_kg == pytest.approx(247458.825000, rel=0.005)

        translating_mass_full_kg = translating_mass_full(
            translating_mass_empty_kg, payload_mass_total_kg
        )
        assert translating_mass_full_kg == pytest.approx(784042.925000, rel=0.005)

        # Step 5: Pulley radius
        drive_pulley_diameter_m = 1.04
        drive_pulley_radius_m = pulley_radius(drive_pulley_diameter_m)
        assert drive_pulley_radius_m == pytest.approx(0.520000, rel=0.005)

        # Step 6: Motor shaft inertia
        gear_ratio_motor_to_pulley = 11.731
        motor_count = 2

        inertia_empty_total = motor_shaft_inertia_total(
            translating_mass_empty_kg, drive_pulley_radius_m, gear_ratio_motor_to_pulley
        )
        assert inertia_empty_total == pytest.approx(486.227552, rel=0.005)

        inertia_full_total = motor_shaft_inertia_total(
            translating_mass_full_kg, drive_pulley_radius_m, gear_ratio_motor_to_pulley
        )
        assert inertia_full_total == pytest.approx(1540.552340, rel=0.005)

        inertia_empty_per_drive = inertia_per_drive(inertia_empty_total, motor_count)
        assert inertia_empty_per_drive == pytest.approx(243.113776, rel=0.005)

        inertia_full_per_drive = inertia_per_drive(inertia_full_total, motor_count)
        assert inertia_full_per_drive == pytest.approx(770.276170, rel=0.005)
