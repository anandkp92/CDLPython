# ABOUTME: Test suite for Sources blocks (Reals, Integers, Logical)
# ABOUTME: Tests constant, time-varying, and table-based signal generators
import pytest
import math
from datetime import datetime
from cdl_python.time_manager import TimeManager, ExecutionMode
from cdl_python.CDL.Reals.Sources import (
    Constant, Sin, Pulse as RealPulse, Ramp, TimeTable as RealTimeTable,
    Smoothness, Extrapolation, CalendarTime, ZeroTime, CivilTime
)
from cdl_python.CDL.Integers.Sources import (
    Constant as IntConstant, Pulse as IntPulse, TimeTable as IntTimeTable
)
from cdl_python.CDL.Logical.Sources import (
    Constant as BoolConstant, Pulse as BoolPulse, SampleTrigger, TimeTable as BoolTimeTable
)


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


# ============================================================================
# Integers.Sources Tests
# ============================================================================

class TestIntegerConstant:
    """Test the Integer Constant source block"""

    def test_constant_output(self):
        """Test that constant outputs the specified integer value"""
        const = IntConstant(k=5)
        result = const.compute()
        assert result['y'] == 5

    def test_constant_with_different_values(self):
        """Test constant with various integer values"""
        for k in [0, 1, -3, 100, -50]:
            const = IntConstant(k=k)
            result = const.compute()
            assert result['y'] == k

    def test_constant_multiple_calls(self):
        """Test that constant returns same value on multiple calls"""
        const = IntConstant(k=42)
        for _ in range(10):
            result = const.compute()
            assert result['y'] == 42


class TestIntegerPulse:
    """Test the Integer Pulse source block"""

    def test_pulse_at_time_zero(self):
        """Test pulse output at t=0 (should be high)"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        pulse = IntPulse(time_manager=tm, amplitude=10, width=0.5, period=1.0, shift=0.0, offset=5)
        result = pulse.compute()
        assert result['y'] == 15  # offset + amplitude

    def test_pulse_low_period(self):
        """Test pulse during low period"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        pulse = IntPulse(time_manager=tm, amplitude=10, width=0.5, period=1.0, shift=0.0, offset=5)

        # Advance to t=0.6 (low period)
        for _ in range(6):
            tm.advance(0.1)
        result = pulse.compute()
        assert result['y'] == 5  # offset only

    def test_pulse_periodic_behavior(self):
        """Test that pulse repeats correctly"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        pulse = IntPulse(time_manager=tm, amplitude=8, width=0.5, period=1.0, shift=0.0, offset=2)

        # First cycle high
        result = pulse.compute()
        assert result['y'] == 10

        # Advance to second cycle at t=1.05 (safely in high period)
        for _ in range(11):
            tm.advance(0.1)
        result = pulse.compute()
        assert result['y'] == 10

    def test_pulse_with_shift(self):
        """Test pulse with time shift"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        pulse = IntPulse(time_manager=tm, amplitude=5, width=0.5, period=1.0, shift=0.3, offset=0)

        # At t=0, adjusted time is -0.3, should be low (offset)
        result = pulse.compute()
        assert result['y'] == 0

        # At t=0.4, adjusted time is 0.1, should be high
        for _ in range(4):
            tm.advance(0.1)
        result = pulse.compute()
        assert result['y'] == 5


class TestIntegerTimeTable:
    """Test the Integer TimeTable source block"""

    def test_timetable_basic(self):
        """Test basic time table lookup"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        table = [[0.0, 10], [1.0, 20], [2.0, 30]]
        tt = IntTimeTable(time_manager=tm, table=table, timeScale=1.0, period=10.0)

        # At t=0, should return 10
        result = tt.compute()
        assert result['y'] == 10

        # At t=1.5, should return 20 (constant segments)
        for _ in range(15):
            tm.advance(0.1)
        result = tt.compute()
        assert result['y'] == 20

    def test_timetable_periodic(self):
        """Test periodic behavior of time table"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        table = [[0.0, 5], [1.0, 10]]
        tt = IntTimeTable(time_manager=tm, table=table, timeScale=1.0, period=2.0)

        # At t=2.5, should wrap to t=0.5, value should be 5
        for _ in range(25):
            tm.advance(0.1)
        result = tt.compute()
        assert result['y'] == 5


# ============================================================================
# Logical.Sources Tests
# ============================================================================

class TestBooleanConstant:
    """Test the Boolean Constant source block"""

    def test_constant_true(self):
        """Test constant with True value"""
        const = BoolConstant(k=True)
        result = const.compute()
        assert result['y'] is True

    def test_constant_false(self):
        """Test constant with False value"""
        const = BoolConstant(k=False)
        result = const.compute()
        assert result['y'] is False

    def test_constant_multiple_calls(self):
        """Test that constant returns same value on multiple calls"""
        const = BoolConstant(k=True)
        for _ in range(10):
            result = const.compute()
            assert result['y'] is True


class TestBooleanPulse:
    """Test the Boolean Pulse source block"""

    def test_pulse_at_time_zero(self):
        """Test pulse output at t=0 (should be high)"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        pulse = BoolPulse(time_manager=tm, width=0.5, period=1.0, shift=0.0)
        result = pulse.compute()
        assert result['y'] is True

    def test_pulse_low_period(self):
        """Test pulse during low period"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        pulse = BoolPulse(time_manager=tm, width=0.5, period=1.0, shift=0.0)

        # Advance to t=0.6 (low period)
        for _ in range(6):
            tm.advance(0.1)
        result = pulse.compute()
        assert result['y'] is False

    def test_pulse_periodic_behavior(self):
        """Test that pulse repeats correctly"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        pulse = BoolPulse(time_manager=tm, width=0.5, period=1.0, shift=0.0)

        # First cycle high
        result = pulse.compute()
        assert result['y'] is True

        # Advance to second cycle at t=1.05 (safely in high period)
        for _ in range(11):
            tm.advance(0.1)
        result = pulse.compute()
        assert result['y'] is True

    def test_pulse_with_shift(self):
        """Test pulse with time shift"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        pulse = BoolPulse(time_manager=tm, width=0.5, period=1.0, shift=0.3)

        # At t=0, adjusted time is -0.3, should be False
        result = pulse.compute()
        assert result['y'] is False

        # At t=0.4, adjusted time is 0.1, should be True
        for _ in range(4):
            tm.advance(0.1)
        result = pulse.compute()
        assert result['y'] is True


class TestSampleTrigger:
    """Test the SampleTrigger source block"""

    def test_trigger_at_sample_time(self):
        """Test that trigger fires at exact sample times"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        trigger = SampleTrigger(time_manager=tm, period=1.0, shift=0.0)

        # At t=0, should trigger
        result = trigger.compute()
        assert result['y'] is True

        # Still at t=0, should not trigger again
        result = trigger.compute()
        assert result['y'] is False

    def test_trigger_between_samples(self):
        """Test that trigger is False between sample times"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        trigger = SampleTrigger(time_manager=tm, period=1.0, shift=0.0)

        # At t=0.5, should not trigger
        for _ in range(5):
            tm.advance(0.1)
        result = trigger.compute()
        assert result['y'] is False

    def test_trigger_periodic(self):
        """Test that trigger fires periodically"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.5)
        trigger = SampleTrigger(time_manager=tm, period=1.0, shift=0.0)

        # At t=0, should trigger
        result = trigger.compute()
        assert result['y'] is True

        # Advance to t=1.0, should trigger again
        tm.advance(0.5)
        tm.advance(0.5)
        result = trigger.compute()
        assert result['y'] is True


class TestBooleanTimeTable:
    """Test the Boolean TimeTable source block"""

    def test_timetable_basic(self):
        """Test basic boolean time table lookup"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        table = [[0.0, 0], [1.0, 1], [2.0, 0]]
        tt = BoolTimeTable(time_manager=tm, table=table, timeScale=1.0, period=10.0)

        # At t=0, should return False
        result = tt.compute()
        assert result['y'] is False

        # At t=1.5, should return True
        for _ in range(15):
            tm.advance(0.1)
        result = tt.compute()
        assert result['y'] is True


# ============================================================================
# Reals.Sources Tests (New Blocks)
# ============================================================================

class TestRealPulse:
    """Test the Real Pulse source block"""

    def test_pulse_at_time_zero(self):
        """Test pulse output at t=0 (should be high)"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        pulse = RealPulse(time_manager=tm, amplitude=5.0, width=0.5, period=1.0, shift=0.0, offset=2.0)
        result = pulse.compute()
        assert result['y'] == pytest.approx(7.0)

    def test_pulse_low_period(self):
        """Test pulse during low period"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        pulse = RealPulse(time_manager=tm, amplitude=5.0, width=0.5, period=1.0, shift=0.0, offset=2.0)

        # Advance to t=0.6 (low period)
        for _ in range(6):
            tm.advance(0.1)
        result = pulse.compute()
        assert result['y'] == pytest.approx(2.0)

    def test_pulse_periodic_behavior(self):
        """Test that pulse repeats correctly"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        pulse = RealPulse(time_manager=tm, amplitude=3.0, width=0.5, period=1.0, shift=0.0, offset=1.0)

        # First cycle high
        result = pulse.compute()
        assert result['y'] == pytest.approx(4.0)

        # Advance to second cycle at t=1.05 (safely in high period)
        for _ in range(11):
            tm.advance(0.1)
        result = pulse.compute()
        assert result['y'] == pytest.approx(4.0)


class TestRamp:
    """Test the Ramp source block"""

    def test_ramp_before_start(self):
        """Test ramp output before start time"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        ramp = Ramp(time_manager=tm, height=10.0, duration=2.0, offset=5.0, startTime=1.0)

        # At t=0, should return offset
        result = ramp.compute()
        assert result['y'] == pytest.approx(5.0)

    def test_ramp_during_ramp(self):
        """Test ramp output during ramping"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        ramp = Ramp(time_manager=tm, height=10.0, duration=2.0, offset=5.0, startTime=0.0)

        # At t=1.0 (halfway), should be offset + height/2
        for _ in range(10):
            tm.advance(0.1)
        result = ramp.compute()
        assert result['y'] == pytest.approx(10.0, abs=1e-5)

    def test_ramp_after_end(self):
        """Test ramp output after completion"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        ramp = Ramp(time_manager=tm, height=10.0, duration=2.0, offset=5.0, startTime=0.0)

        # At t=3.0 (after ramp), should be offset + height
        for _ in range(30):
            tm.advance(0.1)
        result = ramp.compute()
        assert result['y'] == pytest.approx(15.0)

    def test_ramp_at_exact_end(self):
        """Test ramp at exact end time"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        ramp = Ramp(time_manager=tm, height=8.0, duration=1.0, offset=2.0, startTime=0.0)

        # At t=1.0 (exact end), should be offset + height
        for _ in range(10):
            tm.advance(0.1)
        result = ramp.compute()
        assert result['y'] == pytest.approx(10.0, abs=1e-5)


class TestRealTimeTable:
    """Test the Real TimeTable source block"""

    def test_timetable_linear_interpolation(self):
        """Test time table with linear interpolation"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        table = [[0.0, 0.0], [1.0, 10.0], [2.0, 5.0]]
        tt = RealTimeTable(
            time_manager=tm,
            table=table,
            smoothness=Smoothness.LINEAR_SEGMENTS,
            extrapolation=Extrapolation.HOLD_LAST_POINT
        )

        # At t=0.5, should interpolate to 5.0
        for _ in range(5):
            tm.advance(0.1)
        result = tt.compute()
        assert result['y'] == pytest.approx(5.0, abs=1e-5)

    def test_timetable_constant_segments(self):
        """Test time table with constant segments"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        table = [[0.0, 10.0], [1.0, 20.0], [2.0, 30.0]]
        tt = RealTimeTable(
            time_manager=tm,
            table=table,
            smoothness=Smoothness.CONSTANT_SEGMENTS,
            extrapolation=Extrapolation.HOLD_LAST_POINT
        )

        # At t=0.5, should hold value from t=0
        for _ in range(5):
            tm.advance(0.1)
        result = tt.compute()
        assert result['y'] == pytest.approx(10.0)

    def test_timetable_periodic_extrapolation(self):
        """Test time table with periodic extrapolation"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        table = [[0.0, 5.0], [1.0, 10.0]]
        tt = RealTimeTable(
            time_manager=tm,
            table=table,
            smoothness=Smoothness.LINEAR_SEGMENTS,
            extrapolation=Extrapolation.PERIODIC
        )

        # At t=2.5, should wrap to t=0.5 and interpolate
        for _ in range(25):
            tm.advance(0.1)
        result = tt.compute()
        assert result['y'] == pytest.approx(7.5, abs=1e-5)

    def test_timetable_with_offset(self):
        """Test time table with offset"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        table = [[0.0, 0.0], [1.0, 10.0]]
        tt = RealTimeTable(
            time_manager=tm,
            table=table,
            smoothness=Smoothness.LINEAR_SEGMENTS,
            extrapolation=Extrapolation.HOLD_LAST_POINT,
            offset=[100.0]
        )

        # At t=0, should return 0 + offset = 100
        result = tt.compute()
        assert result['y'] == pytest.approx(100.0)


class TestCalendarTime:
    """Test the CalendarTime source block"""

    def test_calendar_time_at_zero(self):
        """Test calendar time at t=0 with default reference (NY2016)"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        cal = CalendarTime(time_manager=tm, zerTim=ZeroTime.NY2016)

        result = cal.compute()
        assert result['year'] == 2016
        assert result['month'] == 1
        assert result['day'] == 1
        assert result['hour'] == 0
        assert result['minute'] == pytest.approx(0.0)
        # January 1, 2016 was a Friday (weekDay=5)
        assert result['weekDay'] == 5

    def test_calendar_time_after_one_day(self):
        """Test calendar time after one day"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=3600)  # 1 hour steps
        cal = CalendarTime(time_manager=tm, zerTim=ZeroTime.NY2016)

        # Advance 24 hours (86400 seconds)
        for _ in range(24):
            tm.advance(3600)

        result = cal.compute()
        assert result['year'] == 2016
        assert result['month'] == 1
        assert result['day'] == 2
        assert result['hour'] == 0

    def test_calendar_time_with_custom_year(self):
        """Test calendar time with custom reference year"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        cal = CalendarTime(time_manager=tm, zerTim=ZeroTime.CUSTOM, yearRef=2020)

        result = cal.compute()
        assert result['year'] == 2020
        assert result['month'] == 1
        assert result['day'] == 1

    def test_calendar_time_with_offset(self):
        """Test calendar time with timezone offset"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        # Offset of 3 hours (10800 seconds)
        cal = CalendarTime(time_manager=tm, zerTim=ZeroTime.NY2016, offset=10800.0)

        result = cal.compute()
        assert result['hour'] == 3
        assert result['minute'] == pytest.approx(0.0)


class TestCivilTime:
    """Test the CivilTime source block"""

    def test_civil_time_at_zero(self):
        """Test civil time at t=0"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        civil = CivilTime(time_manager=tm)

        result = civil.compute()
        assert result['y'] == pytest.approx(0.0)

    def test_civil_time_progression(self):
        """Test civil time progresses with simulation time"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=1.0)
        civil = CivilTime(time_manager=tm)

        # At t=0
        result = civil.compute()
        assert result['y'] == pytest.approx(0.0)

        # Advance to t=5.0
        for _ in range(5):
            tm.advance(1.0)

        result = civil.compute()
        assert result['y'] == pytest.approx(5.0)

    def test_civil_time_fractional(self):
        """Test civil time with fractional seconds"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        civil = CivilTime(time_manager=tm)

        # Advance to t=3.7
        for _ in range(37):
            tm.advance(0.1)

        result = civil.compute()
        assert result['y'] == pytest.approx(3.7, abs=1e-5)
