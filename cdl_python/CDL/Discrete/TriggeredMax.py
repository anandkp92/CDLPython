# ABOUTME: TriggeredMax - Track maximum value between triggers
from typing import Any, Dict
from cdl_python.base import CDLBlock


class TriggeredMax(CDLBlock):
    """Output maximum value since last trigger

    Tracks the maximum input value between trigger events. When trigger has a
    rising edge, the output is reset and starts tracking a new maximum.

    The output continuously updates to show the maximum value seen since the
    last trigger (or since initialization).

    Used for:
    - Peak detection
    - Finding maximum load/temperature in a period
    - Monitoring extreme values between resets
    - Quality control and alarm systems
    """

    def __init__(self):
        """Initialize TriggeredMax block"""
        super().__init__()
        self._max_value: float = float('-inf')  # Start with negative infinity
        self._previous_trigger = False
        self._first_call = True

    def compute(self, u: float, trigger: bool) -> Dict[str, Any]:
        """Compute maximum value since last trigger

        Args:
            u: Input value to track
            trigger: Reset signal (reset maximum on rising edge)

        Returns:
            Dictionary with 'y': maximum value since last trigger
        """
        # Detect rising edge: trigger is True and was previously False
        rising_edge = trigger and not self._previous_trigger

        # Reset on rising edge
        if rising_edge:
            self._max_value = u
            self._first_call = False
        else:
            # Update maximum
            if self._first_call:
                # First call: initialize with current input
                self._max_value = u
                self._first_call = False
            else:
                # Track maximum
                self._max_value = max(self._max_value, u)

        # Update trigger history
        self._previous_trigger = trigger

        return {'y': self._max_value}
