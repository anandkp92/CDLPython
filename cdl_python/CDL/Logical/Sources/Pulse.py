"""
Boolean pulse source block.

Generates periodic boolean pulse signals.
"""

from typing import Dict, Any
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager
import math


class Pulse(CDLBlock):
    """Generate pulse signal of type Boolean

    Block that outputs a boolean pulse signal with specified period, width, and shift.

    The pulse signal is generated an infinite number of times, and aligned with time=shift.

    Parameters:
        width: Width of pulse in fraction of period (0 < width <= 1)
        period: Time for one period (in seconds)
        shift: Shift time for output (in seconds, default=0)

    Outputs:
        y: Output with pulse value (True during pulse width, False otherwise)
    """

    def __init__(self, time_manager: TimeManager, width: float = 0.5, period: float = 1.0, shift: float = 0.0):
        """Initialize Pulse block

        Args:
            time_manager: Time manager for getting current time
            width: Width of pulse in fraction of period (0 < width <= 1)
            period: Time for one period (seconds, must be > 0)
            shift: Shift time for output (seconds)
        """
        super().__init__(time_manager)

        if not (0 < width <= 1):
            raise ValueError(f"width must be in (0, 1], got {width}")
        if period <= 0:
            raise ValueError(f"period must be > 0, got {period}")

        self.width = width
        self.period = period
        self.shift = shift

    def compute(self) -> Dict[str, Any]:
        """Compute pulse output

        Returns:
            Dictionary with 'y': True if within pulse width, False otherwise
        """
        current_time = self.get_time()

        # Adjust time by shift
        adjusted_time = current_time - self.shift

        # Handle negative adjusted time (before first pulse starts)
        if adjusted_time < 0:
            return {'y': False}

        # Calculate position within current period
        # Using modulo to get time within period
        time_in_period = adjusted_time % self.period

        # Pulse is high for first (width * period) seconds of each period
        pulse_high_duration = self.width * self.period
        is_high = time_in_period < pulse_high_duration

        return {'y': is_high}
