# ABOUTME: Sin - Generate sine signal
# ABOUTME: Time-based sine wave generator with configurable parameters
import math
from typing import Any, Dict, Optional
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class Sin(CDLBlock):
    """
    Generate sine signal

    Parameters:
        amplitude: Amplitude of sine wave (default: 1.0)
        freqHz: Frequency of sine wave in Hz (default: 1.0)
        phase: Phase of sine wave in radians (default: 0.0)
        offset: Offset of output signal (default: 0.0)
        startTime: Output = offset for time < startTime (default: 0.0)

    Outputs:
        y: Sine output signal = offset + amplitude * sin(2*pi*freqHz*(time-startTime) + phase)
    """

    def __init__(
        self,
        time_manager: Optional[TimeManager] = None,
        amplitude: float = 1.0,
        freqHz: float = 1.0,
        phase: float = 0.0,
        offset: float = 0.0,
        startTime: float = 0.0
    ):
        """
        Initialize Sin source.

        Args:
            time_manager: TimeManager instance
            amplitude: Amplitude of sine wave
            freqHz: Frequency in Hz
            phase: Phase in radians
            offset: Output offset
            startTime: Start time for sine wave
        """
        super().__init__(time_manager)
        self.amplitude = amplitude
        self.freqHz = freqHz
        self.phase = phase
        self.offset = offset
        self.startTime = startTime

    def compute(self) -> Dict[str, Any]:
        """
        Compute sine output at current time.

        Returns:
            Dictionary with 'y' containing sine wave value
        """
        current_time = self.get_time()

        if current_time < self.startTime:
            # Before start time, output just the offset
            y = self.offset
        else:
            # Compute sine wave: offset + amplitude * sin(2*pi*freq*(t-t0) + phase)
            time_since_start = current_time - self.startTime
            y = self.offset + self.amplitude * math.sin(
                2.0 * math.pi * self.freqHz * time_since_start + self.phase
            )

        return {'y': y}
