# ABOUTME: Change detection block
# ABOUTME: Outputs true when input changes (either rising or falling edge)
from typing import Any, Dict
from cdl_python.base import CDLBlock


class Change(CDLBlock):
    """
    Change detection block

    Outputs true when the input has either a rising edge (false to true)
    or a falling edge (true to false). Otherwise outputs false.

    Parameters:
        pre_u_start: Initial value of previous input (default: False)

    Inputs:
        u: Boolean input to monitor

    Outputs:
        y: True on any change, false otherwise
    """

    def __init__(self, pre_u_start: bool = False, **kwargs):
        """
        Initialize Change block.

        Args:
            pre_u_start: Start value of pre(u) at initial time
        """
        super().__init__(**kwargs)
        self._pre_u = pre_u_start

    def compute(self, u: bool) -> Dict[str, Any]:
        """
        Detect any change in boolean input.

        Args:
            u: Boolean input

        Returns:
            Dictionary with key 'y' containing change detection result
        """
        # Change detected if current value differs from previous
        y = (u != self._pre_u)

        # Update previous value
        self._pre_u = u

        return {'y': y}

    def reset_state(self, pre_u_start: bool = False):
        """Reset the block state"""
        self._pre_u = pre_u_start
