# ABOUTME: Test suite for logical timer blocks (Timer, TimerAccumulating, TrueDelay)
# ABOUTME: Tests time-based logical operations
import pytest
from cdl_python.time_manager import TimeManager, ExecutionMode
from cdl_python.CDL.Logical import Timer, TimerAccumulating, TrueDelay


class TestTimer:
    """Test the Timer block"""

    def test_timer_false_input(self):
        """Test Timer with false input"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        timer = Timer(time_manager=tm, t=2.0)
        result = timer.compute(u=False)
        assert result['y'] == 0.0
        assert result['passed'] is False

    def test_timer_starts_on_true(self):
        """Test Timer starts counting when input goes true"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        timer = Timer(time_manager=tm, t=2.0)
        result = timer.compute(u=False)
        assert result['y'] == 0.0

        result = timer.compute(u=True)
        assert result['y'] == 0.0
        assert result['passed'] is False

    def test_timer_counts_up(self):
        """Test Timer counts elapsed time"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        timer = Timer(time_manager=tm, t=2.0)

        result = timer.compute(u=True)
        tm.advance(dt=0.1)
        result = timer.compute(u=True)
        assert result['y'] == pytest.approx(0.1, abs=1e-6)

        tm.advance(dt=0.1)
        result = timer.compute(u=True)
        assert result['y'] == pytest.approx(0.2, abs=1e-6)

    def test_timer_passes_threshold(self):
        """Test Timer sets passed when time exceeds threshold"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.5)
        timer = Timer(time_manager=tm, t=1.0)

        result = timer.compute(u=True)
        assert result['passed'] is False

        tm.advance(dt=0.5)
        result = timer.compute(u=True)
        assert result['y'] == pytest.approx(0.5)
        assert result['passed'] is False

        tm.advance(dt=0.5)
        result = timer.compute(u=True)
        assert result['y'] == pytest.approx(1.0)
        assert result['passed'] is True

    def test_timer_resets_on_false(self):
        """Test Timer resets when input goes false"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        timer = Timer(time_manager=tm, t=2.0)

        result = timer.compute(u=True)
        tm.advance(dt=0.5)
        result = timer.compute(u=True)
        assert result['y'] == pytest.approx(0.5)

        result = timer.compute(u=False)
        assert result['y'] == 0.0
        assert result['passed'] is False


class TestTimerAccumulating:
    """Test the TimerAccumulating block"""

    def test_timer_accumulating_initialization(self):
        """Test TimerAccumulating initializes correctly"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        timer = TimerAccumulating(time_manager=tm, t=2.0)
        result = timer.compute(u=False, reset=False)
        assert result['y'] == 0.0
        assert result['passed'] is False

    def test_timer_accumulating_counts(self):
        """Test TimerAccumulating accumulates time"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        timer = TimerAccumulating(time_manager=tm, t=2.0)

        result = timer.compute(u=True, reset=False)
        tm.advance(dt=0.5)
        result = timer.compute(u=True, reset=False)
        assert result['y'] == pytest.approx(0.5)

    def test_timer_accumulating_holds_on_false(self):
        """Test TimerAccumulating holds value when u goes false"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        timer = TimerAccumulating(time_manager=tm, t=2.0)

        result = timer.compute(u=True, reset=False)
        tm.advance(dt=0.5)
        result = timer.compute(u=True, reset=False)
        assert result['y'] == pytest.approx(0.5)

        result = timer.compute(u=False, reset=False)
        assert result['y'] == pytest.approx(0.5)  # Holds value

        tm.advance(dt=0.2)
        result = timer.compute(u=False, reset=False)
        assert result['y'] == pytest.approx(0.5)  # Still holding

    def test_timer_accumulating_resumes(self):
        """Test TimerAccumulating resumes counting"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        timer = TimerAccumulating(time_manager=tm, t=2.0)

        result = timer.compute(u=True, reset=False)
        tm.advance(dt=0.5)
        result = timer.compute(u=True, reset=False)
        assert result['y'] == pytest.approx(0.5)

        result = timer.compute(u=False, reset=False)
        tm.advance(dt=0.2)

        result = timer.compute(u=True, reset=False)
        tm.advance(dt=0.3)
        result = timer.compute(u=True, reset=False)
        assert result['y'] == pytest.approx(0.8)  # 0.5 + 0.3

    def test_timer_accumulating_reset(self):
        """Test TimerAccumulating resets to zero"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        timer = TimerAccumulating(time_manager=tm, t=2.0)

        result = timer.compute(u=True, reset=False)
        tm.advance(dt=0.5)
        result = timer.compute(u=True, reset=False)
        assert result['y'] == pytest.approx(0.5)

        result = timer.compute(u=False, reset=True)
        assert result['y'] == 0.0
        assert result['passed'] is False


class TestTrueDelay:
    """Test the TrueDelay block"""

    def test_true_delay_false_input(self):
        """Test TrueDelay with false input"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        delay = TrueDelay(time_manager=tm, delayTime=1.0)
        result = delay.compute(u=False)
        assert result['y'] is False

    def test_true_delay_immediate_false(self):
        """Test TrueDelay passes false immediately"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        delay = TrueDelay(time_manager=tm, delayTime=1.0)

        result = delay.compute(u=True)
        tm.advance(dt=0.5)
        result = delay.compute(u=True)

        result = delay.compute(u=False)
        assert result['y'] is False  # Immediate

    def test_true_delay_delays_true(self):
        """Test TrueDelay delays rising edge"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        delay = TrueDelay(time_manager=tm, delayTime=0.5)

        result = delay.compute(u=True)
        assert result['y'] is False  # Not yet

        tm.advance(dt=0.3)
        result = delay.compute(u=True)
        assert result['y'] is False  # Still not yet

        tm.advance(dt=0.3)
        result = delay.compute(u=True)
        assert result['y'] is True  # Now delayed true appears

    def test_true_delay_zero_delay(self):
        """Test TrueDelay with zero delay"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        delay = TrueDelay(time_manager=tm, delayTime=0.0)

        result = delay.compute(u=True)
        assert result['y'] is True  # Immediate with zero delay
