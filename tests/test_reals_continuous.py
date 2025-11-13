# ABOUTME: Tests for continuous-time Reals blocks
import pytest
from cdl_python.time_manager import TimeManager, ExecutionMode
from cdl_python.CDL.Reals import Derivative, LimitSlewRate, MovingAverage


class TestDerivative:
    """Test Derivative block"""

    def test_constant_input_zero_derivative(self):
        """Derivative of constant should be zero"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        deriv = Derivative(time_manager=tm, y_max=100.0)

        # First call
        deriv.compute(u=5.0)

        # Subsequent calls with same value
        tm.advance(dt=0.1)
        result = deriv.compute(u=5.0)
        assert abs(result['y']) < 0.01  # Should be near zero

    def test_ramp_input_constant_derivative(self):
        """Derivative of ramp should be constant"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        deriv = Derivative(time_manager=tm)

        # Create ramp: u = t
        deriv.compute(u=0.0)

        derivatives = []
        for i in range(1, 5):
            tm.advance(dt=0.1)
            result = deriv.compute(u=i * 0.1)
            derivatives.append(result['y'])

        # All derivatives should be close to 1.0
        for dy in derivatives:
            assert abs(dy - 1.0) < 0.1

    def test_limits_output(self):
        """Derivative should be limited by y_max"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        deriv = Derivative(time_manager=tm, y_max=5.0)

        deriv.compute(u=0.0)

        # Large jump
        tm.advance(dt=0.1)
        result = deriv.compute(u=100.0)  # derivative = 1000

        # Should be limited
        assert abs(result['y']) <= 5.0


class TestLimitSlewRate:
    """Test LimitSlewRate block"""

    def test_tracks_slowly_changing_input(self):
        """Should track input when rate is within limits"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        limiter = LimitSlewRate(
            time_manager=tm,
            raisingSlewRate=10.0,  # 10 units/sec
            fallingSlewRate=10.0,
            y_start=0.0
        )

        # Change by 0.5 in 0.1s = rate of 5 units/s (within limit)
        result = limiter.compute(u=0.5)
        tm.advance(dt=0.1)
        result = limiter.compute(u=1.0)

        # Should track input
        assert abs(result['y'] - 1.0) < 0.2

    def test_limits_rising_rate(self):
        """Should limit rising rate"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        limiter = LimitSlewRate(
            time_manager=tm,
            raisingSlewRate=1.0,  # 1 unit/sec max
            fallingSlewRate=10.0,
            y_start=0.0
        )

        # Request large jump
        result = limiter.compute(u=100.0)

        # Over 1 second, should only rise by 1.0
        for _ in range(10):
            tm.advance(dt=0.1)
            result = limiter.compute(u=100.0)

        # After 1 second, should be at ~1.0
        assert 0.9 < result['y'] < 1.1

    def test_limits_falling_rate(self):
        """Should limit falling rate"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        limiter = LimitSlewRate(
            time_manager=tm,
            raisingSlewRate=10.0,
            fallingSlewRate=2.0,  # 2 units/sec max falling
            y_start=10.0
        )

        # Request large drop
        result = limiter.compute(u=0.0)

        # Over 1 second, should only fall by 2.0
        for _ in range(10):
            tm.advance(dt=0.1)
            result = limiter.compute(u=0.0)

        # After 1 second, should be at ~8.0
        assert 7.9 < result['y'] < 8.1


class TestMovingAverage:
    """Test MovingAverage block"""

    def test_average_of_constant(self):
        """Average of constant should be that constant"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        avg = MovingAverage(time_manager=tm, delta=1.0)

        # Feed constant value
        for _ in range(10):
            result = avg.compute(u=5.0)
            tm.advance(dt=0.1)

        assert abs(result['y'] - 5.0) < 0.1

    def test_filters_noise(self):
        """Moving average should smooth out fluctuations"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        avg = MovingAverage(time_manager=tm, delta=1.0)

        # Alternating values
        values = [1.0, 9.0, 1.0, 9.0, 1.0, 9.0, 1.0, 9.0]
        for u in values:
            result = avg.compute(u=u)
            tm.advance(dt=0.1)

        # Average should be around 5.0
        assert 3.0 < result['y'] < 7.0

    def test_tracks_changing_mean(self):
        """Should track gradual changes in mean"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        avg = MovingAverage(time_manager=tm, delta=0.5)

        # Ramp up
        for i in range(10):
            result = avg.compute(u=float(i))
            tm.advance(dt=0.1)

        # Average should be increasing
        assert result['y'] > 5.0

    def test_invalid_delta(self):
        """Should raise error for non-positive delta"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        with pytest.raises(ValueError):
            MovingAverage(time_manager=tm, delta=0.0)
