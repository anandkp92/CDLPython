# ABOUTME: Change detection block for integers
# ABOUTME: Detects if integer input changes, increases, or decreases
from typing import Any, Dict
from cdl_python.base import CDLBlock


class Change(CDLBlock):
    """
    Change detection block for integers

    Outputs whether the input changes, increases, or decreases.

    Parameters:
        pre_u_start: Initial value of previous input (default: 0)

    Inputs:
        u: Integer input to monitor

    Outputs:
        y: True if input changed
        up: True if input increased
        down: True if input decreased
    """

    def __init__(self, pre_u_start: int = 0, **kwargs):
        """
        Initialize Change block.

        Args:
            pre_u_start: Start value of pre(u) at initial time
        """
        super().__init__(**kwargs)
        self._pre_u = pre_u_start

    def compute(self, u: int) -> Dict[str, Any]:
        """
        Detect changes in integer input.

        Args:
            u: Integer input

        Returns:
            Dictionary with keys 'y', 'up', 'down' containing detection results
        """
        # Detect change
        y = (u != self._pre_u)
        # Detect increase
        up = (u > self._pre_u)
        # Detect decrease
        down = (u < self._pre_u)

        # Update previous value
        self._pre_u = u

        return {'y': y, 'up': up, 'down': down}

    def reset_state(self, pre_u_start: int = 0):
        """Reset the block state"""
        self._pre_u = pre_u_start
