# ABOUTME: TriggeredMovingMean - Moving average between triggers
from typing import Any, Dict
from cdl_python.base import CDLBlock


class TriggeredMovingMean(CDLBlock):
    """Compute moving average of values between triggers

    Accumulates and averages all input values between trigger events. When
    trigger has a rising edge, the accumulated values are reset and a new
    average computation begins.

    The output shows the running average of all values seen since the last
    trigger (or since initialization).

    Used for:
    - Computing average temperature/load over a period
    - Smoothing noisy measurements
    - Period-based statistics
    - Energy consumption averaging
    """

    def __init__(self):
        """Initialize TriggeredMovingMean block"""
        super().__init__()
        self._sum: float = 0.0
        self._count: int = 0
        self._previous_trigger = False

    def compute(self, u: float, trigger: bool) -> Dict[str, Any]:
        """Compute moving average since last trigger

        Args:
            u: Input value to include in average
            trigger: Reset signal (reset accumulation on rising edge)

        Returns:
            Dictionary with 'y': average value since last trigger
        """
        # Detect rising edge: trigger is True and was previously False
        rising_edge = trigger and not self._previous_trigger

        # Reset on rising edge
        if rising_edge:
            self._sum = u
            self._count = 1
        else:
            # Accumulate
            self._sum += u
            self._count += 1

        # Compute average
        if self._count > 0:
            y = self._sum / self._count
        else:
            y = 0.0  # Shouldn't happen, but handle gracefully

        # Update trigger history
        self._previous_trigger = trigger

        return {'y': y}
