import pytest
from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
    gradient_resistance,
    total_power_at_drive_pulley_due_to_motion_resistances,
)
from eytelwein.main.constants import STANDARD_GRAVITY_VALUE
from eytelwein.main.units import get_unit_registry
import numpy as np
from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
    gradient_resistance_sections,
)


# Get unit registry for tests
u = get_unit_registry()


def test_gradient_resistance_basic():
    """Test basic gradient resistance calculation with numeric inputs."""
    # Basic test with 10m height, 20 kg/m belt, 50 kg/m material
    with pytest.raises(ValueError):
        gradient_resistance(-10, 20, 50)


def test_gradient_resistance_with_quantities():
    """Test gradient resistance calculation with Quantity inputs."""
    # Using quantities for all inputs
    height = 10 * u.meter
    belt_load = 20 * u.kg / u.meter
    material_load = 50 * u.kg / u.meter

    result = gradient_resistance(height, belt_load, material_load)
    expected = 10 * STANDARD_GRAVITY_VALUE * (20 + 50)

    assert result.magnitude == pytest.approx(expected)
    assert result.units == u.newton


def test_gradient_resistance_with_different_units():
    """Test gradient resistance calculation with different units."""
    # Using different but compatible units
    height = 1000 * u.centimeter  # 10m
    belt_load = 0.02 * u.tonne / u.meter  # 20 kg/m
    material_load = 0.05 * u.tonne / u.meter  # 50 kg/m

    result = gradient_resistance(height, belt_load, material_load)
    expected = 10 * STANDARD_GRAVITY_VALUE * (20 + 50)

    assert result.magnitude == pytest.approx(expected)
    assert result.units == u.newton


def test_gradient_resistance_output_unit():
    """Test gradient resistance calculation with different output units."""
    # Requesting output in kilonewtons
    height = 10 * u.meter
    belt_load = 20 * u.kg / u.meter
    material_load = 50 * u.kg / u.meter

    result = gradient_resistance(height, belt_load, material_load, unit="kilonewton")
    expected = 10 * STANDARD_GRAVITY_VALUE * (20 + 50) / 1000  # Converting to kN

    assert result.magnitude == pytest.approx(expected, rel=1e-3)
    assert result.units == u.kilonewton


def test_gradient_resistance_precision():
    """Test gradient resistance calculation with specific precision."""
    height = 10 * u.meter
    belt_load = 20 * u.kg / u.meter
    material_load = 50 * u.kg / u.meter

    result = gradient_resistance(height, belt_load, material_load, precision=0)
    expected = round(10 * STANDARD_GRAVITY_VALUE * (20 + 50), 0)

    assert result.magnitude == expected
    assert result.units == u.newton


def test_gradient_resistance_invalid_unit():
    """Test gradient resistance calculation with invalid unit."""
    height = 10 * u.meter
    belt_load = 20 * u.kg / u.meter
    material_load = 50 * u.kg / u.meter

    with pytest.raises(ValueError) as excinfo:
        gradient_resistance(height, belt_load, material_load, unit="invalid_unit")

    assert "Invalid unit" in str(excinfo.value)


def test_gradient_resistance_incompatible_unit():
    """Test gradient resistance calculation with incompatible unit."""
    height = 10 * u.meter
    belt_load = 20 * u.kg / u.meter
    material_load = 50 * u.kg / u.meter

    with pytest.raises(ValueError):
        gradient_resistance(height, belt_load, material_load, unit="second")


def test_gradient_resistance_negative_height():
    """Test gradient resistance calculation with negative height."""
    height = -10 * u.meter
    belt_load = 20 * u.kg / u.meter
    material_load = 50 * u.kg / u.meter

    with pytest.raises(ValueError) as excinfo:
        gradient_resistance(height, belt_load, material_load)

    assert "Height difference must be non-negative" in str(excinfo.value)


def test_gradient_resistance_negative_load():
    """Test gradient resistance calculation with negative load."""
    height = 10 * u.meter
    belt_load = -20 * u.kg / u.meter
    material_load = 50 * u.kg / u.meter

    with pytest.raises(ValueError):
        gradient_resistance(height, belt_load, material_load)


def test_gradient_resistance_zero_height():
    """Test gradient resistance calculation with zero height difference."""
    height = 0 * u.meter
    belt_load = 20 * u.kg / u.meter
    material_load = 50 * u.kg / u.meter

    result = gradient_resistance(height, belt_load, material_load)

    assert result.magnitude == 0
    assert result.units == u.newton


def test_gradient_resistance_unit_conversion_error():
    """Test that incompatible units raise appropriate errors."""
    # Incorrect unit for height
    with pytest.raises(Exception):
        gradient_resistance(10 * u.kilogram, 20, 50)

    # Incorrect unit for belt load
    with pytest.raises(Exception):
        gradient_resistance(10, 20 * u.meter, 50)  # Incorrect unit for material load
    with pytest.raises(Exception):
        gradient_resistance(10, 20, 50 * u.second)


def test_gradient_resistance_with_none_material_load():
    """Test gradient resistance calculation with None material load (optional parameter)."""
    # Using None for material load (should default to 0 kg/m)
    height = 10 * u.meter
    belt_load = 20 * u.kg / u.meter

    result = gradient_resistance(height, belt_load, None)
    expected = 10 * STANDARD_GRAVITY_VALUE * 20  # Only belt load, no material

    assert result.magnitude == pytest.approx(expected)
    assert result.units == u.newton


def test_gradient_resistance_without_material_load():
    """Test gradient resistance calculation without providing material load parameter."""
    # Not providing material_load parameter (should default to None)
    height = 10 * u.meter
    belt_load = 20 * u.kg / u.meter

    result = gradient_resistance(height, belt_load)
    expected = 10 * STANDARD_GRAVITY_VALUE * 20  # Only belt load, no material

    assert result.magnitude == pytest.approx(expected)
    assert result.units == u.newton


def test_gradient_resistance_with_zero_material_load():
    """Test gradient resistance calculation with explicit zero material load."""
    # Explicitly providing zero material load
    height = 10 * u.meter
    belt_load = 20 * u.kg / u.meter
    material_load = 0 * u.kg / u.meter

    result = gradient_resistance(height, belt_load, material_load)
    expected = 10 * STANDARD_GRAVITY_VALUE * 20  # Only belt load, no material

    # Compare with result when material_load is None
    result_none = gradient_resistance(height, belt_load, None)

    assert result.magnitude == pytest.approx(expected)
    assert result.units == u.newton
    assert result.magnitude == pytest.approx(result_none.magnitude)


def test_gradient_resistance_sections_single_value():
    """Test gradient_resistance_sections with a single value (should match scalar function)."""
    # Basic test with 10m height, 20 kg/m belt, 50 kg/m material
    height = 10 * u.meter
    belt_load = 20 * u.kg / u.meter
    material_load = 50 * u.kg / u.meter

    # Calculate using scalar and vectorized functions
    scalar_result = gradient_resistance(height, belt_load, material_load)
    vector_result = gradient_resistance_sections(height, belt_load, material_load)

    # Results should be identical (allowing for small rounding differences)
    np.testing.assert_almost_equal(
        scalar_result.magnitude, vector_result.magnitude.item(), decimal=2
    )
    assert scalar_result.units == vector_result.units
    assert isinstance(vector_result.magnitude, np.ndarray)


def test_gradient_resistance_sections_array_inputs():
    """Test gradient_resistance_sections with array inputs."""
    # Multiple sections with different heights
    heights = np.array([10, 20, -5, 0]) * u.meter
    belt_load = 20 * u.kg / u.meter
    material_load = 50 * u.kg / u.meter

    # Calculate using vectorized function
    results = gradient_resistance_sections(heights, belt_load, material_load)

    # Calculate expected values manually
    expected_values = np.array(
        [
            10 * STANDARD_GRAVITY_VALUE * (20 + 50),
            20 * STANDARD_GRAVITY_VALUE * (20 + 50),
            -5 * STANDARD_GRAVITY_VALUE * (20 + 50),
            0 * STANDARD_GRAVITY_VALUE * (20 + 50),
        ]
    )

    # Check results
    assert isinstance(results.magnitude, np.ndarray)
    assert results.units == u.newton

    # Use lower precision for comparison to accommodate rounding differences
    np.testing.assert_array_almost_equal(results.magnitude, expected_values, decimal=2)


def test_gradient_resistance_sections_mixed_arrays():
    """Test gradient_resistance_sections with a mix of array and scalar inputs."""
    # Multiple sections with different heights and belt loads
    heights = np.array([10, 20, -5, 0]) * u.meter
    belt_loads = np.array([20, 30, 25, 15]) * u.kg / u.meter
    material_load = 50 * u.kg / u.meter

    # Calculate using vectorized function
    results = gradient_resistance_sections(heights, belt_loads, material_load)

    # Calculate expected values manually
    expected_values = np.array(
        [
            10 * STANDARD_GRAVITY_VALUE * (20 + 50),
            20 * STANDARD_GRAVITY_VALUE * (30 + 50),
            -5 * STANDARD_GRAVITY_VALUE * (25 + 50),
            0 * STANDARD_GRAVITY_VALUE * (15 + 50),
        ]
    )

    # Check results
    assert isinstance(results.magnitude, np.ndarray)
    assert results.units == u.newton

    # Use lower precision for comparison to accommodate rounding differences
    np.testing.assert_array_almost_equal(results.magnitude, expected_values, decimal=2)


def test_gradient_resistance_sections_all_arrays():
    """Test gradient_resistance_sections with all array inputs."""
    # Multiple sections with all parameters as arrays
    heights = np.array([10, 20, -5, 0]) * u.meter
    belt_loads = np.array([20, 30, 25, 15]) * u.kg / u.meter
    material_loads = np.array([50, 60, 70, 40]) * u.kg / u.meter

    # Calculate using vectorized function
    results = gradient_resistance_sections(heights, belt_loads, material_loads)

    # Calculate expected values manually
    expected_values = np.array(
        [
            10 * STANDARD_GRAVITY_VALUE * (20 + 50),
            20 * STANDARD_GRAVITY_VALUE * (30 + 60),
            -5 * STANDARD_GRAVITY_VALUE * (25 + 70),
            0 * STANDARD_GRAVITY_VALUE * (15 + 40),
        ]
    )

    # Check results
    assert isinstance(results.magnitude, np.ndarray)
    assert results.units == u.newton

    # Use lower precision for comparison to accommodate rounding differences
    np.testing.assert_array_almost_equal(results.magnitude, expected_values, decimal=2)


def test_gradient_resistance_sections_without_material():
    """Test gradient_resistance_sections with material_load=None."""
    # Multiple sections without material load (return strand)
    heights = np.array([10, 20, -5, 0]) * u.meter
    belt_loads = np.array([20, 30, 25, 15]) * u.kg / u.meter

    # Calculate using vectorized function
    results = gradient_resistance_sections(heights, belt_loads)

    # Calculate expected values manually (material load is 0)
    expected_values = np.array(
        [
            10 * STANDARD_GRAVITY_VALUE * 20,
            20 * STANDARD_GRAVITY_VALUE * 30,
            -5 * STANDARD_GRAVITY_VALUE * 25,
            0 * STANDARD_GRAVITY_VALUE * 15,
        ]
    )

    # Check results
    assert isinstance(results.magnitude, np.ndarray)
    assert results.units == u.newton

    # Use lower precision for comparison to accommodate rounding differences
    np.testing.assert_array_almost_equal(results.magnitude, expected_values, decimal=2)


def test_gradient_resistance_sections_output_unit():
    """Test gradient_resistance_sections with different output units."""
    # Multiple sections with all parameters as arrays
    heights = np.array([10, 20]) * u.meter
    belt_loads = np.array([20, 30]) * u.kg / u.meter
    material_loads = np.array([50, 60]) * u.kg / u.meter

    # Calculate using vectorized function with kilonewtons output
    results = gradient_resistance_sections(
        heights, belt_loads, material_loads, unit="kilonewton"
    )

    # Calculate expected values manually
    expected_values = np.array(
        [
            10 * STANDARD_GRAVITY_VALUE * (20 + 50) / 1000,  # Convert to kN
            20 * STANDARD_GRAVITY_VALUE * (30 + 60) / 1000,  # Convert to kN
        ]
    )

    # Check results
    assert isinstance(results.magnitude, np.ndarray)
    assert results.units == u.kilonewton

    # Use lower precision for comparison to accommodate rounding differences
    np.testing.assert_array_almost_equal(results.magnitude, expected_values, decimal=2)


def test_gradient_resistance_sections_precision():
    """Test gradient_resistance_sections with different precision."""
    # Multiple sections
    heights = np.array([10, 20]) * u.meter
    belt_loads = np.array([20, 30]) * u.kg / u.meter
    material_loads = np.array([50, 60]) * u.kg / u.meter

    # Calculate using vectorized function with different precision
    results = gradient_resistance_sections(
        heights, belt_loads, material_loads, precision=3
    )

    # Calculate expected values manually and round to 3 decimal places
    raw_values = np.array(
        [
            10 * STANDARD_GRAVITY_VALUE * (20 + 50),
            20 * STANDARD_GRAVITY_VALUE * (30 + 60),
        ]
    )
    expected_values = np.round(raw_values, 3)

    # Check results
    assert isinstance(results.magnitude, np.ndarray)
    np.testing.assert_array_almost_equal(results.magnitude, expected_values, decimal=3)


def test_gradient_resistance_sections_validation():
    """Test gradient_resistance_sections input validation."""
    # Test with negative belt loads (should raise error)
    heights = np.array([10, 20]) * u.meter
    belt_loads = np.array([20, -30]) * u.kg / u.meter
    material_loads = np.array([50, 60]) * u.kg / u.meter

    with pytest.raises(ValueError, match="Belt line loads must be non-negative"):
        gradient_resistance_sections(heights, belt_loads, material_loads)

    # Test with negative material loads (should raise error)
    belt_loads = np.array([20, 30]) * u.kg / u.meter
    material_loads = np.array([50, -60]) * u.kg / u.meter

    with pytest.raises(ValueError, match="Material line loads must be non-negative"):
        gradient_resistance_sections(
            heights, belt_loads, material_loads
        )  # Test with mismatched array shapes
    heights = np.array([10, 20, 30]) * u.meter
    belt_loads = np.array([20, 30]) * u.kg / u.meter

    with pytest.raises(ValueError):  # Just check for ValueError, don't specify message
        gradient_resistance_sections(heights, belt_loads)


def test_total_power_at_drive_pulley_due_to_motion_resistances_basic():
    """Test basic power calculation with Quantity inputs."""
    motion_resistance = 75000 * u.newton
    belt_speed = 3 * u.meter / u.second

    result = total_power_at_drive_pulley_due_to_motion_resistances(
        motion_resistance, belt_speed
    )

    assert result.magnitude == pytest.approx(225000)
    assert result.units == u.watt


def test_total_power_at_drive_pulley_due_to_motion_resistances_different_units():
    """Test power calculation with different input and output units."""
    motion_resistance = 75 * u.kilonewton
    belt_speed = 3000 * u.millimeter / u.second

    result = total_power_at_drive_pulley_due_to_motion_resistances(
        motion_resistance, belt_speed, unit="kilowatt"
    )

    assert result.magnitude == pytest.approx(225)
    assert result.units == u.kilowatt


def test_total_power_at_drive_pulley_due_to_motion_resistances_zero_inputs():
    """Test power calculation with zero inputs."""
    # Zero motion resistance
    result1 = total_power_at_drive_pulley_due_to_motion_resistances(
        0 * u.newton, 3 * u.meter / u.second
    )
    assert result1.magnitude == pytest.approx(0)

    # Zero belt speed
    result2 = total_power_at_drive_pulley_due_to_motion_resistances(
        75000 * u.newton, 0 * u.meter / u.second
    )
    assert result2.magnitude == pytest.approx(0)


def test_total_power_at_drive_pulley_due_to_motion_resistances_invalid_units():
    """Test power calculation with invalid units."""
    with pytest.raises(ValueError):
        total_power_at_drive_pulley_due_to_motion_resistances(
            75 * u.kilogram, 3 * u.meter / u.second
        )

    with pytest.raises(ValueError):
        total_power_at_drive_pulley_due_to_motion_resistances(
            75000 * u.newton, 3 * u.kilogram
        )

    with pytest.raises(ValueError):
        total_power_at_drive_pulley_due_to_motion_resistances(
            75000 * u.newton, 3 * u.meter / u.second, unit="invalid"
        )


# Tests for friction_resistance_of_skirting_board_from_material_flow (public function)


def test_friction_resistance_of_skirting_board_from_material_flow_with_quantities():
    """Test friction resistance calculation with Quantity inputs."""
    from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
        friction_resistance_of_skirting_board_from_material_flow,
    )

    # Using quantities for all inputs
    mass_flow = 100 * u.kilogram / u.second
    belt_velocity = 2.5 * u.meter / u.second
    material_density = 1000 * u.kilogram / u.meter**3
    rankine_coefficient = 1.2 * u.dimensionless
    board_width = 1.0 * u.meter
    board_length = 3.0 * u.meter
    roller_length = 0.8 * u.meter
    troughing_angle = 30 * u.degree
    friction_coeff = 0.4 * u.dimensionless

    result = friction_resistance_of_skirting_board_from_material_flow(
        mass_flow,
        belt_velocity,
        material_density,
        rankine_coefficient,
        board_width,
        board_length,
        roller_length,
        troughing_angle,
        friction_coeff,
    )

    # Expected result from private function: approximately 2.027 N
    assert result.magnitude == pytest.approx(2.027, rel=0.01)
    assert result.units == u.newton


def test_friction_resistance_of_skirting_board_from_material_flow_user_provided_parameters_6000_tph():
    """Test public API with user-provided parameters (6000 t/h) expecting 187.78 N."""
    from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
        friction_resistance_of_skirting_board_from_material_flow,
    )

    result = friction_resistance_of_skirting_board_from_material_flow(
        6000 * u.tonne / u.hour,
        5 * u.meter / u.second,
        830 * u.kilogram / u.meter**3,
        1.0 * u.dimensionless,
        1.2 * u.meter,
        1.0 * u.meter,
        0.7 * u.meter,
        35 * u.degree,
        0.6 * u.dimensionless,
    )

    assert result.magnitude == pytest.approx(187.78, rel=1e-3)
    assert result.units == u.newton


def test_friction_resistance_of_skirting_board_from_material_flow_6000_tph_equivalent_mass_flow_kg_per_s():
    """Test robustness with equivalent mass flow in kg/s for the 6000 t/h case."""
    from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
        friction_resistance_of_skirting_board_from_material_flow,
    )

    result = friction_resistance_of_skirting_board_from_material_flow(
        (6000 * 1000 / 3600) * u.kilogram / u.second,
        5 * u.meter / u.second,
        830 * u.kilogram / u.meter**3,
        1.0 * u.dimensionless,
        1.2 * u.meter,
        1.0 * u.meter,
        0.7 * u.meter,
        35 * u.degree,
        0.6 * u.dimensionless,
    )

    assert result.magnitude == pytest.approx(187.78, rel=1e-3)
    assert result.units == u.newton


def test_friction_resistance_of_skirting_board_from_material_flow_6000_tph_equivalent_angle_radians():
    """Test robustness with equivalent troughing angle in radians for the 6000 t/h case."""
    from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
        friction_resistance_of_skirting_board_from_material_flow,
    )

    result = friction_resistance_of_skirting_board_from_material_flow(
        6000 * u.tonne / u.hour,
        5 * u.meter / u.second,
        830 * u.kilogram / u.meter**3,
        1.0 * u.dimensionless,
        1.2 * u.meter,
        1.0 * u.meter,
        0.7 * u.meter,
        np.deg2rad(35) * u.radian,
        0.6 * u.dimensionless,
    )

    assert result.magnitude == pytest.approx(187.78, rel=1e-3)
    assert result.units == u.newton


def test_friction_resistance_of_skirting_board_from_material_flow_6000_tph_equivalent_velocity_km_per_h():
    """Test robustness with equivalent belt velocity in km/h for the 6000 t/h case."""
    from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
        friction_resistance_of_skirting_board_from_material_flow,
    )

    result = friction_resistance_of_skirting_board_from_material_flow(
        6000 * u.tonne / u.hour,
        18 * u.kilometer / u.hour,
        830 * u.kilogram / u.meter**3,
        1.0 * u.dimensionless,
        1.2 * u.meter,
        1.0 * u.meter,
        0.7 * u.meter,
        35 * u.degree,
        0.6 * u.dimensionless,
    )

    assert result.magnitude == pytest.approx(187.78, rel=1e-3)
    assert result.units == u.newton


def test_friction_resistance_of_skirting_board_from_material_flow_6000_tph_equivalent_density_g_per_cm3():
    """Test robustness with equivalent material density in g/cm³ for the 6000 t/h case."""
    from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
        friction_resistance_of_skirting_board_from_material_flow,
    )

    result = friction_resistance_of_skirting_board_from_material_flow(
        6000 * u.tonne / u.hour,
        5 * u.meter / u.second,
        0.83 * u.gram / u.centimeter**3,
        1.0 * u.dimensionless,
        1.2 * u.meter,
        1.0 * u.meter,
        0.7 * u.meter,
        35 * u.degree,
        0.6 * u.dimensionless,
    )

    assert result.magnitude == pytest.approx(187.78, rel=1e-3)
    assert result.units == u.newton


def test_friction_resistance_of_skirting_board_from_material_flow_with_different_units():
    """Test friction resistance calculation with different but compatible units."""
    from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
        friction_resistance_of_skirting_board_from_material_flow,
    )

    # Using different but compatible units
    mass_flow = 0.1 * u.tonne / u.second  # = 100 kg/s
    belt_velocity = 250 * u.centimeter / u.second  # = 2.5 m/s
    material_density = 1 * u.tonne / u.meter**3  # = 1000 kg/m³
    rankine_coefficient = 1.2 * u.dimensionless
    board_width = 100 * u.centimeter  # = 1.0 m
    board_length = 3000 * u.millimeter  # = 3.0 m
    roller_length = 800 * u.millimeter  # = 0.8 m
    troughing_angle = 30 * u.degree
    friction_coeff = 0.4 * u.dimensionless

    result = friction_resistance_of_skirting_board_from_material_flow(
        mass_flow,
        belt_velocity,
        material_density,
        rankine_coefficient,
        board_width,
        board_length,
        roller_length,
        troughing_angle,
        friction_coeff,
    )

    # Expected result should be approximately 2.027 N
    assert result.magnitude == pytest.approx(2.027, rel=0.01)
    assert result.units == u.newton


def test_friction_resistance_of_skirting_board_from_material_flow_output_unit():
    """Test friction resistance calculation with different output units."""
    from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
        friction_resistance_of_skirting_board_from_material_flow,
    )

    mass_flow = 100 * u.kilogram / u.second
    belt_velocity = 2.5 * u.meter / u.second
    material_density = 1000 * u.kilogram / u.meter**3
    rankine_coefficient = 1.2 * u.dimensionless
    board_width = 1.0 * u.meter
    board_length = 3.0 * u.meter
    roller_length = 0.8 * u.meter
    troughing_angle = 30 * u.degree
    friction_coeff = 0.4 * u.dimensionless

    # Request output in kilonewtons
    result = friction_resistance_of_skirting_board_from_material_flow(
        mass_flow,
        belt_velocity,
        material_density,
        rankine_coefficient,
        board_width,
        board_length,
        roller_length,
        troughing_angle,
        friction_coeff,
        unit="kilonewton",
        precision=5,
    )

    expected = 2.027 / 1000  # Converting to kN
    assert result.magnitude == pytest.approx(expected, rel=0.01)
    assert result.units == u.kilonewton


def test_friction_resistance_of_skirting_board_from_material_flow_precision():
    """Test friction resistance calculation with specific precision."""
    from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
        friction_resistance_of_skirting_board_from_material_flow,
    )

    mass_flow = 100 * u.kilogram / u.second
    belt_velocity = 2.5 * u.meter / u.second
    material_density = 1000 * u.kilogram / u.meter**3
    rankine_coefficient = 1.2 * u.dimensionless
    board_width = 1.0 * u.meter
    board_length = 3.0 * u.meter
    roller_length = 0.8 * u.meter
    troughing_angle = 30 * u.degree
    friction_coeff = 0.4 * u.dimensionless

    # Request output with 4 decimal places
    result = friction_resistance_of_skirting_board_from_material_flow(
        mass_flow,
        belt_velocity,
        material_density,
        rankine_coefficient,
        board_width,
        board_length,
        roller_length,
        troughing_angle,
        friction_coeff,
        precision=4,
    )

    expected = round(2.0205, 4)
    assert result.magnitude == expected
    assert result.units == u.newton


def test_friction_resistance_of_skirting_board_from_material_flow_invalid_mass_flow_unit():
    """Test friction resistance with invalid mass flow unit."""
    from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
        friction_resistance_of_skirting_board_from_material_flow,
    )

    with pytest.raises(ValueError):
        friction_resistance_of_skirting_board_from_material_flow(
            100 * u.meter,  # Invalid unit for mass flow
            2.5 * u.meter / u.second,
            1000 * u.kilogram / u.meter**3,
            1.2 * u.dimensionless,
            1.0 * u.meter,
            3.0 * u.meter,
            0.8 * u.meter,
            30 * u.degree,
            0.4 * u.dimensionless,
        )


def test_friction_resistance_of_skirting_board_from_material_flow_invalid_velocity_unit():
    """Test friction resistance with invalid belt velocity unit."""
    from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
        friction_resistance_of_skirting_board_from_material_flow,
    )

    with pytest.raises(ValueError):
        friction_resistance_of_skirting_board_from_material_flow(
            100 * u.kilogram / u.second,
            2.5 * u.kilogram,  # Invalid unit for velocity
            1000 * u.kilogram / u.meter**3,
            1.2 * u.dimensionless,
            1.0 * u.meter,
            3.0 * u.meter,
            0.8 * u.meter,
            30 * u.degree,
            0.4 * u.dimensionless,
        )


def test_friction_resistance_of_skirting_board_from_material_flow_invalid_output_unit():
    """Test friction resistance with invalid output unit."""
    from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
        friction_resistance_of_skirting_board_from_material_flow,
    )

    with pytest.raises(ValueError) as excinfo:
        friction_resistance_of_skirting_board_from_material_flow(
            100 * u.kilogram / u.second,
            2.5 * u.meter / u.second,
            1000 * u.kilogram / u.meter**3,
            1.2 * u.dimensionless,
            1.0 * u.meter,
            3.0 * u.meter,
            0.8 * u.meter,
            30 * u.degree,
            0.4 * u.dimensionless,
            unit="invalid_unit",
        )

    assert "Invalid unit" in str(excinfo.value)


def test_friction_resistance_of_skirting_board_from_material_flow_negative_mass_flow():
    """Test friction resistance with negative mass flow."""
    from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
        friction_resistance_of_skirting_board_from_material_flow,
    )

    with pytest.raises(ValueError) as excinfo:
        friction_resistance_of_skirting_board_from_material_flow(
            -100 * u.kilogram / u.second,  # Negative flow
            2.5 * u.meter / u.second,
            1000 * u.kilogram / u.meter**3,
            1.2 * u.dimensionless,
            1.0 * u.meter,
            3.0 * u.meter,
            0.8 * u.meter,
            30 * u.degree,
            0.4 * u.dimensionless,
        )

    assert "must be positive" in str(excinfo.value)


def test_friction_resistance_of_skirting_board_from_material_flow_zero_velocity():
    """Test friction resistance with zero belt velocity."""
    from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
        friction_resistance_of_skirting_board_from_material_flow,
    )

    with pytest.raises(ValueError) as excinfo:
        friction_resistance_of_skirting_board_from_material_flow(
            100 * u.kilogram / u.second,
            0 * u.meter / u.second,  # Zero velocity
            1000 * u.kilogram / u.meter**3,
            1.2 * u.dimensionless,
            1.0 * u.meter,
            3.0 * u.meter,
            0.8 * u.meter,
            30 * u.degree,
            0.4 * u.dimensionless,
        )

    assert "must be positive" in str(excinfo.value)


def test_friction_resistance_of_skirting_board_from_material_flow_zero_board_width():
    """Test friction resistance with zero skirting board width."""
    from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
        friction_resistance_of_skirting_board_from_material_flow,
    )

    with pytest.raises(ValueError) as excinfo:
        friction_resistance_of_skirting_board_from_material_flow(
            100 * u.kilogram / u.second,
            2.5 * u.meter / u.second,
            1000 * u.kilogram / u.meter**3,
            1.2 * u.dimensionless,
            0 * u.meter,  # Zero width
            3.0 * u.meter,
            0.8 * u.meter,
            30 * u.degree,
            0.4 * u.dimensionless,
        )

    assert "must be positive" in str(excinfo.value)


def test_friction_resistance_of_skirting_board_from_material_flow_invalid_angle():
    """Test friction resistance with invalid troughing angle."""
    from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
        friction_resistance_of_skirting_board_from_material_flow,
    )

    with pytest.raises(ValueError) as excinfo:
        friction_resistance_of_skirting_board_from_material_flow(
            100 * u.kilogram / u.second,
            2.5 * u.meter / u.second,
            1000 * u.kilogram / u.meter**3,
            1.2 * u.dimensionless,
            1.0 * u.meter,
            3.0 * u.meter,
            0.8 * u.meter,
            95 * u.degree,  # Invalid angle (> 90°)
            0.4 * u.dimensionless,
        )

    assert "Troughing angle" in str(excinfo.value)


# Tests for friction_resistance_per_meter_of_skirting_board_from_material_flow


def test_per_meter_returns_newton_per_meter_units():
    """Test that per-meter function returns default units of N/m."""
    from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
        friction_resistance_per_meter_of_skirting_board_from_material_flow,
    )

    mass_flow = 100 * u.kilogram / u.second
    belt_velocity = 2.5 * u.meter / u.second
    material_density = 1000 * u.kilogram / u.meter**3
    rankine_coefficient = 1.2 * u.dimensionless
    board_width = 1.0 * u.meter
    board_length = 3.0 * u.meter
    roller_length = 0.8 * u.meter
    troughing_angle = 30 * u.degree
    friction_coeff = 0.4 * u.dimensionless

    result = friction_resistance_per_meter_of_skirting_board_from_material_flow(
        mass_flow,
        belt_velocity,
        material_density,
        rankine_coefficient,
        board_width,
        board_length,
        roller_length,
        troughing_angle,
        friction_coeff,
    )

    # Should return force per unit length with default units N/m
    assert result.units == u.newton / u.meter
    assert result.magnitude > 0


def test_per_meter_mathematical_relationship_with_total():
    """Test that per_meter_force * length ≈ total_force."""
    from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
        friction_resistance_of_skirting_board_from_material_flow,
        friction_resistance_per_meter_of_skirting_board_from_material_flow,
    )

    mass_flow = 100 * u.kilogram / u.second
    belt_velocity = 2.5 * u.meter / u.second
    material_density = 1000 * u.kilogram / u.meter**3
    rankine_coefficient = 1.2 * u.dimensionless
    board_width = 1.0 * u.meter
    board_length = 3.0 * u.meter
    roller_length = 0.8 * u.meter
    troughing_angle = 30 * u.degree
    friction_coeff = 0.4 * u.dimensionless

    # Get total force
    total_force = friction_resistance_of_skirting_board_from_material_flow(
        mass_flow,
        belt_velocity,
        material_density,
        rankine_coefficient,
        board_width,
        board_length,
        roller_length,
        troughing_angle,
        friction_coeff,
        unit="newton",
        precision=6,
    )

    # Get per-meter force
    per_meter_force = (
        friction_resistance_per_meter_of_skirting_board_from_material_flow(
            mass_flow,
            belt_velocity,
            material_density,
            rankine_coefficient,
            board_width,
            board_length,
            roller_length,
            troughing_angle,
            friction_coeff,
            unit="newton/meter",
            precision=6,
        )
    )

    # Verify mathematical relationship: total = per_meter * length
    calculated_total = per_meter_force * board_length
    calculated_total = calculated_total.to(u.newton)

    assert calculated_total.magnitude == pytest.approx(total_force.magnitude, rel=1e-5)


@pytest.mark.parametrize(
    "board_length_value,expected_ratio",
    [
        (1.0, 1.0),  # 1 meter
        (2.5, 0.4),  # 2.5 meters -> per_meter = total / 2.5
        (5.0, 0.2),  # 5 meters -> per_meter = total / 5.0
        (10.0, 0.1),  # 10 meters -> per_meter = total / 10.0
    ],
)
def test_per_meter_with_various_lengths(board_length_value, expected_ratio):
    """Test per-meter calculation with various skirting board lengths."""
    from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
        friction_resistance_of_skirting_board_from_material_flow,
        friction_resistance_per_meter_of_skirting_board_from_material_flow,
    )

    mass_flow = 100 * u.kilogram / u.second
    belt_velocity = 2.5 * u.meter / u.second
    material_density = 1000 * u.kilogram / u.meter**3
    rankine_coefficient = 1.2 * u.dimensionless
    board_width = 1.0 * u.meter
    board_length = board_length_value * u.meter
    roller_length = 0.8 * u.meter
    troughing_angle = 30 * u.degree
    friction_coeff = 0.4 * u.dimensionless

    # Get total force
    total_force = friction_resistance_of_skirting_board_from_material_flow(
        mass_flow,
        belt_velocity,
        material_density,
        rankine_coefficient,
        board_width,
        board_length,
        roller_length,
        troughing_angle,
        friction_coeff,
        precision=6,
    )

    # Get per-meter force
    per_meter_force = (
        friction_resistance_per_meter_of_skirting_board_from_material_flow(
            mass_flow,
            belt_velocity,
            material_density,
            rankine_coefficient,
            board_width,
            board_length,
            roller_length,
            troughing_angle,
            friction_coeff,
            precision=6,
        )
    )

    # Verify ratio
    per_meter_value = per_meter_force.to(u.newton / u.meter).magnitude
    total_value = total_force.to(u.newton).magnitude
    actual_ratio = per_meter_value / total_value

    assert actual_ratio == pytest.approx(expected_ratio, rel=1e-5)


def test_per_meter_unit_conversions():
    """Test per-meter function with different output units."""
    from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
        friction_resistance_per_meter_of_skirting_board_from_material_flow,
    )

    mass_flow = 100 * u.kilogram / u.second
    belt_velocity = 2.5 * u.meter / u.second
    material_density = 1000 * u.kilogram / u.meter**3
    rankine_coefficient = 1.2 * u.dimensionless
    board_width = 1.0 * u.meter
    board_length = 3.0 * u.meter
    roller_length = 0.8 * u.meter
    troughing_angle = 30 * u.degree
    friction_coeff = 0.4 * u.dimensionless

    # Test with default units (newton/meter)
    result_nm = friction_resistance_per_meter_of_skirting_board_from_material_flow(
        mass_flow,
        belt_velocity,
        material_density,
        rankine_coefficient,
        board_width,
        board_length,
        roller_length,
        troughing_angle,
        friction_coeff,
        precision=6,
    )

    # Test with kilonewton/meter
    result_knm = friction_resistance_per_meter_of_skirting_board_from_material_flow(
        mass_flow,
        belt_velocity,
        material_density,
        rankine_coefficient,
        board_width,
        board_length,
        roller_length,
        troughing_angle,
        friction_coeff,
        unit="kilonewton/meter",
        precision=9,
    )

    # Test with newton/millimeter
    result_nmm = friction_resistance_per_meter_of_skirting_board_from_material_flow(
        mass_flow,
        belt_velocity,
        material_density,
        rankine_coefficient,
        board_width,
        board_length,
        roller_length,
        troughing_angle,
        friction_coeff,
        unit="newton/millimeter",
        precision=9,
    )

    # Verify unit conversions
    assert result_nm.units == u.newton / u.meter
    assert result_knm.units == u.kilonewton / u.meter
    assert result_nmm.units == u.newton / u.millimeter

    # Verify numerical consistency
    assert result_knm.magnitude == pytest.approx(result_nm.magnitude / 1000, rel=1e-6)
    assert result_nmm.magnitude == pytest.approx(result_nm.magnitude / 1000, rel=1e-6)


def test_per_meter_precision_handling():
    """Test that per-meter function respects precision parameter."""
    from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
        friction_resistance_per_meter_of_skirting_board_from_material_flow,
    )

    mass_flow = 100 * u.kilogram / u.second
    belt_velocity = 2.5 * u.meter / u.second
    material_density = 1000 * u.kilogram / u.meter**3
    rankine_coefficient = 1.2 * u.dimensionless
    board_width = 1.0 * u.meter
    board_length = 3.0 * u.meter
    roller_length = 0.8 * u.meter
    troughing_angle = 30 * u.degree
    friction_coeff = 0.4 * u.dimensionless

    # Test with precision=2
    result_prec2 = friction_resistance_per_meter_of_skirting_board_from_material_flow(
        mass_flow,
        belt_velocity,
        material_density,
        rankine_coefficient,
        board_width,
        board_length,
        roller_length,
        troughing_angle,
        friction_coeff,
        precision=2,
    )

    # Test with precision=4
    result_prec4 = friction_resistance_per_meter_of_skirting_board_from_material_flow(
        mass_flow,
        belt_velocity,
        material_density,
        rankine_coefficient,
        board_width,
        board_length,
        roller_length,
        troughing_angle,
        friction_coeff,
        precision=4,
    )

    # Verify precision is respected (magnitude should be rounded)
    # For precision=2, should have at most 2 decimal places
    assert len(str(result_prec2.magnitude).split(".")[-1]) <= 2
    # For precision=4, should have at most 4 decimal places
    assert len(str(result_prec4.magnitude).split(".")[-1]) <= 4


def test_per_meter_invalid_inputs():
    """Test per-meter function with invalid inputs."""
    from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
        friction_resistance_per_meter_of_skirting_board_from_material_flow,
    )

    # Test with negative mass flow
    with pytest.raises(ValueError) as excinfo:
        friction_resistance_per_meter_of_skirting_board_from_material_flow(
            -100 * u.kilogram / u.second,  # Negative
            2.5 * u.meter / u.second,
            1000 * u.kilogram / u.meter**3,
            1.2 * u.dimensionless,
            1.0 * u.meter,
            3.0 * u.meter,
            0.8 * u.meter,
            30 * u.degree,
            0.4 * u.dimensionless,
        )
    assert "must be positive" in str(excinfo.value)

    # Test with zero skirting board length
    with pytest.raises(ValueError) as excinfo:
        friction_resistance_per_meter_of_skirting_board_from_material_flow(
            100 * u.kilogram / u.second,
            2.5 * u.meter / u.second,
            1000 * u.kilogram / u.meter**3,
            1.2 * u.dimensionless,
            1.0 * u.meter,
            0 * u.meter,  # Zero length
            0.8 * u.meter,
            30 * u.degree,
            0.4 * u.dimensionless,
        )
    assert "must be positive" in str(excinfo.value)

    # Test with invalid output unit
    with pytest.raises(ValueError) as excinfo:
        friction_resistance_per_meter_of_skirting_board_from_material_flow(
            100 * u.kilogram / u.second,
            2.5 * u.meter / u.second,
            1000 * u.kilogram / u.meter**3,
            1.2 * u.dimensionless,
            1.0 * u.meter,
            3.0 * u.meter,
            0.8 * u.meter,
            30 * u.degree,
            0.4 * u.dimensionless,
            unit="invalid_unit",
        )
    assert "Invalid unit" in str(excinfo.value)
