"""
Real-valued ramp source block.

Generates a ramp signal that increases linearly from offset to offset+height.
"""

from typing import Dict, Any
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class Ramp(CDLBlock):
    """Generate ramp signal

    The output y is a ramp signal that starts at 'offset', then increases linearly
    to 'offset + height' over 'duration' seconds starting at 'startTime'.
    After the ramp completes, output remains at 'offset + height'.

    Parameters:
        height: Height of ramp (default=1.0)
        duration: Duration of ramp in seconds (must be > 0, default=1.0)
        offset: Offset of output signal (default=0.0)
        startTime: Output = offset for time < startTime (seconds, default=0.0)

    Outputs:
        y: Ramp output signal
    """

    def __init__(self, time_manager: TimeManager, height: float = 1.0, duration: float = 1.0,
                 offset: float = 0.0, startTime: float = 0.0):
        """Initialize Ramp block

        Args:
            time_manager: Time manager for getting current time
            height: Height of ramp
            duration: Duration of ramp (seconds, must be > 0)
            offset: Offset of output signal
            startTime: Start time of ramp (seconds)
        """
        super().__init__(time_manager)

        if duration <= 0:
            raise ValueError(f"duration must be > 0, got {duration}")

        self.height = height
        self.duration = duration
        self.offset = offset
        self.startTime = startTime

    def compute(self) -> Dict[str, Any]:
        """Compute ramp output

        Returns:
            Dictionary with 'y': ramp value
        """
        current_time = self.get_time()

        if current_time < self.startTime:
            # Before ramp starts
            y = self.offset
        elif current_time < (self.startTime + self.duration):
            # During ramp
            elapsed = current_time - self.startTime
            y = self.offset + (elapsed * self.height / self.duration)
        else:
            # After ramp completes
            y = self.offset + self.height

        return {'y': y}
