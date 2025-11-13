# ABOUTME: Test suite for Reals.Sources blocks
# ABOUTME: Tests constant and sine wave signal generators
import pytest
import math
from cdl_python.time_manager import TimeManager, ExecutionMode
from cdl_python.CDL.Reals.Sources import Constant, Sin


class TestConstant:
    """Test the Constant source block"""

    def test_constant_output(self):
        """Test that constant outputs the specified value"""
        const = Constant(k=5.0)
        result = const.compute()
        assert result['y'] == 5.0

    def test_constant_with_different_values(self):
        """Test constant with various values"""
        for k in [0.0, 1.5, -3.2, 100.0]:
            const = Constant(k=k)
            result = const.compute()
            assert result['y'] == k

    def test_constant_multiple_calls(self):
        """Test that constant returns same value on multiple calls"""
        const = Constant(k=3.14)
        for _ in range(10):
            result = const.compute()
            assert result['y'] == pytest.approx(3.14)


class TestSin:
    """Test the Sin source block"""

    def test_sin_at_time_zero(self):
        """Test sin output at t=0"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        sin = Sin(time_manager=tm, amplitude=1.0, freqHz=1.0, phase=0.0, offset=0.0)
        result = sin.compute()
        assert result['y'] == pytest.approx(0.0, abs=1e-6)

    def test_sin_quarter_period(self):
        """Test sin at quarter period (90 degrees)"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.25)
        sin = Sin(time_manager=tm, amplitude=1.0, freqHz=1.0, phase=0.0, offset=0.0)

        # At t=0: sin(0) = 0
        result = sin.compute()
        assert result['y'] == pytest.approx(0.0, abs=1e-6)

        # At t=0.25: sin(2*pi*1*0.25) = sin(pi/2) = 1
        tm.advance(dt=0.25)
        result = sin.compute()
        assert result['y'] == pytest.approx(1.0, abs=1e-6)

    def test_sin_half_period(self):
        """Test sin at half period (180 degrees)"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.5)
        sin = Sin(time_manager=tm, amplitude=1.0, freqHz=1.0, phase=0.0, offset=0.0)

        # At t=0.5: sin(2*pi*1*0.5) = sin(pi) = 0
        tm.advance(dt=0.5)
        result = sin.compute()
        assert result['y'] == pytest.approx(0.0, abs=1e-6)

    def test_sin_with_amplitude(self):
        """Test sin with different amplitude"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.25)
        sin = Sin(time_manager=tm, amplitude=5.0, freqHz=1.0, phase=0.0, offset=0.0)

        # At t=0.25: 5*sin(pi/2) = 5
        tm.advance(dt=0.25)
        result = sin.compute()
        assert result['y'] == pytest.approx(5.0, abs=1e-6)

    def test_sin_with_offset(self):
        """Test sin with offset"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.0)
        sin = Sin(time_manager=tm, amplitude=1.0, freqHz=1.0, phase=0.0, offset=3.0)

        # At t=0: 3 + sin(0) = 3
        result = sin.compute()
        assert result['y'] == pytest.approx(3.0, abs=1e-6)

    def test_sin_with_phase(self):
        """Test sin with phase shift"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.0)
        # Phase = pi/2 radians (90 degrees)
        sin = Sin(time_manager=tm, amplitude=1.0, freqHz=1.0, phase=math.pi/2, offset=0.0)

        # At t=0: sin(0 + pi/2) = sin(pi/2) = 1
        result = sin.compute()
        assert result['y'] == pytest.approx(1.0, abs=1e-6)

    def test_sin_before_start_time(self):
        """Test sin outputs offset before start time"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        sin = Sin(time_manager=tm, amplitude=1.0, freqHz=1.0, phase=0.0, offset=2.0, startTime=1.0)

        # At t=0 (before startTime): output = offset
        result = sin.compute()
        assert result['y'] == pytest.approx(2.0, abs=1e-6)

        # At t=0.5 (still before startTime): output = offset
        tm.advance(dt=0.5)
        result = sin.compute()
        assert result['y'] == pytest.approx(2.0, abs=1e-6)

        # At t=1.25 (after startTime): output = offset + amplitude*sin(2*pi*freq*(1.25-1.0))
        tm.advance(dt=0.75)  # Now at t=1.25
        result = sin.compute()
        expected = 2.0 + 1.0 * math.sin(2.0 * math.pi * 1.0 * 0.25)  # = 2.0 + sin(pi/2) = 3.0
        assert result['y'] == pytest.approx(expected, abs=1e-6)

    def test_sin_full_cycle(self):
        """Test sin over a full cycle"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.25)
        sin = Sin(time_manager=tm, amplitude=2.0, freqHz=1.0, phase=0.0, offset=0.0)

        # Sample at key points in the cycle
        test_points = [
            (0.0, 0.0),           # t=0: sin(0) = 0
            (0.25, 2.0),          # t=0.25: 2*sin(pi/2) = 2
            (0.5, 0.0),           # t=0.5: 2*sin(pi) = 0
            (0.75, -2.0),         # t=0.75: 2*sin(3*pi/2) = -2
            (1.0, 0.0),           # t=1.0: 2*sin(2*pi) = 0
        ]

        for i, (target_time, expected) in enumerate(test_points):
            result = sin.compute()
            assert result['y'] == pytest.approx(expected, abs=1e-5), f"Failed at step {i}, time {tm.get_time()}"

            # Advance to next time point
            if i < len(test_points) - 1:
                tm.advance(dt=0.25)
