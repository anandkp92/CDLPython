# ABOUTME: Accumulating timer block - accumulates time when input is true
# ABOUTME: Holds accumulated value when input is false, can be reset
from typing import Any, Dict, Optional
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class TimerAccumulating(CDLBlock):
    """
    Accumulating timer block

    Accumulates time while input is true.
    Holds accumulated value when input is false.
    Can be reset to zero with reset input.

    Parameters:
        t: Threshold time for comparison (seconds, default: 0)

    Inputs:
        u: Boolean input that activates timer
        reset: Reset timer to zero

    Outputs:
        y: Accumulated time (seconds)
        passed: True if accumulated time > threshold
    """

    def __init__(
        self,
        time_manager: Optional[TimeManager] = None,
        t: float = 0.0
    ):
        """
        Initialize TimerAccumulating block.

        Args:
            time_manager: TimeManager instance
            t: Threshold time (seconds)
        """
        super().__init__(time_manager)
        self.t = t
        self._accumulated = 0.0
        self._entry_time = None
        self._passed = (t <= 0)
        self._prev_u = False
        self._prev_reset = False

    def compute(self, u: bool, reset: bool) -> Dict[str, Any]:
        """
        Compute accumulating timer output.

        Args:
            u: Boolean input
            reset: Reset input

        Returns:
            Dictionary with keys 'y' (accumulated time) and 'passed' (threshold exceeded)
        """
        current_time = self.get_time()

        # Detect rising edge of reset
        reset_rising = reset and not self._prev_reset

        if reset_rising or reset:
            # Reset to zero
            self._accumulated = 0.0
            self._entry_time = None
            self._passed = (self.t <= 0)
        elif u:
            # Timer is running
            if self._entry_time is None:
                # Just became true - start new accumulation period
                self._entry_time = current_time
            else:
                # Continue accumulating
                elapsed_this_period = current_time - self._entry_time
                self._accumulated += elapsed_this_period
                self._entry_time = current_time

            # Check if threshold passed
            if self._accumulated >= self.t:
                self._passed = True

        else:
            # Timer is paused (u is false)
            # Hold accumulated value, but clear entry time
            self._entry_time = None
            # Keep _passed state

        # Update previous values
        self._prev_u = u
        self._prev_reset = reset

        return {'y': self._accumulated, 'passed': self._passed}

    def reset_state(self):
        """Reset the block state"""
        self._accumulated = 0.0
        self._entry_time = None
        self._passed = (self.t <= 0)
        self._prev_u = False
        self._prev_reset = False
