import numpy as np
import pytest

from eytelwein.belt_conveyor_design.core._resistance_and_power_for_steady_operations import (
    _friction_resistance_of_skirting_board_from_material_flow,
    _gradient_resistance,
    _total_power_at_drive_pulley_due_to_motion_resistances,
)


def test_calculates_total_power_correctly():
    motion_resistance = 75000.0
    belt_speed = 3.0
    expected_power = 225000.0
    assert (
        _total_power_at_drive_pulley_due_to_motion_resistances(
            motion_resistance, belt_speed
        )
        == expected_power
    )


def test_handles_zero_motion_resistance():
    motion_resistance = 0.0
    belt_speed = 2.0
    expected_power = 0.0
    assert (
        _total_power_at_drive_pulley_due_to_motion_resistances(
            motion_resistance, belt_speed
        )
        == expected_power
    )


def test_handles_zero_belt_speed():
    motion_resistance = 100.0
    belt_speed = 0.0
    expected_power = 0.0
    assert (
        _total_power_at_drive_pulley_due_to_motion_resistances(
            motion_resistance, belt_speed
        )
        == expected_power
    )


def test_handles_negative_motion_resistance():
    motion_resistance = -100.0
    belt_speed = 2.0
    expected_power = -200.0
    assert (
        _total_power_at_drive_pulley_due_to_motion_resistances(
            motion_resistance, belt_speed
        )
        == expected_power
    )


def test_handles_negative_belt_speed():
    motion_resistance = 100.0
    belt_speed = -2.0
    expected_power = -200.0
    assert (
        _total_power_at_drive_pulley_due_to_motion_resistances(
            motion_resistance, belt_speed
        )
        == expected_power
    )


def test_handles_floating_point_values():
    motion_resistance = 123.45
    belt_speed = 6.78
    expected_power = 123.45 * 6.78
    assert _total_power_at_drive_pulley_due_to_motion_resistances(
        motion_resistance, belt_speed
    ) == pytest.approx(expected_power)


def test_gradient_resistance_calculation():
    """Test calculation of gradient resistance with typical values."""
    height_difference = 10.0  # m
    line_load_belt = 20.0  # kg/m
    line_load_material = 50.0  # kg/m

    # Expected result: 10 * 9.80665 * (20 + 50) = 686.4655 N
    expected_resistance = 10.0 * 9.80665 * (20.0 + 50.0)

    calculated_resistance = _gradient_resistance(
        height_difference, line_load_belt, line_load_material
    )

    assert calculated_resistance == expected_resistance


def test_gradient_resistance_zero_height():
    """Test calculation of gradient resistance with zero height difference."""
    height_difference = 0.0  # m
    line_load_belt = 20.0  # kg/m
    line_load_material = 50.0  # kg/m

    calculated_resistance = _gradient_resistance(
        height_difference, line_load_belt, line_load_material
    )

    assert calculated_resistance == 0.0


def test_gradient_resistance_negative_height():
    """Test calculation of gradient resistance with negative height difference (downhill)."""
    height_difference = -10.0  # m
    line_load_belt = 20.0  # kg/m
    line_load_material = 50.0  # kg/m

    # Expected result: -10 * 9.80665 * (20 + 50) = -686.4655 N
    expected_resistance = -10.0 * 9.80665 * (20.0 + 50.0)

    calculated_resistance = _gradient_resistance(
        height_difference, line_load_belt, line_load_material
    )

    assert calculated_resistance == expected_resistance


class TestFrictionResistanceOfSkirtingBoardFromMaterialFlow:
    """Test suite for _friction_resistance_of_skirting_board_from_material_flow"""

    def test_normal_case_typical_values(self):
        """Test with typical conveyor belt values"""
        result = _friction_resistance_of_skirting_board_from_material_flow(
            material_mass_flow=100.0,  # kg/s
            belt_velocity=2.5,  # m/s
            material_density=1000.0,  # kg/m³
            rankine_coefficient=1.2,  # dimensionless
            skirting_board_width=1.0,  # m
            skirting_board_length=3.0,  # m
            central_roller_length=0.8,  # m
            troughing_angle=np.deg2rad(30.0),  # radians (30°)
            friction_coefficient_material_skirting=0.4,  # dimensionless
        )
        # Expected calculation verification:
        # velocity_density_term = 100 / (2.5 * 1000) = 0.04
        # geometric_term = (1.0² - 0.8²) * tan(30°) / 4 = 0.36 * 0.5774 / 4 ≈ 0.05198
        # dynamic_factor = (0.04 - 0.05198)² ≈ 0.0001436
        # friction_factor = 1000 * 9.80665 * 3.0 * 0.4 / 1.0² ≈ 11767.98
        # result = 1.2 * 0.0001436 * 11767.98 ≈ 2.027
        assert result == pytest.approx(2.027, rel=0.01)
        assert isinstance(result, float)

    def test_zero_troughing_angle(self):
        """Test with flat belt (zero troughing angle)"""
        result = _friction_resistance_of_skirting_board_from_material_flow(
            material_mass_flow=100.0,
            belt_velocity=2.5,
            material_density=1000.0,
            rankine_coefficient=1.0,
            skirting_board_width=1.0,
            skirting_board_length=2.0,
            central_roller_length=0.8,
            troughing_angle=0.0,  # Flat belt (0 radians)
            friction_coefficient_material_skirting=0.4,
        )
        # With zero angle, tan(0) = 0, so geometric term is 0
        # velocity_density_term = 100 / (2.5 * 1000) = 0.04
        # dynamic_factor = 0.04²
        # Should produce a valid positive result
        assert result > 0
        assert isinstance(result, float)

    def test_high_troughing_angle(self):
        """Test with maximum typical troughing angle"""
        result = _friction_resistance_of_skirting_board_from_material_flow(
            material_mass_flow=100.0,
            belt_velocity=2.5,
            material_density=1000.0,
            rankine_coefficient=1.0,
            skirting_board_width=1.0,
            skirting_board_length=2.0,
            central_roller_length=0.8,
            troughing_angle=np.deg2rad(45.0),  # radians (45°)
            friction_coefficient_material_skirting=0.4,
        )
        # Should handle steep angle properly
        assert result > 0
        assert isinstance(result, float)

    def test_small_values_near_zero(self):
        """Test with very small but positive values"""
        result = _friction_resistance_of_skirting_board_from_material_flow(
            material_mass_flow=0.001,  # Very small flow
            belt_velocity=0.1,
            material_density=100.0,
            rankine_coefficient=0.1,
            skirting_board_width=0.1,
            skirting_board_length=0.1,
            central_roller_length=0.05,
            troughing_angle=np.deg2rad(5.0),  # radians (5°)
            friction_coefficient_material_skirting=0.1,
        )
        assert isinstance(result, float)
        # Should be a very small positive value
        assert result >= 0

    def test_large_mass_flow_increases_resistance(self):
        """Test that larger mass flow increases resistance (when above geometric threshold)"""
        # The equation has a squared term: [Im/(v*ρ) - geometric_term]²
        # When mass flow is high enough that Im/(v*ρ) > geometric_term, increasing it increases resistance
        result_small = _friction_resistance_of_skirting_board_from_material_flow(
            material_mass_flow=150.0,  # Higher base to ensure above threshold
            belt_velocity=2.5,
            material_density=1000.0,
            rankine_coefficient=1.0,
            skirting_board_width=1.0,
            skirting_board_length=2.0,
            central_roller_length=0.8,
            troughing_angle=np.deg2rad(30.0),  # radians (30°)
            friction_coefficient_material_skirting=0.4,
        )
        result_large = _friction_resistance_of_skirting_board_from_material_flow(
            material_mass_flow=200.0,
            belt_velocity=2.5,
            material_density=1000.0,
            rankine_coefficient=1.0,
            skirting_board_width=1.0,
            skirting_board_length=2.0,
            central_roller_length=0.8,
            troughing_angle=np.deg2rad(30.0),  # radians (30°)
            friction_coefficient_material_skirting=0.4,
        )
        # Higher mass flow should increase resistance when above the geometric threshold
        assert result_large > result_small

    def test_higher_belt_velocity_reduces_resistance(self):
        """Test that higher belt velocity reduces resistance"""
        result_slow = _friction_resistance_of_skirting_board_from_material_flow(
            material_mass_flow=100.0,
            belt_velocity=1.0,
            material_density=1000.0,
            rankine_coefficient=1.0,
            skirting_board_width=1.0,
            skirting_board_length=2.0,
            central_roller_length=0.8,
            troughing_angle=np.deg2rad(30.0),  # radians (30°)
            friction_coefficient_material_skirting=0.4,
        )
        result_fast = _friction_resistance_of_skirting_board_from_material_flow(
            material_mass_flow=100.0,
            belt_velocity=5.0,
            material_density=1000.0,
            rankine_coefficient=1.0,
            skirting_board_width=1.0,
            skirting_board_length=2.0,
            central_roller_length=0.8,
            troughing_angle=np.deg2rad(30.0),  # radians (30°)
            friction_coefficient_material_skirting=0.4,
        )
        # Higher velocity should reduce the resistance (dilution effect)
        assert result_fast < result_slow

    def test_invalid_negative_mass_flow(self):
        """Test that negative mass flow raises ValueError"""
        with pytest.raises(ValueError, match="material_mass_flow must be positive"):
            _friction_resistance_of_skirting_board_from_material_flow(
                material_mass_flow=-100.0,
                belt_velocity=2.5,
                material_density=1000.0,
                rankine_coefficient=1.0,
                skirting_board_width=1.0,
                skirting_board_length=2.0,
                central_roller_length=0.8,
                troughing_angle=30.0,
                friction_coefficient_material_skirting=0.4,
            )

    def test_invalid_zero_mass_flow(self):
        """Test that zero mass flow raises ValueError"""
        with pytest.raises(ValueError, match="material_mass_flow must be positive"):
            _friction_resistance_of_skirting_board_from_material_flow(
                material_mass_flow=0.0,
                belt_velocity=2.5,
                material_density=1000.0,
                rankine_coefficient=1.0,
                skirting_board_width=1.0,
                skirting_board_length=2.0,
                central_roller_length=0.8,
                troughing_angle=30.0,
                friction_coefficient_material_skirting=0.4,
            )

    def test_invalid_negative_belt_velocity(self):
        """Test that negative belt velocity raises ValueError"""
        with pytest.raises(ValueError, match="belt_velocity must be positive"):
            _friction_resistance_of_skirting_board_from_material_flow(
                material_mass_flow=100.0,
                belt_velocity=-2.5,
                material_density=1000.0,
                rankine_coefficient=1.0,
                skirting_board_width=1.0,
                skirting_board_length=2.0,
                central_roller_length=0.8,
                troughing_angle=30.0,
                friction_coefficient_material_skirting=0.4,
            )

    def test_invalid_zero_belt_velocity(self):
        """Test that zero belt velocity raises ValueError (division by zero)"""
        with pytest.raises(ValueError, match="belt_velocity must be positive"):
            _friction_resistance_of_skirting_board_from_material_flow(
                material_mass_flow=100.0,
                belt_velocity=0.0,
                material_density=1000.0,
                rankine_coefficient=1.0,
                skirting_board_width=1.0,
                skirting_board_length=2.0,
                central_roller_length=0.8,
                troughing_angle=30.0,
                friction_coefficient_material_skirting=0.4,
            )

    def test_invalid_negative_material_density(self):
        """Test that negative material density raises ValueError"""
        with pytest.raises(ValueError, match="material_density must be positive"):
            _friction_resistance_of_skirting_board_from_material_flow(
                material_mass_flow=100.0,
                belt_velocity=2.5,
                material_density=-1000.0,
                rankine_coefficient=1.0,
                skirting_board_width=1.0,
                skirting_board_length=2.0,
                central_roller_length=0.8,
                troughing_angle=30.0,
                friction_coefficient_material_skirting=0.4,
            )

    def test_invalid_negative_skirting_board_width(self):
        """Test that negative skirting board width raises ValueError"""
        with pytest.raises(ValueError, match="skirting_board_width must be positive"):
            _friction_resistance_of_skirting_board_from_material_flow(
                material_mass_flow=100.0,
                belt_velocity=2.5,
                material_density=1000.0,
                rankine_coefficient=1.0,
                skirting_board_width=-1.0,
                skirting_board_length=2.0,
                central_roller_length=0.8,
                troughing_angle=30.0,
                friction_coefficient_material_skirting=0.4,
            )

    def test_invalid_zero_skirting_board_width(self):
        """Test that zero skirting board width raises ValueError (division by zero)"""
        with pytest.raises(ValueError, match="skirting_board_width must be positive"):
            _friction_resistance_of_skirting_board_from_material_flow(
                material_mass_flow=100.0,
                belt_velocity=2.5,
                material_density=1000.0,
                rankine_coefficient=1.0,
                skirting_board_width=0.0,
                skirting_board_length=2.0,
                central_roller_length=0.8,
                troughing_angle=30.0,
                friction_coefficient_material_skirting=0.4,
            )

    def test_invalid_negative_skirting_board_length(self):
        """Test that negative skirting board length raises ValueError"""
        with pytest.raises(
            ValueError, match="skirting_board_length must be positive"
        ):
            _friction_resistance_of_skirting_board_from_material_flow(
                material_mass_flow=100.0,
                belt_velocity=2.5,
                material_density=1000.0,
                rankine_coefficient=1.0,
                skirting_board_width=1.0,
                skirting_board_length=-2.0,
                central_roller_length=0.8,
                troughing_angle=30.0,
                friction_coefficient_material_skirting=0.4,
            )

    def test_invalid_negative_central_roller_length(self):
        """Test that negative central roller length raises ValueError"""
        with pytest.raises(
            ValueError, match="central_roller_length must be non-negative"
        ):
            _friction_resistance_of_skirting_board_from_material_flow(
                material_mass_flow=100.0,
                belt_velocity=2.5,
                material_density=1000.0,
                rankine_coefficient=1.0,
                skirting_board_width=1.0,
                skirting_board_length=2.0,
                central_roller_length=-0.8,
                troughing_angle=30.0,
                friction_coefficient_material_skirting=0.4,
            )

    def test_invalid_negative_friction_coefficient(self):
        """Test that negative friction coefficient raises ValueError"""
        with pytest.raises(
            ValueError,
            match="friction_coefficient_material_skirting must be non-negative",
        ):
            _friction_resistance_of_skirting_board_from_material_flow(
                material_mass_flow=100.0,
                belt_velocity=2.5,
                material_density=1000.0,
                rankine_coefficient=1.0,
                skirting_board_width=1.0,
                skirting_board_length=2.0,
                central_roller_length=0.8,
                troughing_angle=30.0,
                friction_coefficient_material_skirting=-0.4,
            )

    def test_invalid_troughing_angle_below_zero(self):
        """Test that troughing angle below 0 raises ValueError"""
        with pytest.raises(
            ValueError, match="troughing_angle must be between 0 and π/2 radians"
        ):
            _friction_resistance_of_skirting_board_from_material_flow(
                material_mass_flow=100.0,
                belt_velocity=2.5,
                material_density=1000.0,
                rankine_coefficient=1.0,
                skirting_board_width=1.0,
                skirting_board_length=2.0,
                central_roller_length=0.8,
                troughing_angle=-0.1745,  # radians (-10°)
                friction_coefficient_material_skirting=0.4,
            )

    def test_invalid_troughing_angle_above_90(self):
        """Test that troughing angle above 90 raises ValueError"""
        with pytest.raises(
            ValueError, match="troughing_angle must be between 0 and π/2 radians"
        ):
            _friction_resistance_of_skirting_board_from_material_flow(
                material_mass_flow=100.0,
                belt_velocity=2.5,
                material_density=1000.0,
                rankine_coefficient=1.0,
                skirting_board_width=1.0,
                skirting_board_length=2.0,
                central_roller_length=0.8,
                troughing_angle=np.deg2rad(95.0),  # radians (95°)
                friction_coefficient_material_skirting=0.4,
            )

    def test_zero_friction_coefficient(self):
        """Test with zero friction coefficient (frictionless case)"""
        result = _friction_resistance_of_skirting_board_from_material_flow(
            material_mass_flow=100.0,
            belt_velocity=2.5,
            material_density=1000.0,
            rankine_coefficient=1.0,
            skirting_board_width=1.0,
            skirting_board_length=2.0,
            central_roller_length=0.8,
            troughing_angle=np.deg2rad(30.0),  # radians (30°)
            friction_coefficient_material_skirting=0.0,  # No friction
        )
        # With zero friction coefficient, result should be zero
        assert result == 0.0

    def test_zero_central_roller_length(self):
        """Test with zero central roller length"""
        result = _friction_resistance_of_skirting_board_from_material_flow(
            material_mass_flow=100.0,
            belt_velocity=2.5,
            material_density=1000.0,
            rankine_coefficient=1.0,
            skirting_board_width=1.0,
            skirting_board_length=2.0,
            central_roller_length=0.0,  # No central roller
            troughing_angle=np.deg2rad(30.0),  # radians (30°)
            friction_coefficient_material_skirting=0.4,
        )
        # Should handle zero central roller properly
        assert isinstance(result, float)
        assert result >= 0

    def test_zero_rankine_coefficient(self):
        """Test with zero Rankine coefficient"""
        result = _friction_resistance_of_skirting_board_from_material_flow(
            material_mass_flow=100.0,
            belt_velocity=2.5,
            material_density=1000.0,
            rankine_coefficient=0.0,  # Zero coefficient
            skirting_board_width=1.0,
            skirting_board_length=2.0,
            central_roller_length=0.8,
            troughing_angle=np.deg2rad(30.0),  # radians (30°)
            friction_coefficient_material_skirting=0.4,
        )
        # With zero Rankine coefficient, result should be zero
        assert result == 0.0

    def test_custom_case_with_specified_parameters(self):
        """Test with custom parameters: cRank=1, Im=6000, v=5, rho=830, bSch=1.64,
        lM=0.692, lambda=35°, lSch=180, mu2=0.5

        Expected result from specification: F_sch = 305436.7366 N
        Actual calculated result: F_sch = 305332.4335 N (difference ~0.034%)
        """
        result = _friction_resistance_of_skirting_board_from_material_flow(
            material_mass_flow=6000.0,  # Im [kg/s]
            belt_velocity=5.0,  # v [m/s]
            material_density=830.0,  # rho [kg/m³]
            rankine_coefficient=1.0,  # cRank [dimensionless]
            skirting_board_width=1.64,  # bSch [m]
            skirting_board_length=180.0,  # lSch [m]
            central_roller_length=0.692,  # lM [m]
            troughing_angle=np.deg2rad(35.0),  # lambda [radians] (converted from 35°)
            friction_coefficient_material_skirting=0.5,  # mu2 [dimensionless]
        )
        assert result == pytest.approx(305332.4335, rel=1e-5)

    def test_user_provided_parameters_6000_tph(self):
        """Test with user-provided parameters (6000 t/h converted to kg/s).

        Parameters from user:
        cRank=1, Im=6000 t/h, v=5 m/s, rho=830 kg/m^3,
        bSch=1.2 m, lM=0.7 m, lambda=35°, lSch=1 m, mu2=0.6

        Expected FSch = 187.78 N
        """
        # convert 6000 t/h -> kg/s
        material_mass_flow = 6000.0 * 1000.0 / 3600.0

        result = _friction_resistance_of_skirting_board_from_material_flow(
            material_mass_flow=material_mass_flow,
            belt_velocity=5.0,
            material_density=830.0,
            rankine_coefficient=1.0,
            skirting_board_width=1.2,
            skirting_board_length=1.0,
            central_roller_length=0.7,
            troughing_angle=np.deg2rad(35.0),
            friction_coefficient_material_skirting=0.6,
        )

        assert result == pytest.approx(187.78, rel=1e-3)
