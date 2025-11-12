# ABOUTME: Test suite for additional real blocks (Hysteresis, Sort, Line, MatrixGain, etc.)
# ABOUTME: Tests real-valued operations including sorting, interpolation, and matrix operations
import pytest
import numpy as np
from cdl_python.CDL.Reals import Hysteresis, Sort, Line, MatrixGain, MatrixMax, MatrixMin


class TestHysteresis:
    """Test the Hysteresis block"""

    def test_hysteresis_initialization_false(self):
        """Test Hysteresis initializes to false"""
        hys = Hysteresis(uLow=2.0, uHigh=4.0, pre_y_start=False)
        result = hys.compute(u=3.0)
        assert result['y'] is False

    def test_hysteresis_switch_to_true(self):
        """Test Hysteresis switches to true when u > uHigh"""
        hys = Hysteresis(uLow=2.0, uHigh=4.0, pre_y_start=False)
        result = hys.compute(u=3.0)
        assert result['y'] is False
        result = hys.compute(u=4.5)
        assert result['y'] is True

    def test_hysteresis_stays_true(self):
        """Test Hysteresis stays true above uLow"""
        hys = Hysteresis(uLow=2.0, uHigh=4.0, pre_y_start=True)
        result = hys.compute(u=3.0)
        assert result['y'] is True

    def test_hysteresis_switch_to_false(self):
        """Test Hysteresis switches to false when u < uLow"""
        hys = Hysteresis(uLow=2.0, uHigh=4.0, pre_y_start=True)
        result = hys.compute(u=3.0)
        assert result['y'] is True
        result = hys.compute(u=1.5)
        assert result['y'] is False


class TestSort:
    """Test the Sort block"""

    def test_sort_ascending(self):
        """Test Sort in ascending order"""
        sort_block = Sort(ascending=True)
        result = sort_block.compute(u=[3.0, 1.0, 4.0, 1.5, 9.0, 2.0])
        expected = [1.0, 1.5, 2.0, 3.0, 4.0, 9.0]
        assert np.allclose(result['y'], expected)
        assert result['yIdx'] == [2, 4, 6, 1, 3, 5]  # 1-based indices

    def test_sort_descending(self):
        """Test Sort in descending order"""
        sort_block = Sort(ascending=False)
        result = sort_block.compute(u=[3.0, 1.0, 4.0, 1.5])
        expected = [4.0, 3.0, 1.5, 1.0]
        assert np.allclose(result['y'], expected)

    def test_sort_empty(self):
        """Test Sort with empty input"""
        sort_block = Sort()
        result = sort_block.compute(u=[])
        assert len(result['y']) == 0


class TestLine:
    """Test the Line interpolation block"""

    def test_line_basic_interpolation(self):
        """Test Line basic linear interpolation"""
        line = Line(limitBelow=False, limitAbove=False)
        # Line through (0, 0) and (10, 20): y = 2x
        result = line.compute(x1=0.0, f1=0.0, x2=10.0, f2=20.0, u=5.0)
        assert result['y'] == pytest.approx(10.0)

    def test_line_limit_below(self):
        """Test Line with lower limit"""
        line = Line(limitBelow=True, limitAbove=False)
        result = line.compute(x1=2.0, f1=4.0, x2=8.0, f2=16.0, u=0.0)
        # Should limit u to x1=2.0, so y = 4.0
        assert result['y'] == pytest.approx(4.0)

    def test_line_limit_above(self):
        """Test Line with upper limit"""
        line = Line(limitBelow=False, limitAbove=True)
        result = line.compute(x1=2.0, f1=4.0, x2=8.0, f2=16.0, u=10.0)
        # Should limit u to x2=8.0, so y = 16.0
        assert result['y'] == pytest.approx(16.0)

    def test_line_both_limits(self):
        """Test Line with both limits"""
        line = Line(limitBelow=True, limitAbove=True)
        result = line.compute(x1=2.0, f1=4.0, x2=8.0, f2=16.0, u=5.0)
        # u is within limits, so interpolate: slope = 2, y = 2*5 + 0 = 10
        assert result['y'] == pytest.approx(10.0)


class TestMatrixGain:
    """Test the MatrixGain block"""

    def test_matrix_gain_identity(self):
        """Test MatrixGain with identity matrix"""
        K = [[1.0, 0.0], [0.0, 1.0]]
        mg = MatrixGain(K=K)
        result = mg.compute(u=[3.0, 5.0])
        assert np.allclose(result['y'], [3.0, 5.0])

    def test_matrix_gain_custom(self):
        """Test MatrixGain with custom matrix"""
        K = [[0.12, 2.0], [3.0, 1.5]]
        mg = MatrixGain(K=K)
        result = mg.compute(u=[1.0, 2.0])
        # y = K * u = [[0.12, 2.0], [3.0, 1.5]] * [1.0, 2.0]
        # y[0] = 0.12*1 + 2.0*2 = 4.12
        # y[1] = 3.0*1 + 1.5*2 = 6.0
        assert result['y'][0] == pytest.approx(4.12)
        assert result['y'][1] == pytest.approx(6.0)

    def test_matrix_gain_non_square(self):
        """Test MatrixGain with non-square matrix"""
        K = [[1.0, 2.0, 3.0]]  # 1x3 matrix
        mg = MatrixGain(K=K)
        result = mg.compute(u=[1.0, 2.0, 3.0])
        # y = 1*1 + 2*2 + 3*3 = 14
        assert result['y'][0] == pytest.approx(14.0)


class TestMatrixMax:
    """Test the MatrixMax block"""

    def test_matrix_max_basic(self):
        """Test MatrixMax with positive values"""
        mm = MatrixMax()
        result = mm.compute(u=[1.0, 5.0, 3.0, 9.0, 2.0])
        assert result['y'] == 9.0

    def test_matrix_max_negative(self):
        """Test MatrixMax with negative values"""
        mm = MatrixMax()
        result = mm.compute(u=[-5.0, -1.0, -10.0, -3.0])
        assert result['y'] == -1.0

    def test_matrix_max_single(self):
        """Test MatrixMax with single element"""
        mm = MatrixMax()
        result = mm.compute(u=[42.0])
        assert result['y'] == 42.0


class TestMatrixMin:
    """Test the MatrixMin block"""

    def test_matrix_min_basic(self):
        """Test MatrixMin with positive values"""
        mm = MatrixMin()
        result = mm.compute(u=[5.0, 1.0, 9.0, 3.0, 2.0])
        assert result['y'] == 1.0

    def test_matrix_min_negative(self):
        """Test MatrixMin with negative values"""
        mm = MatrixMin()
        result = mm.compute(u=[-5.0, -1.0, -10.0, -3.0])
        assert result['y'] == -10.0

    def test_matrix_min_single(self):
        """Test MatrixMin with single element"""
        mm = MatrixMin()
        result = mm.compute(u=[42.0])
        assert result['y'] == 42.0
