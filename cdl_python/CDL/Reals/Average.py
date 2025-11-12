# ABOUTME: Average block - outputs average of two real inputs.
# ABOUTME: Implements y = (u1 + u2) / 2 for CDL real-valued averaging.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class Average(CDLBlock):
    """
    Output the average of two inputs.

    Outputs y = (u1 + u2) / 2

    Inputs:
        u1: First input for average function
        u2: Second input for average function

    Outputs:
        y: Average of the two inputs
    """

    def compute(self, u1: float, u2: float) -> Dict[str, Any]:
        """
        Compute average of two inputs.

        Args:
            u1: First input value
            u2: Second input value

        Returns:
            Dictionary with output 'y' = (u1 + u2) / 2
        """
        return {'y': 0.5 * (u1 + u2)}
