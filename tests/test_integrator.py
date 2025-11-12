# ABOUTME: Unit tests for IntegratorWithReset block.
# ABOUTME: Tests stateful block behavior, time management integration, and reset functionality.

import pytest
from cdl_python.CDL.Reals.IntegratorWithReset import IntegratorWithReset
from cdl_python.time_manager import TimeManager, ExecutionMode


class TestIntegratorWithReset:
    """Tests for IntegratorWithReset block"""

    def test_initialization(self):
        """Test integrator initialization with default parameters"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION)
        integrator = IntegratorWithReset(time_manager=tm)

        result = integrator.compute(u=0.0, trigger=False, y_reset_in=0.0)
        assert result['y'] == 0.0

    def test_initialization_with_y_start(self):
        """Test integrator initialization with custom y_start"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION)
        integrator = IntegratorWithReset(time_manager=tm, y_start=5.0)

        result = integrator.compute(u=0.0, trigger=False, y_reset_in=0.0)
        assert result['y'] == 5.0

    def test_integration_constant_input(self):
        """Test integration with constant input"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        integrator = IntegratorWithReset(time_manager=tm, k=1.0, y_start=0.0)

        # First call at t=0
        result = integrator.compute(u=2.0, trigger=False, y_reset_in=0.0)
        assert result['y'] == 0.0

        # Advance time and compute at t=0.1
        tm.advance()
        result = integrator.compute(u=2.0, trigger=False, y_reset_in=0.0)
        # y = y_start + k * u * dt = 0 + 1 * 2 * 0.1 = 0.2
        assert abs(result['y'] - 0.2) < 1e-10

        # Advance time and compute at t=0.2
        tm.advance()
        result = integrator.compute(u=2.0, trigger=False, y_reset_in=0.0)
        # y = 0.2 + 1 * 2 * 0.1 = 0.4
        assert abs(result['y'] - 0.4) < 1e-10

    def test_integration_with_gain(self):
        """Test integration with gain parameter"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        integrator = IntegratorWithReset(time_manager=tm, k=2.0, y_start=0.0)

        # First call
        integrator.compute(u=1.0, trigger=False, y_reset_in=0.0)

        # After 0.1s with k=2.0, u=1.0
        tm.advance()
        result = integrator.compute(u=1.0, trigger=False, y_reset_in=0.0)
        # y = 0 + 2 * 1 * 0.1 = 0.2
        assert abs(result['y'] - 0.2) < 1e-10

    def test_trigger_reset(self):
        """Test integrator reset with trigger"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        integrator = IntegratorWithReset(time_manager=tm, k=1.0, y_start=0.0)

        # Integrate for a while
        integrator.compute(u=2.0, trigger=False, y_reset_in=0.0)
        tm.advance()
        integrator.compute(u=2.0, trigger=False, y_reset_in=0.0)
        tm.advance()
        result = integrator.compute(u=2.0, trigger=False, y_reset_in=0.0)
        # Should be around 0.4
        assert result['y'] > 0.3

        # Now trigger reset to 10.0
        tm.advance()
        result = integrator.compute(u=2.0, trigger=True, y_reset_in=10.0)
        assert result['y'] == 10.0

        # Continue integrating from 10.0
        tm.advance()
        result = integrator.compute(u=2.0, trigger=False, y_reset_in=0.0)
        # y = 10.0 + 1 * 2 * 0.1 = 10.2
        assert abs(result['y'] - 10.2) < 1e-10

    def test_negative_integration(self):
        """Test integration with negative input"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        integrator = IntegratorWithReset(time_manager=tm, k=1.0, y_start=5.0)

        # First call
        integrator.compute(u=-1.0, trigger=False, y_reset_in=0.0)

        # After 0.1s with negative input
        tm.advance()
        result = integrator.compute(u=-1.0, trigger=False, y_reset_in=0.0)
        # y = 5.0 + 1 * (-1) * 0.1 = 4.9
        assert abs(result['y'] - 4.9) < 1e-10

    def test_variable_timestep(self):
        """Test integration with variable timesteps"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION)
        integrator = IntegratorWithReset(time_manager=tm, k=1.0, y_start=0.0)

        # First call at t=0
        integrator.compute(u=2.0, trigger=False, y_reset_in=0.0)

        # Advance by 0.5s
        tm.advance(dt=0.5)
        result = integrator.compute(u=2.0, trigger=False, y_reset_in=0.0)
        # y = 0 + 1 * 2 * 0.5 = 1.0
        assert abs(result['y'] - 1.0) < 1e-10

        # Advance by 0.2s
        tm.advance(dt=0.2)
        result = integrator.compute(u=2.0, trigger=False, y_reset_in=0.0)
        # y = 1.0 + 1 * 2 * 0.2 = 1.4
        assert abs(result['y'] - 1.4) < 1e-10

    def test_reset_state_method(self):
        """Test manual state reset"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        integrator = IntegratorWithReset(time_manager=tm, k=1.0, y_start=3.0)

        # Integrate
        integrator.compute(u=2.0, trigger=False, y_reset_in=0.0)
        tm.advance()
        integrator.compute(u=2.0, trigger=False, y_reset_in=0.0)

        # Reset state
        integrator.reset_state()

        # Should restart from y_start
        tm.advance()
        result = integrator.compute(u=0.0, trigger=False, y_reset_in=0.0)
        assert result['y'] == 3.0

    def test_requires_time_manager(self):
        """Test that integrator raises error without TimeManager"""
        integrator = IntegratorWithReset(time_manager=None)

        with pytest.raises(RuntimeError, match="requires a TimeManager"):
            integrator.compute(u=1.0, trigger=False, y_reset_in=0.0)
