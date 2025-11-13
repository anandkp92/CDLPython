# ABOUTME: MovingAverage - Compute moving average over time window
from typing import Any, Dict
from collections import deque
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class MovingAverage(CDLBlock):
    """Compute moving average over a time window

    Calculates the average of the input signal over the last 'delta' seconds.
    Uses a sliding window approach with discrete samples.

    Note: This is a discrete approximation of the continuous moving average.
    The window contains samples taken at each compute() call.

    Used for:
    - Noise filtering
    - Trend smoothing
    - Load averaging
    - Removing high-frequency fluctuations
    """

    def __init__(self, time_manager: TimeManager, delta: float):
        """Initialize MovingAverage block

        Args:
            time_manager: Time manager for time tracking
            delta: Time window for averaging (seconds, must be > 0)
        """
        super().__init__(time_manager)
        if delta <= 0:
            raise ValueError("delta must be positive")
        self.delta = delta

        # State: store (time, value) pairs in window
        self._window = deque()

    def compute(self, u: float) -> Dict[str, Any]:
        """Compute moving average

        Args:
            u: Input signal

        Returns:
            Dictionary with 'y': moving average over last delta seconds
        """
        current_time = self.get_time()

        # Add current sample to window
        self._window.append((current_time, u))

        # Remove samples outside the time window
        cutoff_time = current_time - self.delta
        while self._window and self._window[0][0] < cutoff_time:
            self._window.popleft()

        # Compute average
        if len(self._window) > 0:
            total = sum(value for _, value in self._window)
            y = total / len(self._window)
        else:
            y = u  # Fallback if window is empty

        return {'y': y}
