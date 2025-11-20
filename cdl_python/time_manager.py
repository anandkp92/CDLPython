# ABOUTME: TimeManager for CDL blocks - manages time in simulation and real-time modes.
# ABOUTME: Provides unified time interface that blocks query during execution.

import time
from enum import Enum
from typing import Optional
from threading import Lock


class ExecutionMode(Enum):
    """Execution mode for CDL system"""
    SIMULATION = "simulation"
    REALTIME = "realtime"


class TimeManager:
    """
    Manages time for CDL block execution.

    Supports two modes:
    - SIMULATION: Manual time advancement with fixed or variable timesteps
    - REALTIME: Wall-clock time for actual building control

    Thread-safe for future CPRE asynchronous operation.

    Example:
        # Simulation mode
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        tm.advance()  # Advances by 0.1 seconds

        # Real-time mode
        tm = TimeManager(mode=ExecutionMode.REALTIME)
        current = tm.get_time()  # Returns wall-clock time
    """

    def __init__(
        self,
        mode: ExecutionMode = ExecutionMode.REALTIME,
        start_time: Optional[float] = None,
        time_step: Optional[float] = None
    ):
        """
        Initialize TimeManager.

        Args:
            mode: ExecutionMode.SIMULATION or ExecutionMode.REALTIME
            start_time: Initial time (default: 0.0 for simulation, wall-clock for realtime)
            time_step: Default timestep for simulation mode (seconds)
        """
        self.mode = mode
        self.time_step = time_step
        self._lock = Lock()

        if start_time is not None:
            self._current_time = start_time
        else:
            if mode == ExecutionMode.SIMULATION:
                self._current_time = 0.0
            else:
                self._current_time = time.time()

    def get_time(self) -> float:
        """
        Get current time.

        Returns:
            Current time in seconds (simulation time or wall-clock time)
        """
        with self._lock:
            if self.mode == ExecutionMode.REALTIME:
                self._current_time = time.time()
            return self._current_time

    def advance(self, dt: Optional[float] = None) -> float:
        """
        Advance time.

        In SIMULATION mode: increments by dt (or time_step if dt not provided)
        In REALTIME mode: updates to current wall-clock time

        Args:
            dt: Time increment in seconds (only used in SIMULATION mode)

        Returns:
            New current time

        Raises:
            ValueError: If in SIMULATION mode and neither dt nor time_step is set
        """
        with self._lock:
            if self.mode == ExecutionMode.SIMULATION:
                if dt is not None:
                    self._current_time += dt
                elif self.time_step is not None:
                    self._current_time += self.time_step
                else:
                    raise ValueError(
                        "SIMULATION mode requires dt parameter or time_step to be set"
                    )
            else:  # REALTIME
                self._current_time = time.time()

            return self._current_time

    def reset(self, start_time: Optional[float] = None):
        """
        Reset time manager.

        Args:
            start_time: New start time (default: 0.0 for simulation, current wall-clock for realtime)
        """
        with self._lock:
            if start_time is not None:
                self._current_time = start_time
            else:
                if self.mode == ExecutionMode.SIMULATION:
                    self._current_time = 0.0
                else:
                    self._current_time = time.time()

    def set_mode(self, mode: ExecutionMode, start_time: Optional[float] = None):
        """
        Change execution mode.

        Args:
            mode: New execution mode
            start_time: Optional start time for new mode
        """
        with self._lock:
            self.mode = mode
            if start_time is not None:
                self._current_time = start_time
            elif mode == ExecutionMode.REALTIME:
                self._current_time = time.time()

    def get_state(self) -> dict:
        """
        Get current state of TimeManager for checkpointing.

        Returns:
            Dictionary containing time manager state including:
            - mode: Execution mode (SIMULATION or REALTIME)
            - current_time: Current time value
            - time_step: Default timestep (if set)

        Example:
            >>> tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
            >>> tm.advance()
            >>> state = tm.get_state()
            >>> # state = {'mode': 'simulation', 'current_time': 0.1, 'time_step': 0.1}
        """
        with self._lock:
            return {
                'mode': self.mode.value,
                'current_time': self._current_time,
                'time_step': self.time_step
            }

    def set_state(self, state: dict):
        """
        Restore TimeManager state from checkpoint.

        Args:
            state: Dictionary containing state to restore (from get_state())

        Raises:
            ValueError: If state dictionary is invalid

        Example:
            >>> # Save state
            >>> saved_state = tm.get_state()
            >>> # ... some operations ...
            >>> # Restore state
            >>> tm.set_state(saved_state)
        """
        with self._lock:
            if 'mode' in state:
                self.mode = ExecutionMode(state['mode'])
            if 'current_time' in state:
                self._current_time = state['current_time']
            if 'time_step' in state:
                self.time_step = state['time_step']
