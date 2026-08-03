"""Tests for the validate_positive_count helper in main.validation module."""

import pytest
from eytelwein.main.validation import validate_positive_count


class TestValidatePositiveCount:
    """Test suite for validate_positive_count function."""

    def test_validate_positive_count_valid_integers(self):
        """Valid positive integers should not raise."""
        validate_positive_count(1, "test_param")
        validate_positive_count(10, "test_param")
        validate_positive_count(1000, "test_param")

    def test_validate_positive_count_zero_raises(self):
        """Zero should raise ValueError."""
        with pytest.raises(ValueError, match="must be a positive integer"):
            validate_positive_count(0, "test_param")

    def test_validate_positive_count_negative_raises(self):
        """Negative integers should raise ValueError."""
        with pytest.raises(ValueError, match="must be a positive integer"):
            validate_positive_count(-1, "test_param")

        with pytest.raises(ValueError, match="must be a positive integer"):
            validate_positive_count(-100, "test_param")

    def test_validate_positive_count_bool_raises(self):
        """Boolean values (subclass of int) should raise ValueError."""
        with pytest.raises(ValueError, match="must be an integer"):
            validate_positive_count(True, "test_param")

        with pytest.raises(ValueError, match="must be an integer"):
            validate_positive_count(False, "test_param")

    def test_validate_positive_count_float_raises(self):
        """Float values should raise ValueError."""
        with pytest.raises(ValueError, match="must be an integer"):
            validate_positive_count(1.5, "test_param")

        with pytest.raises(ValueError, match="must be an integer"):
            validate_positive_count(10.0, "test_param")

    def test_validate_positive_count_string_raises(self):
        """String values should raise ValueError."""
        with pytest.raises(ValueError, match="must be an integer"):
            validate_positive_count("5", "test_param")

    def test_validate_positive_count_custom_param_name_in_error(self):
        """Error message should include custom parameter name."""
        with pytest.raises(ValueError, match="strand_count"):
            validate_positive_count(-1, "strand_count")

        with pytest.raises(ValueError, match="quantity_of_drives"):
            validate_positive_count(0, "quantity_of_drives")

    def test_validate_positive_count_default_param_name(self):
        """Default parameter name 'count' should be used when not specified."""
        with pytest.raises(ValueError, match="count"):
            validate_positive_count(0)
