# ABOUTME: Test suite for Routing blocks
# ABOUTME: Tests extractors, replicators, and filters for Real, Integer, Boolean types
import pytest
from cdl_python.CDL.Routing import (
    # Real blocks
    RealExtractor,
    RealExtractSignal,
    RealScalarReplicator,
    RealVectorFilter,
    RealVectorReplicator,
    # Integer blocks
    IntegerExtractor,
    IntegerExtractSignal,
    IntegerScalarReplicator,
    IntegerVectorFilter,
    IntegerVectorReplicator,
    # Boolean blocks
    BooleanExtractor,
    BooleanExtractSignal,
    BooleanScalarReplicator,
    BooleanVectorFilter,
    BooleanVectorReplicator,
)


# =====================================================
# Real Extractor Tests
# =====================================================

class TestRealExtractor:
    """Test RealExtractor block"""

    def test_extract_middle_element(self):
        """Extract element from middle of vector"""
        ext = RealExtractor(nin=5)
        result = ext.compute(u=[1.0, 2.0, 3.0, 4.0, 5.0], index=3)
        assert result['y'] == 3.0

    def test_extract_first_element(self):
        """Extract first element"""
        ext = RealExtractor(nin=3)
        result = ext.compute(u=[10.0, 20.0, 30.0], index=1)
        assert result['y'] == 10.0

    def test_extract_last_element(self):
        """Extract last element"""
        ext = RealExtractor(nin=3)
        result = ext.compute(u=[10.0, 20.0, 30.0], index=3)
        assert result['y'] == 30.0

    def test_clamps_high_index(self):
        """Index clamped to maximum when too high"""
        ext = RealExtractor(nin=3)
        result = ext.compute(u=[1.0, 2.0, 3.0], index=10)
        assert result['y'] == 3.0

    def test_clamps_low_index(self):
        """Index clamped to minimum when too low"""
        ext = RealExtractor(nin=3)
        result = ext.compute(u=[1.0, 2.0, 3.0], index=0)
        assert result['y'] == 1.0


class TestRealExtractSignal:
    """Test RealExtractSignal block"""

    def test_extract_with_parameter(self):
        """Extract using parameter instead of input"""
        ext = RealExtractSignal(nin=4, extract=2)
        result = ext.compute(u=[1.5, 2.5, 3.5, 4.5])
        assert result['y'] == 2.5

    def test_clamps_extract_parameter(self):
        """Extract parameter clamped to valid range"""
        ext = RealExtractSignal(nin=3, extract=10)
        result = ext.compute(u=[1.0, 2.0, 3.0])
        assert result['y'] == 3.0


# =====================================================
# Real Replicator Tests
# =====================================================

class TestRealScalarReplicator:
    """Test RealScalarReplicator block"""

    def test_replicate_scalar(self):
        """Replicate scalar to vector"""
        rep = RealScalarReplicator(nout=4)
        result = rep.compute(u=5.5)
        assert result['y'] == [5.5, 5.5, 5.5, 5.5]

    def test_replicate_once(self):
        """Replication of 1 produces single-element vector"""
        rep = RealScalarReplicator(nout=1)
        result = rep.compute(u=3.14)
        assert result['y'] == [3.14]


class TestRealVectorReplicator:
    """Test RealVectorReplicator block"""

    def test_replicate_vector(self):
        """Replicate vector multiple times"""
        rep = RealVectorReplicator(nin=2, nrep=3)
        result = rep.compute(u=[1.0, 2.0])
        assert result['y'] == [1.0, 2.0, 1.0, 2.0, 1.0, 2.0]

    def test_replicate_once(self):
        """Replication of 1 returns same vector"""
        rep = RealVectorReplicator(nin=3, nrep=1)
        result = rep.compute(u=[1.0, 2.0, 3.0])
        assert result['y'] == [1.0, 2.0, 3.0]


# =====================================================
# Real Filter Tests
# =====================================================

class TestRealVectorFilter:
    """Test RealVectorFilter block"""

    def test_filter_alternating_mask(self):
        """Filter with alternating mask"""
        filt = RealVectorFilter(nin=4, nout=2, msk=[True, False, True, False])
        result = filt.compute(u=[1.0, 2.0, 3.0, 4.0])
        assert result['y'] == [1.0, 3.0]

    def test_filter_all_true(self):
        """Filter with all True mask returns all elements"""
        filt = RealVectorFilter(nin=3, nout=3, msk=[True, True, True])
        result = filt.compute(u=[1.0, 2.0, 3.0])
        assert result['y'] == [1.0, 2.0, 3.0]

    def test_filter_custom_mask(self):
        """Filter with custom mask pattern"""
        filt = RealVectorFilter(nin=5, nout=3, msk=[True, False, True, True, False])
        result = filt.compute(u=[10.0, 20.0, 30.0, 40.0, 50.0])
        assert result['y'] == [10.0, 30.0, 40.0]

    def test_raises_on_mismatch(self):
        """Raises error when nout doesn't match True count"""
        with pytest.raises(ValueError):
            RealVectorFilter(nin=4, nout=3, msk=[True, False, True, False])  # Only 2 Trues


# =====================================================
# Integer Extractor Tests
# =====================================================

class TestIntegerExtractor:
    """Test IntegerExtractor block"""

    def test_extract_integer(self):
        """Extract integer from vector"""
        ext = IntegerExtractor(nin=4)
        result = ext.compute(u=[10, 20, 30, 40], index=2)
        assert result['y'] == 20

    def test_clamps_integer_index(self):
        """Index clamping works for integers"""
        ext = IntegerExtractor(nin=3)
        result = ext.compute(u=[1, 2, 3], index=10)
        assert result['y'] == 3


class TestIntegerExtractSignal:
    """Test IntegerExtractSignal block"""

    def test_extract_integer_with_parameter(self):
        """Extract integer using parameter"""
        ext = IntegerExtractSignal(nin=3, extract=2)
        result = ext.compute(u=[100, 200, 300])
        assert result['y'] == 200


# =====================================================
# Integer Replicator Tests
# =====================================================

class TestIntegerScalarReplicator:
    """Test IntegerScalarReplicator block"""

    def test_replicate_integer_scalar(self):
        """Replicate integer scalar"""
        rep = IntegerScalarReplicator(nout=5)
        result = rep.compute(u=7)
        assert result['y'] == [7, 7, 7, 7, 7]


class TestIntegerVectorReplicator:
    """Test IntegerVectorReplicator block"""

    def test_replicate_integer_vector(self):
        """Replicate integer vector"""
        rep = IntegerVectorReplicator(nin=2, nrep=2)
        result = rep.compute(u=[1, 2])
        assert result['y'] == [1, 2, 1, 2]


# =====================================================
# Integer Filter Tests
# =====================================================

class TestIntegerVectorFilter:
    """Test IntegerVectorFilter block"""

    def test_filter_integers(self):
        """Filter integer vector"""
        filt = IntegerVectorFilter(nin=4, nout=2, msk=[False, True, False, True])
        result = filt.compute(u=[10, 20, 30, 40])
        assert result['y'] == [20, 40]


# =====================================================
# Boolean Extractor Tests
# =====================================================

class TestBooleanExtractor:
    """Test BooleanExtractor block"""

    def test_extract_boolean(self):
        """Extract boolean from vector"""
        ext = BooleanExtractor(nin=4)
        result = ext.compute(u=[True, False, True, False], index=3)
        assert result['y'] is True

    def test_extract_false(self):
        """Extract False value"""
        ext = BooleanExtractor(nin=3)
        result = ext.compute(u=[True, False, True], index=2)
        assert result['y'] is False


class TestBooleanExtractSignal:
    """Test BooleanExtractSignal block"""

    def test_extract_boolean_with_parameter(self):
        """Extract boolean using parameter"""
        ext = BooleanExtractSignal(nin=3, extract=1)
        result = ext.compute(u=[True, False, False])
        assert result['y'] is True


# =====================================================
# Boolean Replicator Tests
# =====================================================

class TestBooleanScalarReplicator:
    """Test BooleanScalarReplicator block"""

    def test_replicate_true(self):
        """Replicate True"""
        rep = BooleanScalarReplicator(nout=3)
        result = rep.compute(u=True)
        assert result['y'] == [True, True, True]

    def test_replicate_false(self):
        """Replicate False"""
        rep = BooleanScalarReplicator(nout=4)
        result = rep.compute(u=False)
        assert result['y'] == [False, False, False, False]


class TestBooleanVectorReplicator:
    """Test BooleanVectorReplicator block"""

    def test_replicate_boolean_vector(self):
        """Replicate boolean vector"""
        rep = BooleanVectorReplicator(nin=2, nrep=3)
        result = rep.compute(u=[True, False])
        assert result['y'] == [True, False, True, False, True, False]


# =====================================================
# Boolean Filter Tests
# =====================================================

class TestBooleanVectorFilter:
    """Test BooleanVectorFilter block"""

    def test_filter_booleans(self):
        """Filter boolean vector"""
        filt = BooleanVectorFilter(nin=4, nout=2, msk=[True, False, False, True])
        result = filt.compute(u=[True, True, False, False])
        assert result['y'] == [True, False]

    def test_filter_all_false(self):
        """Filter with pattern that extracts all False values"""
        filt = BooleanVectorFilter(nin=3, nout=2, msk=[False, True, True])
        result = filt.compute(u=[True, False, False])
        assert result['y'] == [False, False]
