# ABOUTME: ZeroOrderHold - Zero-order hold (staircase output)
from typing import Any, Dict, Optional
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class ZeroOrderHold(CDLBlock):
    """Zero-order hold - samples input and holds value constant

    Samples the input signal at regular intervals (samplePeriod) starting at
    startTime, and holds the sampled value constant until the next sample.
    Creates a staircase output signal.

    Used for:
    - Converting continuous signals to discrete
    - Interfacing with digital controllers
    - Creating piecewise-constant signals
    """

    def __init__(self, time_manager: TimeManager, samplePeriod: float, startTime: float = 0.0):
        """Initialize ZeroOrderHold block

        Args:
            time_manager: Time manager for sampling logic
            samplePeriod: Time between samples (must be > 0)
            startTime: Time of first sample
        """
        super().__init__(time_manager)
        if samplePeriod <= 0:
            raise ValueError("samplePeriod must be positive")
        self.samplePeriod = samplePeriod
        self.startTime = startTime
        self._held_value: Optional[float] = None
        self._next_sample_time = startTime

    def compute(self, u: float) -> Dict[str, Any]:
        """Compute zero-order hold output

        Args:
            u: Current input value

        Returns:
            Dictionary with 'y': held value (sampled at discrete times)
        """
        current_time = self.get_time()

        # Check if we should sample
        if current_time >= self._next_sample_time:
            # Sample the input
            self._held_value = u
            # Schedule next sample
            while self._next_sample_time <= current_time:
                self._next_sample_time += self.samplePeriod

        # Output the held value (or input if no sample yet)
        if self._held_value is None:
            y = u  # Before first sample, pass through
        else:
            y = self._held_value

        return {'y': y}
