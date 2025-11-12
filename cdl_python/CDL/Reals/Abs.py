# ABOUTME: Abs block - outputs absolute value of real input.
# ABOUTME: Implements y = abs(u) for CDL real-valued absolute value.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class Abs(CDLBlock):
    """
    Output the absolute value of the input.

    Outputs y = abs(u)

    Inputs:
        u: Input for absolute function

    Outputs:
        y: Absolute value of the input
    """

    def compute(self, u: float) -> Dict[str, Any]:
        """
        Compute absolute value of input.

        Args:
            u: Input value

        Returns:
            Dictionary with output 'y' = abs(u)
        """
        return {'y': abs(u)}
