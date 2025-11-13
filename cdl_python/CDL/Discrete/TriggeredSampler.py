# ABOUTME: TriggeredSampler - Sample on boolean trigger
from typing import Any, Dict
from cdl_python.base import CDLBlock


class TriggeredSampler(CDLBlock):
    """Sample input when trigger goes from false to true

    Samples and holds the input value when the trigger input has a rising edge
    (changes from false to true). The output holds the sampled value until the
    next trigger.

    Used for:
    - Event-driven sampling
    - Capturing values at specific events
    - Sample-and-hold circuits
    - Synchronizing signals to events
    """

    def __init__(self, y_start: float = 0.0):
        """Initialize TriggeredSampler block

        Args:
            y_start: Initial output value (before first trigger)
        """
        super().__init__()
        self.y_start = y_start
        self._sampled_value = y_start
        self._previous_trigger = False

    def compute(self, u: float, trigger: bool) -> Dict[str, Any]:
        """Compute triggered sample output

        Args:
            u: Input value to sample
            trigger: Trigger signal (sample on rising edge)

        Returns:
            Dictionary with 'y': sampled value (updates on rising edge of trigger)
        """
        # Detect rising edge: trigger is True and was previously False
        rising_edge = trigger and not self._previous_trigger

        # Sample on rising edge
        if rising_edge:
            self._sampled_value = u

        # Update trigger history
        self._previous_trigger = trigger

        return {'y': self._sampled_value}
