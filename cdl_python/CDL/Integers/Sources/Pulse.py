"""
Integer pulse source block.

Generates periodic integer pulse signals.
"""

from typing import Dict, Any
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager
from cdl_python.CDL.Logical.Sources.Pulse import Pulse as BooleanPulse


class Pulse(CDLBlock):
    """Generate pulse signal of type Integer

    Block that outputs an integer pulse signal. Internally uses a boolean pulse
    and converts it to integer values.

    When pulse is high: y = offset + amplitude
    When pulse is low: y = offset

    Parameters:
        amplitude: Amplitude of pulse (default=1)
        width: Width of pulse in fraction of period (0 < width <= 1, default=0.5)
        period: Time for one period (in seconds)
        shift: Shift time for output (in seconds, default=0)
        offset: Offset of output signals (default=0)

    Outputs:
        y: Output connector with pulse value
    """

    def __init__(self, time_manager: TimeManager, amplitude: int = 1, width: float = 0.5,
                 period: float = 1.0, shift: float = 0.0, offset: int = 0):
        """Initialize Pulse block

        Args:
            time_manager: Time manager for getting current time
            amplitude: Amplitude of pulse
            width: Width of pulse in fraction of period (0 < width <= 1)
            period: Time for one period (seconds, must be > 0)
            shift: Shift time for output (seconds)
            offset: Offset of output signals
        """
        super().__init__(time_manager)

        self.amplitude = amplitude
        self.width = width
        self.period = period
        self.shift = shift
        self.offset = offset

        # Create internal boolean pulse
        self._bool_pulse = BooleanPulse(
            time_manager=time_manager,
            width=width,
            period=period,
            shift=shift
        )

    def compute(self) -> Dict[str, Any]:
        """Compute pulse output

        Returns:
            Dictionary with 'y': integer pulse value
        """
        # Get boolean pulse
        bool_output = self._bool_pulse.compute()

        # Convert to integer: True -> offset + amplitude, False -> offset
        if bool_output['y']:
            y = self.offset + self.amplitude
        else:
            y = self.offset

        return {'y': y}
