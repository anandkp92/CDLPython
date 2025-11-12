# ABOUTME: Edge block - detects rising edge on boolean input.
# ABOUTME: Implements y = edge(u) for CDL boolean rising edge detection.

from typing import Dict, Any, Optional
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class Edge(CDLBlock):
    """
    Output y is true if the input u has a rising edge.

    Detects when input changes from false to true.

    Parameters:
        pre_u_start: Start value of previous u at initial time (default: False)

    Inputs:
        u: Input to be monitored

    Outputs:
        y: True when input switches from false to true

    State:
        Maintains previous input value to detect edges
    """

    def __init__(
        self,
        pre_u_start: bool = False,
        time_manager: Optional[TimeManager] = None
    ):
        """
        Initialize Edge.

        Args:
            pre_u_start: Initial value of previous input
            time_manager: TimeManager instance (optional)
        """
        super().__init__(time_manager)
        self.pre_u_start = pre_u_start

        # Initialize state
        self._state = {
            'prev_u': pre_u_start
        }

    def compute(self, u: bool) -> Dict[str, Any]:
        """
        Detect rising edge.

        Args:
            u: Current input value

        Returns:
            Dictionary with output 'y' (true if rising edge detected)
        """
        prev_u = self._state['prev_u']

        # Rising edge: prev was false, current is true
        y = (not prev_u) and u

        # Update state
        self._state['prev_u'] = u

        return {'y': y}

    def reset_state(self):
        """Reset state to initial conditions"""
        self._state = {
            'prev_u': self.pre_u_start
        }
