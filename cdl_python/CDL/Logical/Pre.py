# ABOUTME: Previous value (delay) block
# ABOUTME: Outputs the previous value of input with one-step delay
from typing import Any, Dict
from cdl_python.base import CDLBlock


class Pre(CDLBlock):
    """
    Previous value block: y = pre(u)

    Returns the value of the input from the previous compute call.
    This adds a one-step delay without advancing time.

    Parameters:
        pre_u_start: Initial value of previous input (default: False)

    Inputs:
        u: Boolean input

    Outputs:
        y: Previous value of u
    """

    def __init__(self, pre_u_start: bool = False, **kwargs):
        """
        Initialize Pre block.

        Args:
            pre_u_start: Start value of pre(u) at initial time
        """
        super().__init__(**kwargs)
        self._pre_u = pre_u_start

    def compute(self, u: bool) -> Dict[str, Any]:
        """
        Return previous value of input.

        Args:
            u: Boolean input

        Returns:
            Dictionary with key 'y' containing the previous value
        """
        # Output is the previous value
        y = self._pre_u

        # Update previous value for next call
        self._pre_u = u

        return {'y': y}

    def reset_state(self, pre_u_start: bool = False):
        """Reset the block state"""
        self._pre_u = pre_u_start
