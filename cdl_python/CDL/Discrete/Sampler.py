# ABOUTME: Sampler - Sample continuous signal at fixed intervals
from typing import Any, Dict
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class Sampler(CDLBlock):
    """Ideal sampling of continuous signal

    Samples the input signal at regular intervals (samplePeriod) starting at
    startTime. Between sample times, the output holds the last sampled value.

    Difference from ZeroOrderHold: Sampler is the idealized mathematical
    sampler, while ZeroOrderHold explicitly models the hold behavior.
    In practice, they behave identically.
    """

    def __init__(self, time_manager: TimeManager, samplePeriod: float, startTime: float = 0.0):
        """Initialize Sampler block

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
        self._sampled_value: float = 0.0
        self._next_sample_time = startTime
        self._initialized = False

    def compute(self, u: float) -> Dict[str, Any]:
        """Compute sampled output

        Args:
            u: Current input value

        Returns:
            Dictionary with 'y': sampled value
        """
        current_time = self.get_time()

        # Check if we should sample
        if current_time >= self._next_sample_time or not self._initialized:
            # Sample the input
            self._sampled_value = u
            self._initialized = True
            # Schedule next sample
            if current_time >= self._next_sample_time:
                while self._next_sample_time <= current_time:
                    self._next_sample_time += self.samplePeriod

        return {'y': self._sampled_value}
