# ABOUTME: IntegratorWithReset block - integrates input signal with reset capability.
# ABOUTME: Implements y(t) = y_start + integral(k*u) with trigger-based reset functionality.

from typing import Dict, Any, Optional
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class IntegratorWithReset(CDLBlock):
    """
    Output the integral of the input signal with reset capability.

    Implements:
        y(t) = y_start + integral(k * u(t))

    When trigger changes from False to True, the integrator is reset
    to the value of y_reset_in.

    Parameters:
        k: Integrator gain (default: 1.0)
        y_start: Initial value of output (default: 0.0)

    Inputs:
        u: Input to be integrated
        trigger: When True, resets integrator to y_reset_in
        y_reset_in: Value to reset integrator to when triggered

    Outputs:
        y: Value of the integrator

    State:
        Maintains integrated value and last computation time between calls.
    """

    def __init__(
        self,
        time_manager: Optional[TimeManager] = None,
        k: float = 1.0,
        y_start: float = 0.0
    ):
        """
        Initialize IntegratorWithReset.

        Args:
            time_manager: TimeManager instance (required for integration)
            k: Integrator gain
            y_start: Initial value of output
        """
        super().__init__(time_manager)
        self.k = k
        self.y_start = y_start

        # Initialize state
        self._state = {
            'y': y_start,
            'last_time': None,
            'last_trigger': False
        }

    def compute(self, u: float, trigger: bool, y_reset_in: float) -> Dict[str, Any]:
        """
        Compute integrator output.

        Args:
            u: Input value to integrate
            trigger: Reset trigger (resets when True)
            y_reset_in: Value to reset to when triggered

        Returns:
            Dictionary with output 'y' (integrated value)

        Raises:
            RuntimeError: If no TimeManager is set
        """
        current_time = self.get_time()

        # Detect rising edge of trigger (False -> True)
        if trigger and not self._state['last_trigger']:
            # Reset integrator
            self._state['y'] = y_reset_in
            self._state['last_time'] = current_time
            self._state['last_trigger'] = trigger
            return {'y': self._state['y']}

        # First call - initialize without integration
        if self._state['last_time'] is None:
            self._state['last_time'] = current_time
            self._state['last_trigger'] = trigger
            return {'y': self._state['y']}

        # Compute time step
        dt = current_time - self._state['last_time']

        # Integrate: dy/dt = k * u
        if dt > 0:
            self._state['y'] += self.k * u * dt

        # Update state
        self._state['last_time'] = current_time
        self._state['last_trigger'] = trigger

        return {'y': self._state['y']}

    def reset_state(self):
        """Reset integrator to initial conditions"""
        self._state = {
            'y': self.y_start,
            'last_time': None,
            'last_trigger': False
        }
