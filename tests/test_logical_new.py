# ABOUTME: Tests for new Logical blocks (Proof, VariablePulse)
import pytest
from cdl_python.time_manager import TimeManager, ExecutionMode
from cdl_python.CDL.Logical import Proof, VariablePulse


class TestVariablePulse:
    """Test VariablePulse block"""

    def test_generates_pulse(self):
        """Test basic pulse generation"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        pulse = VariablePulse(time_manager=tm, period=1.0)

        # Before first pulse
        result = pulse.compute(u=0.3)
        assert result['y'] is False

        # At period start (t=1.0), pulse starts
        tm.advance(dt=1.0)
        result = pulse.compute(u=0.3)  # Request 0.3s pulse width
        assert result['y'] is True

        # During pulse (t=1.2)
        tm.advance(dt=0.2)
        result = pulse.compute(u=0.3)
        assert result['y'] is True

        # After pulse ends (t=1.4 > 1.0+0.3)
        tm.advance(dt=0.2)
        result = pulse.compute(u=0.3)
        assert result['y'] is False

    def test_variable_width(self):
        """Test that pulse width varies with input"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        pulse = VariablePulse(time_manager=tm, period=2.0)

        # Move to first pulse
        tm.advance(dt=2.0)
        pulse.compute(u=0.5)  # Wide pulse

        # Check it lasts 0.5s
        tm.advance(dt=0.4)
        assert pulse.compute(u=0.5)['y'] is True
        tm.advance(dt=0.2)
        assert pulse.compute(u=0.5)['y'] is False


    def test_invalid_period(self):
        """Test error on invalid period"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        with pytest.raises(ValueError):
            VariablePulse(time_manager=tm, period=0.0)


class TestProof:
    """Test Proof block"""

    def test_signal_matches_setpoint(self):
        """Test yTest when signal matches setpoint"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=1.0)
        proof = Proof(time_manager=tm, delTes=5.0, delTim=10.0)

        # Signal matches setpoint immediately
        result = proof.compute(u=True, uSet=True)
        # Before test delay, yTest should be True (not failing yet)
        assert result['yTest'] is True

        # After test delay
        tm.advance(dt=6.0)
        result = proof.compute(u=True, uSet=True)
        assert result['yTest'] is True  # Matches

    def test_signal_mismatch_detected(self):
        """Test yTest when signal doesn't match setpoint"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=1.0)
        proof = Proof(time_manager=tm, delTes=5.0, delTim=10.0)

        # Signal doesn't match setpoint
        proof.compute(u=False, uSet=True)

        # After test delay, should detect mismatch
        tm.advance(dt=6.0)
        result = proof.compute(u=False, uSet=True)
        assert result['yTest'] is False  # Mismatch detected

    def test_locked_on_detection(self):
        """Test yLocOn when signal stuck at true"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=1.0)
        proof = Proof(time_manager=tm, delTes=5.0, delTim=10.0)

        # Keep signal at True
        proof.compute(u=True, uSet=True)

        # Before delTim, not locked
        tm.advance(dt=9.0)
        result = proof.compute(u=True, uSet=True)
        assert result['yLocOn'] is False

        # After delTim, locked on
        tm.advance(dt=2.0)
        result = proof.compute(u=True, uSet=True)
        assert result['yLocOn'] is True

    def test_locked_off_detection(self):
        """Test yLocOff when signal stuck at false"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=1.0)
        proof = Proof(time_manager=tm, delTes=5.0, delTim=10.0)

        # Keep signal at False
        proof.compute(u=False, uSet=False)

        # After delTim, should be locked off
        tm.advance(dt=11.0)
        result = proof.compute(u=False, uSet=False)
        assert result['yLocOff'] is True
