# ABOUTME: Test suite for Discrete blocks
# ABOUTME: Tests sampling, delay, and triggered operations
import pytest
from cdl_python.time_manager import TimeManager, ExecutionMode
from cdl_python.CDL.Discrete import (
    Sampler,
    UnitDelay,
    ZeroOrderHold,
    FirstOrderHold,
    TriggeredSampler,
    TriggeredMax,
    TriggeredMovingMean,
)


# =====================================================
# UnitDelay Tests
# =====================================================

class TestUnitDelay:
    """Test UnitDelay block (z^-1 operator)"""

    def test_first_output_is_initial_value(self):
        """First output should be y_start"""
        delay = UnitDelay(y_start=5.0)
        result = delay.compute(u=10.0)
        assert result['y'] == 5.0

    def test_second_output_is_first_input(self):
        """Second output should be the first input"""
        delay = UnitDelay(y_start=0.0)
        delay.compute(u=10.0)  # First call
        result = delay.compute(u=20.0)  # Second call
        assert result['y'] == 10.0

    def test_delay_sequence(self):
        """Test delay over a sequence"""
        delay = UnitDelay(y_start=0.0)
        inputs = [1.0, 2.0, 3.0, 4.0, 5.0]
        expected = [0.0, 1.0, 2.0, 3.0, 4.0]

        outputs = []
        for u in inputs:
            result = delay.compute(u=u)
            outputs.append(result['y'])

        assert outputs == expected

    def test_negative_initial_value(self):
        """Test with negative initial value"""
        delay = UnitDelay(y_start=-5.0)
        result = delay.compute(u=10.0)
        assert result['y'] == -5.0


# =====================================================
# ZeroOrderHold Tests
# =====================================================

class TestZeroOrderHold:
    """Test ZeroOrderHold block"""

    def test_samples_at_correct_times(self):
        """Verify sampling occurs at correct times"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        zoh = ZeroOrderHold(time_manager=tm, samplePeriod=1.0, startTime=0.0)

        # t=0: should sample
        result = zoh.compute(u=10.0)
        assert result['y'] == 10.0

        # t=0.5: should hold
        tm.advance(dt=0.5)
        result = zoh.compute(u=20.0)
        assert result['y'] == 10.0  # Still holding

        # t=1.0: should sample again
        tm.advance(dt=0.5)
        result = zoh.compute(u=30.0)
        assert result['y'] == 30.0

    def test_holds_between_samples(self):
        """Value should be held constant between samples"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        zoh = ZeroOrderHold(time_manager=tm, samplePeriod=0.5, startTime=0.0)

        # Sample at t=0
        zoh.compute(u=5.0)

        # Hold from t=0.1 to t=0.4
        for _ in range(4):
            tm.advance(dt=0.1)
            result = zoh.compute(u=999.0)  # Input changes but output holds
            assert result['y'] == 5.0

    def test_delayed_start_time(self):
        """Test with startTime > 0"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        zoh = ZeroOrderHold(time_manager=tm, samplePeriod=1.0, startTime=2.0)

        # Before startTime, should pass through
        result = zoh.compute(u=10.0)
        assert result['y'] == 10.0

        # At startTime, should sample
        tm.advance(dt=2.0)
        result = zoh.compute(u=20.0)
        assert result['y'] == 20.0

    def test_invalid_sample_period(self):
        """Should raise error for non-positive samplePeriod"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        with pytest.raises(ValueError):
            ZeroOrderHold(time_manager=tm, samplePeriod=0.0, startTime=0.0)


# =====================================================
# Sampler Tests
# =====================================================

class TestSampler:
    """Test Sampler block"""

    def test_samples_at_fixed_intervals(self):
        """Verify sampling at regular intervals"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.5)
        sampler = Sampler(time_manager=tm, samplePeriod=1.0, startTime=0.0)

        # t=0: sample
        result = sampler.compute(u=1.0)
        assert result['y'] == 1.0

        # t=0.5: hold
        tm.advance(dt=0.5)
        result = sampler.compute(u=2.0)
        assert result['y'] == 1.0

        # t=1.0: sample
        tm.advance(dt=0.5)
        result = sampler.compute(u=3.0)
        assert result['y'] == 3.0

    def test_behaves_like_zero_order_hold(self):
        """Sampler should behave identically to ZeroOrderHold"""
        tm1 = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        tm2 = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)

        sampler = Sampler(time_manager=tm1, samplePeriod=0.5, startTime=0.0)
        zoh = ZeroOrderHold(time_manager=tm2, samplePeriod=0.5, startTime=0.0)

        inputs = [1.0, 2.0, 3.0, 4.0, 5.0]
        outputs_sampler = []
        outputs_zoh = []

        for u in inputs:
            outputs_sampler.append(sampler.compute(u=u)['y'])
            outputs_zoh.append(zoh.compute(u=u)['y'])
            tm1.advance(dt=0.1)
            tm2.advance(dt=0.1)

        assert outputs_sampler == outputs_zoh


# =====================================================
# FirstOrderHold Tests
# =====================================================

class TestFirstOrderHold:
    """Test FirstOrderHold block"""

    def test_holds_before_second_sample(self):
        """Before second sample, should hold constant"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        foh = FirstOrderHold(time_manager=tm, samplePeriod=1.0, startTime=0.0)

        # First sample at t=0
        result = foh.compute(u=10.0)
        assert result['y'] == 10.0

        # Between t=0 and t=1, should hold
        tm.advance(dt=0.5)
        result = foh.compute(u=20.0)
        assert result['y'] == 10.0

    def test_linear_interpolation(self):
        """After two samples, should interpolate linearly"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        foh = FirstOrderHold(time_manager=tm, samplePeriod=1.0, startTime=0.0)

        # First sample: u=0 at t=0
        foh.compute(u=0.0)

        # Second sample: u=10 at t=1
        tm.advance(dt=1.0)
        foh.compute(u=10.0)

        # At t=1.5, should extrapolate: 10 + slope*0.5 = 10 + 10*0.5 = 15
        tm.advance(dt=0.5)
        result = foh.compute(u=999.0)
        assert result['y'] == pytest.approx(15.0)

    def test_negative_slope(self):
        """Test with decreasing values"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=1.0)
        foh = FirstOrderHold(time_manager=tm, samplePeriod=1.0, startTime=0.0)

        # u=10 at t=0
        foh.compute(u=10.0)

        # u=0 at t=1 (slope = -10)
        tm.advance(dt=1.0)
        foh.compute(u=0.0)

        # At t=1.5: 0 + (-10)*0.5 = -5
        tm.advance(dt=0.5)
        result = foh.compute(u=999.0)
        assert result['y'] == pytest.approx(-5.0)


# =====================================================
# TriggeredSampler Tests
# =====================================================

class TestTriggeredSampler:
    """Test TriggeredSampler block"""

    def test_samples_on_rising_edge(self):
        """Should sample when trigger goes from False to True"""
        sampler = TriggeredSampler(y_start=0.0)

        # Initial: trigger=False
        result = sampler.compute(u=10.0, trigger=False)
        assert result['y'] == 0.0  # Initial value

        # Rising edge: trigger goes True
        result = sampler.compute(u=20.0, trigger=True)
        assert result['y'] == 20.0  # Sampled

        # Trigger stays True (no edge)
        result = sampler.compute(u=30.0, trigger=True)
        assert result['y'] == 20.0  # Still holding

    def test_holds_until_next_trigger(self):
        """Should hold value until next rising edge"""
        sampler = TriggeredSampler(y_start=0.0)

        # First trigger
        sampler.compute(u=10.0, trigger=True)

        # Trigger goes low
        result = sampler.compute(u=20.0, trigger=False)
        assert result['y'] == 10.0

        # Second rising edge
        result = sampler.compute(u=30.0, trigger=True)
        assert result['y'] == 30.0

    def test_initial_value(self):
        """Should output y_start before first trigger"""
        sampler = TriggeredSampler(y_start=99.0)
        result = sampler.compute(u=10.0, trigger=False)
        assert result['y'] == 99.0


# =====================================================
# TriggeredMax Tests
# =====================================================

class TestTriggeredMax:
    """Test TriggeredMax block"""

    def test_tracks_maximum(self):
        """Should track maximum value"""
        tmax = TriggeredMax()

        result = tmax.compute(u=10.0, trigger=False)
        assert result['y'] == 10.0

        result = tmax.compute(u=20.0, trigger=False)
        assert result['y'] == 20.0

        result = tmax.compute(u=15.0, trigger=False)
        assert result['y'] == 20.0  # Still max

    def test_resets_on_trigger(self):
        """Should reset maximum on rising edge"""
        tmax = TriggeredMax()

        # Track max
        tmax.compute(u=10.0, trigger=False)
        tmax.compute(u=20.0, trigger=False)
        assert tmax.compute(u=15.0, trigger=False)['y'] == 20.0

        # Reset with trigger
        result = tmax.compute(u=5.0, trigger=True)
        assert result['y'] == 5.0

        # New maximum
        result = tmax.compute(u=8.0, trigger=False)
        assert result['y'] == 8.0

    def test_handles_negative_values(self):
        """Should handle negative values correctly"""
        tmax = TriggeredMax()

        result = tmax.compute(u=-10.0, trigger=False)
        assert result['y'] == -10.0

        result = tmax.compute(u=-5.0, trigger=False)
        assert result['y'] == -5.0

        result = tmax.compute(u=-20.0, trigger=False)
        assert result['y'] == -5.0


# =====================================================
# TriggeredMovingMean Tests
# =====================================================

class TestTriggeredMovingMean:
    """Test TriggeredMovingMean block"""

    def test_computes_running_average(self):
        """Should compute running average"""
        tmean = TriggeredMovingMean()

        result = tmean.compute(u=10.0, trigger=False)
        assert result['y'] == pytest.approx(10.0)

        result = tmean.compute(u=20.0, trigger=False)
        assert result['y'] == pytest.approx(15.0)  # (10+20)/2

        result = tmean.compute(u=30.0, trigger=False)
        assert result['y'] == pytest.approx(20.0)  # (10+20+30)/3

    def test_resets_on_trigger(self):
        """Should reset accumulation on rising edge"""
        tmean = TriggeredMovingMean()

        # Accumulate values
        tmean.compute(u=10.0, trigger=False)
        tmean.compute(u=20.0, trigger=False)
        assert tmean.compute(u=30.0, trigger=False)['y'] == pytest.approx(20.0)

        # Reset with trigger
        result = tmean.compute(u=50.0, trigger=True)
        assert result['y'] == pytest.approx(50.0)

        # New average
        result = tmean.compute(u=60.0, trigger=False)
        assert result['y'] == pytest.approx(55.0)  # (50+60)/2

    def test_single_value_average(self):
        """Average of single value should be that value"""
        tmean = TriggeredMovingMean()
        result = tmean.compute(u=42.0, trigger=False)
        assert result['y'] == pytest.approx(42.0)

    def test_zero_values(self):
        """Should handle zero values correctly"""
        tmean = TriggeredMovingMean()

        tmean.compute(u=0.0, trigger=False)
        result = tmean.compute(u=0.0, trigger=False)
        assert result['y'] == pytest.approx(0.0)
