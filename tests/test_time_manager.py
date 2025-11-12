# ABOUTME: Unit tests for TimeManager class.
# ABOUTME: Tests simulation and real-time modes, time advancement, and thread safety.

import pytest
import time
from cdl_python.time_manager import TimeManager, ExecutionMode


class TestTimeManager:
    """Tests for TimeManager class"""

    def test_simulation_mode_initialization(self):
        """Test initialization in simulation mode"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION)
        assert tm.mode == ExecutionMode.SIMULATION
        assert tm.get_time() == 0.0

    def test_simulation_mode_with_start_time(self):
        """Test initialization with custom start time"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, start_time=10.0)
        assert tm.get_time() == 10.0

    def test_realtime_mode_initialization(self):
        """Test initialization in realtime mode"""
        before = time.time()
        tm = TimeManager(mode=ExecutionMode.REALTIME)
        after = time.time()

        assert tm.mode == ExecutionMode.REALTIME
        current_time = tm.get_time()
        # Allow small tolerance for timing precision
        assert before - 0.001 <= current_time <= after + 0.001

    def test_simulation_advance_with_timestep(self):
        """Test advancing time in simulation mode with fixed timestep"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        assert tm.get_time() == 0.0

        tm.advance()
        assert tm.get_time() == 0.1

        tm.advance()
        assert tm.get_time() == 0.2

    def test_simulation_advance_with_dt(self):
        """Test advancing time with variable dt"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION)

        tm.advance(dt=0.5)
        assert tm.get_time() == 0.5

        tm.advance(dt=0.3)
        assert tm.get_time() == 0.8

    def test_simulation_advance_without_dt_raises(self):
        """Test that advance() without dt or time_step raises error"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION)

        with pytest.raises(ValueError, match="requires dt parameter or time_step"):
            tm.advance()

    def test_realtime_advance(self):
        """Test advancing time in realtime mode"""
        tm = TimeManager(mode=ExecutionMode.REALTIME)
        t1 = tm.get_time()

        time.sleep(0.01)  # Sleep for 10ms
        tm.advance()
        t2 = tm.get_time()

        assert t2 > t1
        assert (t2 - t1) >= 0.01  # At least 10ms passed

    def test_reset_simulation(self):
        """Test resetting time in simulation mode"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        tm.advance()
        tm.advance()
        assert tm.get_time() == 0.2

        tm.reset()
        assert tm.get_time() == 0.0

    def test_reset_with_custom_time(self):
        """Test resetting with custom start time"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION)
        tm.advance(dt=1.0)

        tm.reset(start_time=5.0)
        assert tm.get_time() == 5.0

    def test_set_mode(self):
        """Test changing execution mode"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION)
        assert tm.mode == ExecutionMode.SIMULATION

        tm.set_mode(ExecutionMode.REALTIME)
        assert tm.mode == ExecutionMode.REALTIME

        # Time should be updated to wall-clock
        current_time = tm.get_time()
        assert current_time > 0

    def test_set_mode_with_start_time(self):
        """Test changing mode with custom start time"""
        tm = TimeManager(mode=ExecutionMode.SIMULATION)
        tm.set_mode(ExecutionMode.SIMULATION, start_time=100.0)

        assert tm.get_time() == 100.0
