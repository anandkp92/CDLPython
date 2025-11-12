# ABOUTME: Min block - outputs minimum of two integer inputs.
# ABOUTME: Implements y = min(u1, u2) for CDL integer minimum.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class Min(CDLBlock):
    """
    Output the minimum of two integer inputs.

    Outputs y = min(u1, u2)

    Inputs:
        u1: First integer input
        u2: Second integer input

    Outputs:
        y: Minimum of the inputs
    """

    def compute(self, u1: int, u2: int) -> Dict[str, Any]:
        """
        Compute minimum of two integer inputs.

        Args:
            u1: First integer value
            u2: Second integer value

        Returns:
            Dictionary with output 'y' = min(u1, u2)
        """
        return {'y': min(u1, u2)}
