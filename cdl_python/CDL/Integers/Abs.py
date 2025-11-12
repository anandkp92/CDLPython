# ABOUTME: Abs block - outputs absolute value of integer input.
# ABOUTME: Implements y = abs(u) for CDL integer absolute value.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class Abs(CDLBlock):
    """
    Output the absolute value of an integer input.

    Outputs y = abs(u)

    Inputs:
        u: Integer input

    Outputs:
        y: Absolute value of the input
    """

    def compute(self, u: int) -> Dict[str, Any]:
        """
        Compute absolute value of integer input.

        Args:
            u: Integer value

        Returns:
            Dictionary with output 'y' = abs(u)
        """
        return {'y': abs(u)}
