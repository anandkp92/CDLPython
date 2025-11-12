# ABOUTME: Counter block that increments on trigger
# ABOUTME: Counts number of times trigger input becomes true
from typing import Any, Dict
from cdl_python.base import CDLBlock


class OnCounter(CDLBlock):
    """
    Counter block

    Increments output whenever trigger input rises to true.
    Can be reset to initial value.

    Parameters:
        y_start: Initial and reset value (default: 0)

    Inputs:
        trigger: When true, increment counter
        reset: When true, reset counter to y_start

    Outputs:
        y: Counter value
    """

    def __init__(self, y_start: int = 0, **kwargs):
        """
        Initialize OnCounter block.

        Args:
            y_start: Initial and reset value
        """
        super().__init__(**kwargs)
        self.y_start = y_start
        self._y = y_start
        self._prev_trigger = False
        self._prev_reset = False

    def compute(self, trigger: bool, reset: bool) -> Dict[str, Any]:
        """
        Update counter based on trigger and reset inputs.

        Args:
            trigger: Trigger input
            reset: Reset input

        Returns:
            Dictionary with key 'y' containing counter value
        """
        # Detect rising edges
        trigger_rising = trigger and not self._prev_trigger
        reset_rising = reset and not self._prev_reset

        # Reset has priority
        if reset_rising or reset:
            self._y = self.y_start
        # Increment on trigger rising edge
        elif trigger_rising:
            self._y += 1

        # Update previous values
        self._prev_trigger = trigger
        self._prev_reset = reset

        return {'y': self._y}

    def reset_state(self):
        """Reset the block state"""
        self._y = self.y_start
        self._prev_trigger = False
        self._prev_reset = False
