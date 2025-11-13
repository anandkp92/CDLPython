# ABOUTME: Derivative - Compute time derivative of input signal
from typing import Any, Dict, Optional
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class Derivative(CDLBlock):
    """Compute time derivative of input signal

    Calculates dy/dt using numerical differentiation.
    Uses backward difference: dy/dt ≈ (u - u_prev) / dt

    Output is limited by y_max parameter.

    Note: This is a simplified implementation using numerical differentiation.
    In practice, derivative blocks often include filtering to reduce noise sensitivity.

    Used for:
    - D-term in PID controllers
    - Rate-of-change monitoring
    - Velocity from position
    - Trend detection
    """

    def __init__(self, time_manager: TimeManager, y_max: float = float('inf'), y_start: float = 0.0):
        """Initialize Derivative block

        Args:
            time_manager: Time manager for timestep
            y_max: Maximum absolute value of output
            y_start: Initial derivative value
        """
        super().__init__(time_manager)
        self.y_max = y_max
        self.y_start = y_start

        # State
        self._previous_u: Optional[float] = None
        self._previous_time: Optional[float] = None
        self._y = y_start

    def compute(self, u: float) -> Dict[str, Any]:
        """Compute derivative

        Args:
            u: Input signal

        Returns:
            Dictionary with 'y': time derivative of input
        """
        current_time = self.get_time()

        if self._previous_u is None:
            # First call: no derivative yet
            self._y = self.y_start
        else:
            # Compute time step
            dt = current_time - self._previous_time

            if dt > 0:
                # Compute derivative using backward difference
                self._y = (u - self._previous_u) / dt

                # Limit output
                self._y = max(-self.y_max, min(self.y_max, self._y))

        # Store for next call
        self._previous_u = u
        self._previous_time = current_time

        return {'y': self._y}
