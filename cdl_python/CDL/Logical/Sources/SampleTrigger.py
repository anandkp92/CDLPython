"""
Sample trigger source block.

Generates trigger signals at specified sampling intervals.
"""

from typing import Dict, Any
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager
import math


class SampleTrigger(CDLBlock):
    """Generate sample trigger signal

    The Boolean output y is a trigger signal that is only True at sample times
    (defined by parameter period) and is otherwise False.

    The trigger signal is generated an infinite number of times, aligned with time=shift.

    Parameters:
        period: Sample period (seconds, must be > 0)
        shift: Shift time for output (seconds, default=0)

    Outputs:
        y: Output with trigger value (True only at exact sample times)
    """

    def __init__(self, time_manager: TimeManager, period: float = 1.0, shift: float = 0.0):
        """Initialize SampleTrigger block

        Args:
            time_manager: Time manager for getting current time
            period: Sample period (seconds, must be > 0)
            shift: Shift time for output (seconds)
        """
        super().__init__(time_manager)

        if period <= 0:
            raise ValueError(f"period must be > 0, got {period}")

        self.period = period
        self.shift = shift

        # Calculate first sample time
        # Align with shift modulo period
        self.t0 = (shift % period)

        # Track last time we checked
        self._last_time = None
        self._last_trigger = False

    def compute(self) -> Dict[str, Any]:
        """Compute trigger output

        Returns:
            Dictionary with 'y': True if at sample time, False otherwise
        """
        current_time = self.get_time()

        # Adjust time by shift
        adjusted_time = current_time - self.shift

        # Check if we're at a sample time
        # We trigger when adjusted_time is a multiple of period (within tolerance)
        if adjusted_time < 0:
            # Before first sample
            trigger = False
        else:
            # Calculate how close we are to a multiple of period
            time_in_period = adjusted_time % self.period
            # Trigger if we're very close to the start of a period (within a small tolerance)
            # Also check if this is a new sample time (not same as last check)
            is_sample_time = time_in_period < 1e-9 or (self.period - time_in_period) < 1e-9

            # Only trigger if this is different from last time (edge-triggered)
            if is_sample_time and (self._last_time is None or
                                   abs(current_time - self._last_time) > 1e-9):
                trigger = True
                self._last_time = current_time
            else:
                trigger = False

        self._last_trigger = trigger
        return {'y': trigger}
