"""
Real-valued pulse source block.

Generates periodic real-valued pulse signals.
"""

from typing import Dict, Any
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class Pulse(CDLBlock):
    """Generate pulse signal of type Real

    Block that outputs a real-valued pulse signal with specified amplitude, width, period, and offset.

    When pulse is high: y = offset + amplitude
    When pulse is low: y = offset

    Parameters:
        amplitude: Amplitude of pulse (default=1.0)
        width: Width of pulse in fraction of period (0 < width <= 1, default=0.5)
        period: Time for one period (in seconds, default=1.0)
        shift: Shift time for output (in seconds, default=0.0)
        offset: Offset of output signal (default=0.0)

    Outputs:
        y: Output with pulse value
    """

    def __init__(self, time_manager: TimeManager, amplitude: float = 1.0, width: float = 0.5,
                 period: float = 1.0, shift: float = 0.0, offset: float = 0.0):
        """Initialize Pulse block

        Args:
            time_manager: Time manager for getting current time
            amplitude: Amplitude of pulse
            width: Width of pulse in fraction of period (0 < width <= 1)
            period: Time for one period (seconds, must be > 0)
            shift: Shift time for output (seconds)
            offset: Offset of output signal
        """
        super().__init__(time_manager)

        if not (0 < width <= 1):
            raise ValueError(f"width must be in (0, 1], got {width}")
        if period <= 0:
            raise ValueError(f"period must be > 0, got {period}")

        self.amplitude = amplitude
        self.width = width
        self.period = period
        self.shift = shift
        self.offset = offset

    def compute(self) -> Dict[str, Any]:
        """Compute pulse output

        Returns:
            Dictionary with 'y': pulse value (offset + amplitude or offset)
        """
        current_time = self.get_time()

        # Adjust time by shift
        adjusted_time = current_time - self.shift

        # Handle negative adjusted time (before first pulse starts)
        if adjusted_time < 0:
            return {'y': self.offset}

        # Calculate position within current period
        time_in_period = adjusted_time % self.period

        # Pulse is high for first (width * period) seconds of each period
        pulse_high_duration = self.width * self.period
        is_high = time_in_period < pulse_high_duration

        if is_high:
            return {'y': self.offset + self.amplitude}
        else:
            return {'y': self.offset}
