# ABOUTME: Test suite for additional integer blocks (comparisons, MultiSum, AddParameter, etc.)
# ABOUTME: Tests integer operations and threshold comparisons
import pytest
from cdl_python.CDL.Integers import (
    AddParameter, GreaterEqual, GreaterEqualThreshold, GreaterThreshold,
    LessEqual, LessEqualThreshold, LessThreshold, MultiSum
)


class TestAddParameter:
    """Test the AddParameter block"""

    def test_add_parameter_positive(self):
        """Test AddParameter with positive parameter"""
        add_param = AddParameter(p=10)
        result = add_param.compute(u=5)
        assert result['y'] == 15

    def test_add_parameter_negative(self):
        """Test AddParameter with negative parameter"""
        add_param = AddParameter(p=-5)
        result = add_param.compute(u=10)
        assert result['y'] == 5

    def test_add_parameter_zero(self):
        """Test AddParameter with zero parameter"""
        add_param = AddParameter(p=0)
        result = add_param.compute(u=7)
        assert result['y'] == 7


class TestGreaterEqual:
    """Test the GreaterEqual comparison block"""

    def test_greater_equal_true_greater(self):
        """Test u1 > u2"""
        ge = GreaterEqual()
        result = ge.compute(u1=10, u2=5)
        assert result['y'] is True

    def test_greater_equal_true_equal(self):
        """Test u1 == u2"""
        ge = GreaterEqual()
        result = ge.compute(u1=5, u2=5)
        assert result['y'] is True

    def test_greater_equal_false(self):
        """Test u1 < u2"""
        ge = GreaterEqual()
        result = ge.compute(u1=3, u2=7)
        assert result['y'] is False

    def test_greater_equal_negative(self):
        """Test with negative numbers"""
        ge = GreaterEqual()
        result = ge.compute(u1=-2, u2=-5)
        assert result['y'] is True


class TestGreaterEqualThreshold:
    """Test the GreaterEqualThreshold block"""

    def test_greater_equal_threshold_true_greater(self):
        """Test u > t"""
        get = GreaterEqualThreshold(t=10)
        result = get.compute(u=15)
        assert result['y'] is True

    def test_greater_equal_threshold_true_equal(self):
        """Test u == t"""
        get = GreaterEqualThreshold(t=10)
        result = get.compute(u=10)
        assert result['y'] is True

    def test_greater_equal_threshold_false(self):
        """Test u < t"""
        get = GreaterEqualThreshold(t=10)
        result = get.compute(u=5)
        assert result['y'] is False

    def test_greater_equal_threshold_default(self):
        """Test default threshold (0)"""
        get = GreaterEqualThreshold()
        result = get.compute(u=0)
        assert result['y'] is True


class TestGreaterThreshold:
    """Test the GreaterThreshold block"""

    def test_greater_threshold_true(self):
        """Test u > t"""
        gt = GreaterThreshold(t=10)
        result = gt.compute(u=15)
        assert result['y'] is True

    def test_greater_threshold_equal(self):
        """Test u == t (should be false)"""
        gt = GreaterThreshold(t=10)
        result = gt.compute(u=10)
        assert result['y'] is False

    def test_greater_threshold_false(self):
        """Test u < t"""
        gt = GreaterThreshold(t=10)
        result = gt.compute(u=5)
        assert result['y'] is False


class TestLessEqual:
    """Test the LessEqual comparison block"""

    def test_less_equal_true_less(self):
        """Test u1 < u2"""
        le = LessEqual()
        result = le.compute(u1=3, u2=7)
        assert result['y'] is True

    def test_less_equal_true_equal(self):
        """Test u1 == u2"""
        le = LessEqual()
        result = le.compute(u1=5, u2=5)
        assert result['y'] is True

    def test_less_equal_false(self):
        """Test u1 > u2"""
        le = LessEqual()
        result = le.compute(u1=10, u2=5)
        assert result['y'] is False


class TestLessEqualThreshold:
    """Test the LessEqualThreshold block"""

    def test_less_equal_threshold_true_less(self):
        """Test u < t"""
        let = LessEqualThreshold(t=10)
        result = let.compute(u=5)
        assert result['y'] is True

    def test_less_equal_threshold_true_equal(self):
        """Test u == t"""
        let = LessEqualThreshold(t=10)
        result = let.compute(u=10)
        assert result['y'] is True

    def test_less_equal_threshold_false(self):
        """Test u > t"""
        let = LessEqualThreshold(t=10)
        result = let.compute(u=15)
        assert result['y'] is False


class TestLessThreshold:
    """Test the LessThreshold block"""

    def test_less_threshold_true(self):
        """Test u < t"""
        lt = LessThreshold(t=10)
        result = lt.compute(u=5)
        assert result['y'] is True

    def test_less_threshold_equal(self):
        """Test u == t (should be false)"""
        lt = LessThreshold(t=10)
        result = lt.compute(u=10)
        assert result['y'] is False

    def test_less_threshold_false(self):
        """Test u > t"""
        lt = LessThreshold(t=10)
        result = lt.compute(u=15)
        assert result['y'] is False


class TestMultiSum:
    """Test the MultiSum block"""

    def test_multisum_empty(self):
        """Test MultiSum with no inputs"""
        ms = MultiSum()
        result = ms.compute(u=[])
        assert result['y'] == 0

    def test_multisum_single_default_gain(self):
        """Test MultiSum with single input and default gain"""
        ms = MultiSum(k=[1])
        result = ms.compute(u=[5])
        assert result['y'] == 5

    def test_multisum_multiple_default_gains(self):
        """Test MultiSum with multiple inputs and default gains"""
        ms = MultiSum(k=[1, 1, 1])
        result = ms.compute(u=[2, 3, 4])
        assert result['y'] == 9

    def test_multisum_custom_gains(self):
        """Test MultiSum with custom gains"""
        ms = MultiSum(k=[2, -1, 3])
        result = ms.compute(u=[5, 3, 2])
        assert result['y'] == 2*5 + (-1)*3 + 3*2  # 10 - 3 + 6 = 13

    def test_multisum_negative_values(self):
        """Test MultiSum with negative values"""
        ms = MultiSum(k=[1, 1])
        result = ms.compute(u=[-5, 10])
        assert result['y'] == 5

    def test_multisum_all_zeros(self):
        """Test MultiSum with all zero inputs"""
        ms = MultiSum(k=[1, 1, 1])
        result = ms.compute(u=[0, 0, 0])
        assert result['y'] == 0
