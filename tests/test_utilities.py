# ABOUTME: Test suite for Utilities blocks
# ABOUTME: Tests Assert block for validation and debugging
import pytest
import warnings
from cdl_python.CDL.Utilities import Assert


class TestAssert:
    """Test the Assert utility block"""

    def test_assert_true_no_warning(self):
        """No warning when input is True"""
        assert_block = Assert(message="This should not appear")

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = assert_block.compute(u=True)

            # Verify no warning was issued
            assert len(w) == 0
            # Verify empty output
            assert result == {}

    def test_assert_false_issues_warning(self):
        """Warning issued when input is False"""
        assert_block = Assert(message="Test assertion failed")

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = assert_block.compute(u=False)

            # Verify warning was issued
            assert len(w) == 1
            assert issubclass(w[0].category, UserWarning)
            assert "Test assertion failed" in str(w[0].message)
            # Verify empty output
            assert result == {}

    def test_assert_custom_message(self):
        """Custom message appears in warning"""
        custom_msg = "Temperature sensor out of range"
        assert_block = Assert(message=custom_msg)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            assert_block.compute(u=False)

            assert len(w) == 1
            assert custom_msg in str(w[0].message)

    def test_assert_default_message(self):
        """Default message used when none specified"""
        assert_block = Assert()

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            assert_block.compute(u=False)

            assert len(w) == 1
            assert "Assertion failed" in str(w[0].message)

    def test_assert_multiple_calls(self):
        """Multiple False inputs generate multiple warnings"""
        assert_block = Assert(message="Error")

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # First False
            assert_block.compute(u=False)
            assert len(w) == 1

            # Second False
            assert_block.compute(u=False)
            assert len(w) == 2

            # True doesn't add warning
            assert_block.compute(u=True)
            assert len(w) == 2

    def test_assert_returns_empty_dict(self):
        """Assert block always returns empty dictionary"""
        assert_block = Assert()

        result_true = assert_block.compute(u=True)
        result_false = assert_block.compute(u=False)

        assert result_true == {}
        assert result_false == {}
