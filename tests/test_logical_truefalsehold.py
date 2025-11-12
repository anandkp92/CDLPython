# ABOUTME: Test suite for TrueFalseHold block
# ABOUTME: Tests true/false signal holding behavior
import pytest
from cdl_python.time_manager import TimeManager, ExecutionMode
from cdl_python.CDL.Logical import TrueFalseHold


class TestTrueFalseHold:
    """Test the TrueFalseHold block"""

    def test_initial_output_follows_input(self):
        """Test that initial output follows input"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        hold = TrueFalseHold(time_manager=tm, trueHoldDuration=1.0, falseHoldDuration=1.0)

        result = hold.compute(u=True)
        assert result['y'] is True

        # Reset and test with false
        hold.reset_state()
        result = hold.compute(u=False)
        assert result['y'] is False

    def test_true_hold_duration(self):
        """Test that true signal is held for specified duration"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        hold = TrueFalseHold(time_manager=tm, trueHoldDuration=1.0, falseHoldDuration=1.0)

        # Start with true
        result = hold.compute(u=True)
        assert result['y'] is True

        # Advance time and switch to false
        tm.advance(dt=0.3)
        result = hold.compute(u=False)
        # Output should still be true (holding)
        assert result['y'] is True

        # Advance more but still within hold duration
        tm.advance(dt=0.5)
        result = hold.compute(u=False)
        # Still holding true
        assert result['y'] is True

        # Advance past the hold duration
        tm.advance(dt=0.3)  # Total 1.1 seconds
        result = hold.compute(u=False)
        # Now it should switch to false
        assert result['y'] is False

    def test_false_hold_duration(self):
        """Test that false signal is held for specified duration"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        hold = TrueFalseHold(time_manager=tm, trueHoldDuration=1.0, falseHoldDuration=1.0)

        # Start with false
        result = hold.compute(u=False)
        assert result['y'] is False

        # Advance time and switch to true
        tm.advance(dt=0.3)
        result = hold.compute(u=True)
        # Output should still be false (holding)
        assert result['y'] is False

        # Advance more but still within hold duration
        tm.advance(dt=0.5)
        result = hold.compute(u=True)
        # Still holding false
        assert result['y'] is False

        # Advance past the hold duration
        tm.advance(dt=0.3)  # Total 1.1 seconds
        result = hold.compute(u=True)
        # Now it should switch to true
        assert result['y'] is True

    def test_different_hold_durations(self):
        """Test with different true and false hold durations"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        hold = TrueFalseHold(
            time_manager=tm,
            trueHoldDuration=0.5,  # Shorter
            falseHoldDuration=1.5  # Longer
        )

        # Start with true
        result = hold.compute(u=True)
        assert result['y'] is True

        # Switch to false after 0.2s
        tm.advance(dt=0.2)
        result = hold.compute(u=False)
        # Should hold true (0.2 < 0.5)
        assert result['y'] is True

        # Advance to 0.6s total
        tm.advance(dt=0.4)
        result = hold.compute(u=False)
        # Should now be false (0.6 > 0.5)
        assert result['y'] is False

        # Switch back to true after 0.3s more (0.9s total)
        tm.advance(dt=0.3)
        result = hold.compute(u=True)
        # Should hold false (0.3 < 1.5)
        assert result['y'] is False

        # Advance to 1.8s total (0.9s since false started)
        tm.advance(dt=0.9)
        result = hold.compute(u=True)
        # Should now be true (0.9 + 0.3 = 1.2, but we need 1.5)
        assert result['y'] is False

        # Advance to 2.1s total (1.5s since false started)
        tm.advance(dt=0.3)
        result = hold.compute(u=True)
        # Should now be true (1.5 >= 1.5)
        assert result['y'] is True

    def test_input_changes_during_hold(self):
        """Test that input changes during hold period are ignored until hold expires"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        hold = TrueFalseHold(time_manager=tm, trueHoldDuration=1.0, falseHoldDuration=1.0)

        # Start with true
        result = hold.compute(u=True)
        assert result['y'] is True

        # Switch to false
        tm.advance(dt=0.2)
        result = hold.compute(u=False)
        assert result['y'] is True  # Holding

        # Switch back to true (should still hold original true)
        tm.advance(dt=0.3)
        result = hold.compute(u=True)
        assert result['y'] is True  # Still holding from original

        # Switch to false again
        tm.advance(dt=0.2)
        result = hold.compute(u=False)
        assert result['y'] is True  # Still holding

        # After hold duration expires
        tm.advance(dt=0.4)  # Total 1.1s
        result = hold.compute(u=False)
        assert result['y'] is False  # Now follows input

    def test_zero_hold_duration(self):
        """Test with zero hold duration (immediate switching)"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        hold = TrueFalseHold(time_manager=tm, trueHoldDuration=0.0, falseHoldDuration=0.0)

        result = hold.compute(u=True)
        assert result['y'] is True

        result = hold.compute(u=False)
        assert result['y'] is False

        result = hold.compute(u=True)
        assert result['y'] is True
