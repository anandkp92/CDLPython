# ABOUTME: FirstOrderHold - First-order hold with linear interpolation
from typing import Any, Dict, Optional
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class FirstOrderHold(CDLBlock):
    """First-order hold - linear interpolation between samples

    Samples the input signal at regular intervals and performs linear
    interpolation between samples. This creates a smoother output than
    zero-order hold (staircase).

    The interpolation uses the slope between the last two samples to
    extrapolate forward until the next sample is taken.

    Used for:
    - Smoother reconstruction of sampled signals
    - Reducing high-frequency content compared to ZOH
    - Better approximation of continuous signals
    """

    def __init__(self, time_manager: TimeManager, samplePeriod: float, startTime: float = 0.0):
        """Initialize FirstOrderHold block

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

        # State variables
        self._current_sample: Optional[float] = None
        self._previous_sample: Optional[float] = None
        self._current_sample_time: float = startTime
        self._next_sample_time: float = startTime

    def compute(self, u: float) -> Dict[str, Any]:
        """Compute first-order hold output with linear interpolation

        Args:
            u: Current input value

        Returns:
            Dictionary with 'y': interpolated value
        """
        current_time = self.get_time()

        # Check if we should sample
        if current_time >= self._next_sample_time:
            # Store previous sample
            if self._current_sample is not None:
                self._previous_sample = self._current_sample

            # Take new sample
            self._current_sample = u
            self._current_sample_time = current_time

            # Schedule next sample
            while self._next_sample_time <= current_time:
                self._next_sample_time += self.samplePeriod

        # Compute output
        if self._current_sample is None:
            # Before first sample
            y = u
        elif self._previous_sample is None:
            # After first sample but before second - hold constant
            y = self._current_sample
        else:
            # Linear interpolation/extrapolation
            # Slope from previous to current sample
            slope = (self._current_sample - self._previous_sample) / self.samplePeriod

            # Time since current sample
            dt = current_time - self._current_sample_time

            # Linear extrapolation
            y = self._current_sample + slope * dt

        return {'y': y}
