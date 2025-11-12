# ABOUTME: Unit tests for basic real-valued CDL blocks.
# ABOUTME: Tests arithmetic operations (Add, Subtract, Multiply, Divide).

import pytest
from cdl_python.CDL.Reals.Add import Add
from cdl_python.CDL.Reals.Subtract import Subtract
from cdl_python.CDL.Reals.Multiply import Multiply
from cdl_python.CDL.Reals.Divide import Divide


class TestAdd:
    """Tests for Add block"""

    def test_add_positive_numbers(self):
        """Test adding positive numbers"""
        block = Add()
        result = block.compute(u1=2.0, u2=3.0)
        assert result['y'] == 5.0

    def test_add_negative_numbers(self):
        """Test adding negative numbers"""
        block = Add()
        result = block.compute(u1=-2.0, u2=-3.0)
        assert result['y'] == -5.0

    def test_add_mixed_signs(self):
        """Test adding positive and negative"""
        block = Add()
        result = block.compute(u1=5.0, u2=-3.0)
        assert result['y'] == 2.0

    def test_add_with_zero(self):
        """Test adding with zero"""
        block = Add()
        result = block.compute(u1=5.0, u2=0.0)
        assert result['y'] == 5.0

    def test_add_floating_point(self):
        """Test floating point addition"""
        block = Add()
        result = block.compute(u1=1.5, u2=2.7)
        assert abs(result['y'] - 4.2) < 1e-10


class TestSubtract:
    """Tests for Subtract block"""

    def test_subtract_positive_numbers(self):
        """Test subtracting positive numbers"""
        block = Subtract()
        result = block.compute(u1=5.0, u2=3.0)
        assert result['y'] == 2.0

    def test_subtract_negative_result(self):
        """Test subtraction resulting in negative"""
        block = Subtract()
        result = block.compute(u1=3.0, u2=5.0)
        assert result['y'] == -2.0

    def test_subtract_negative_numbers(self):
        """Test subtracting negative numbers"""
        block = Subtract()
        result = block.compute(u1=-2.0, u2=-5.0)
        assert result['y'] == 3.0

    def test_subtract_from_zero(self):
        """Test subtracting from zero"""
        block = Subtract()
        result = block.compute(u1=0.0, u2=5.0)
        assert result['y'] == -5.0

    def test_subtract_zero(self):
        """Test subtracting zero"""
        block = Subtract()
        result = block.compute(u1=5.0, u2=0.0)
        assert result['y'] == 5.0


class TestMultiply:
    """Tests for Multiply block"""

    def test_multiply_positive_numbers(self):
        """Test multiplying positive numbers"""
        block = Multiply()
        result = block.compute(u1=3.0, u2=4.0)
        assert result['y'] == 12.0

    def test_multiply_negative_numbers(self):
        """Test multiplying negative numbers"""
        block = Multiply()
        result = block.compute(u1=-3.0, u2=-4.0)
        assert result['y'] == 12.0

    def test_multiply_mixed_signs(self):
        """Test multiplying positive and negative"""
        block = Multiply()
        result = block.compute(u1=3.0, u2=-4.0)
        assert result['y'] == -12.0

    def test_multiply_by_zero(self):
        """Test multiplying by zero"""
        block = Multiply()
        result = block.compute(u1=5.0, u2=0.0)
        assert result['y'] == 0.0

    def test_multiply_by_one(self):
        """Test multiplying by one"""
        block = Multiply()
        result = block.compute(u1=5.0, u2=1.0)
        assert result['y'] == 5.0

    def test_multiply_decimals(self):
        """Test multiplying decimal numbers"""
        block = Multiply()
        result = block.compute(u1=2.5, u2=4.0)
        assert result['y'] == 10.0


class TestDivide:
    """Tests for Divide block"""

    def test_divide_positive_numbers(self):
        """Test dividing positive numbers"""
        block = Divide()
        result = block.compute(u1=10.0, u2=2.0)
        assert result['y'] == 5.0

    def test_divide_negative_numbers(self):
        """Test dividing negative numbers"""
        block = Divide()
        result = block.compute(u1=-10.0, u2=-2.0)
        assert result['y'] == 5.0

    def test_divide_mixed_signs(self):
        """Test dividing positive by negative"""
        block = Divide()
        result = block.compute(u1=10.0, u2=-2.0)
        assert result['y'] == -5.0

    def test_divide_by_one(self):
        """Test dividing by one"""
        block = Divide()
        result = block.compute(u1=5.0, u2=1.0)
        assert result['y'] == 5.0

    def test_divide_zero_by_number(self):
        """Test dividing zero by number"""
        block = Divide()
        result = block.compute(u1=0.0, u2=5.0)
        assert result['y'] == 0.0

    def test_divide_by_zero_raises(self):
        """Test that dividing by zero raises error"""
        block = Divide()
        with pytest.raises(ZeroDivisionError):
            block.compute(u1=5.0, u2=0.0)

    def test_divide_fractional_result(self):
        """Test division with fractional result"""
        block = Divide()
        result = block.compute(u1=7.0, u2=2.0)
        assert result['y'] == 3.5
