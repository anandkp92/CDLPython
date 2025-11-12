# ABOUTME: Max block - outputs maximum of two integer inputs.
# ABOUTME: Implements y = max(u1, u2) for CDL integer maximum.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class Max(CDLBlock):
    """
    Output the maximum of two integer inputs.

    Outputs y = max(u1, u2)

    Inputs:
        u1: First integer input
        u2: Second integer input

    Outputs:
        y: Maximum of the inputs
    """

    def compute(self, u1: int, u2: int) -> Dict[str, Any]:
        """
        Compute maximum of two integer inputs.

        Args:
            u1: First integer value
            u2: Second integer value

        Returns:
            Dictionary with output 'y' = max(u1, u2)
        """
        return {'y': max(u1, u2)}
