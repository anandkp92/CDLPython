# ABOUTME: Less than threshold comparison for integers
# ABOUTME: Outputs true if input < threshold
from typing import Any, Dict
from cdl_python.base import CDLBlock


class LessThreshold(CDLBlock):
    """
    Less than threshold: y = (u < t)

    Compares input against a threshold parameter.

    Parameters:
        t: Threshold value (default: 0)

    Inputs:
        u: Integer input

    Outputs:
        y: True if u < t, false otherwise
    """

    def __init__(self, t: int = 0, **kwargs):
        """
        Initialize LessThreshold block.

        Args:
            t: Threshold value
        """
        super().__init__(**kwargs)
        self.t = t

    def compute(self, u: int) -> Dict[str, Any]:
        """
        Compare input against threshold for less than.

        Args:
            u: Integer input

        Returns:
            Dictionary with key 'y' containing comparison result
        """
        return {'y': u < self.t}
