# ABOUTME: Falling edge detection block
# ABOUTME: Outputs true when input transitions from true to false
from typing import Any, Dict, Optional
from cdl_python.base import CDLBlock


class FallingEdge(CDLBlock):
    """
    Falling edge detection block

    Outputs true when the input transitions from true to false.
    Otherwise outputs false.

    Parameters:
        pre_u_start: Initial value of previous input (default: False)

    Inputs:
        u: Boolean input to monitor

    Outputs:
        y: True on falling edge, false otherwise
    """

    def __init__(self, pre_u_start: bool = False, **kwargs):
        """
        Initialize FallingEdge block.

        Args:
            pre_u_start: Start value of pre(u) at initial time
        """
        super().__init__(**kwargs)
        self._pre_u = pre_u_start
        self._initialized = False

    def compute(self, u: bool) -> Dict[str, Any]:
        """
        Detect falling edge of boolean input.

        Args:
            u: Boolean input

        Returns:
            Dictionary with key 'y' containing edge detection result
        """
        # Falling edge is when previous value was true and current is false
        y = self._pre_u and not u

        # Update previous value
        self._pre_u = u

        return {'y': y}

    def reset_state(self, pre_u_start: bool = False):
        """Reset the block state"""
        self._pre_u = pre_u_start
        self._initialized = False
