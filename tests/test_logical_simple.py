# ABOUTME: Test suite for simple logical blocks (Xor, Nand, Nor, MultiAnd, MultiOr)
# ABOUTME: Tests basic logical operations without state management
import pytest
from cdl_python.CDL.Logical import Xor, Nand, Nor, MultiAnd, MultiOr


class TestXor:
    """Test the XOR logical operator"""

    def test_xor_false_false(self):
        """Test XOR with both inputs false"""
        xor_block = Xor()
        result = xor_block.compute(u1=False, u2=False)
        assert result['y'] is False

    def test_xor_false_true(self):
        """Test XOR with u1=False, u2=True"""
        xor_block = Xor()
        result = xor_block.compute(u1=False, u2=True)
        assert result['y'] is True

    def test_xor_true_false(self):
        """Test XOR with u1=True, u2=False"""
        xor_block = Xor()
        result = xor_block.compute(u1=True, u2=False)
        assert result['y'] is True

    def test_xor_true_true(self):
        """Test XOR with both inputs true"""
        xor_block = Xor()
        result = xor_block.compute(u1=True, u2=True)
        assert result['y'] is False


class TestNand:
    """Test the NAND logical operator"""

    def test_nand_false_false(self):
        """Test NAND with both inputs false"""
        nand_block = Nand()
        result = nand_block.compute(u1=False, u2=False)
        assert result['y'] is True

    def test_nand_false_true(self):
        """Test NAND with u1=False, u2=True"""
        nand_block = Nand()
        result = nand_block.compute(u1=False, u2=True)
        assert result['y'] is True

    def test_nand_true_false(self):
        """Test NAND with u1=True, u2=False"""
        nand_block = Nand()
        result = nand_block.compute(u1=True, u2=False)
        assert result['y'] is True

    def test_nand_true_true(self):
        """Test NAND with both inputs true"""
        nand_block = Nand()
        result = nand_block.compute(u1=True, u2=True)
        assert result['y'] is False


class TestNor:
    """Test the NOR logical operator"""

    def test_nor_false_false(self):
        """Test NOR with both inputs false"""
        nor_block = Nor()
        result = nor_block.compute(u1=False, u2=False)
        assert result['y'] is True

    def test_nor_false_true(self):
        """Test NOR with u1=False, u2=True"""
        nor_block = Nor()
        result = nor_block.compute(u1=False, u2=True)
        assert result['y'] is False

    def test_nor_true_false(self):
        """Test NOR with u1=True, u2=False"""
        nor_block = Nor()
        result = nor_block.compute(u1=True, u2=False)
        assert result['y'] is False

    def test_nor_true_true(self):
        """Test NOR with both inputs true"""
        nor_block = Nor()
        result = nor_block.compute(u1=True, u2=True)
        assert result['y'] is False


class TestMultiAnd:
    """Test the MultiAnd logical operator"""

    def test_multiand_empty(self):
        """Test MultiAnd with no inputs"""
        multiand_block = MultiAnd()
        result = multiand_block.compute(u=[])
        assert result['y'] is False

    def test_multiand_single_true(self):
        """Test MultiAnd with single true input"""
        multiand_block = MultiAnd()
        result = multiand_block.compute(u=[True])
        assert result['y'] is True

    def test_multiand_single_false(self):
        """Test MultiAnd with single false input"""
        multiand_block = MultiAnd()
        result = multiand_block.compute(u=[False])
        assert result['y'] is False

    def test_multiand_all_true(self):
        """Test MultiAnd with all true inputs"""
        multiand_block = MultiAnd()
        result = multiand_block.compute(u=[True, True, True])
        assert result['y'] is True

    def test_multiand_all_false(self):
        """Test MultiAnd with all false inputs"""
        multiand_block = MultiAnd()
        result = multiand_block.compute(u=[False, False, False])
        assert result['y'] is False

    def test_multiand_mixed_one_false(self):
        """Test MultiAnd with mixed inputs (one false)"""
        multiand_block = MultiAnd()
        result = multiand_block.compute(u=[True, False, True])
        assert result['y'] is False

    def test_multiand_two_inputs_true(self):
        """Test MultiAnd with two true inputs"""
        multiand_block = MultiAnd()
        result = multiand_block.compute(u=[True, True])
        assert result['y'] is True


class TestMultiOr:
    """Test the MultiOr logical operator"""

    def test_multior_empty(self):
        """Test MultiOr with no inputs"""
        multior_block = MultiOr()
        result = multior_block.compute(u=[])
        assert result['y'] is False

    def test_multior_single_true(self):
        """Test MultiOr with single true input"""
        multior_block = MultiOr()
        result = multior_block.compute(u=[True])
        assert result['y'] is True

    def test_multior_single_false(self):
        """Test MultiOr with single false input"""
        multior_block = MultiOr()
        result = multior_block.compute(u=[False])
        assert result['y'] is False

    def test_multior_all_true(self):
        """Test MultiOr with all true inputs"""
        multior_block = MultiOr()
        result = multior_block.compute(u=[True, True, True])
        assert result['y'] is True

    def test_multior_all_false(self):
        """Test MultiOr with all false inputs"""
        multior_block = MultiOr()
        result = multior_block.compute(u=[False, False, False])
        assert result['y'] is False

    def test_multior_mixed_one_true(self):
        """Test MultiOr with mixed inputs (one true)"""
        multior_block = MultiOr()
        result = multior_block.compute(u=[False, True, False])
        assert result['y'] is True

    def test_multior_two_inputs_false(self):
        """Test MultiOr with two false inputs"""
        multior_block = MultiOr()
        result = multior_block.compute(u=[False, False])
        assert result['y'] is False
