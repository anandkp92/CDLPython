# ABOUTME: Add block - outputs sum of two integer inputs.
# ABOUTME: Implements y = u1 + u2 for CDL integer addition.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class Add(CDLBlock):
    """
    Output the sum of two integer inputs.

    Outputs y = u1 + u2

    Inputs:
        u1: First integer input
        u2: Second integer input

    Outputs:
        y: Sum of the inputs
    """

    def compute(self, u1: int, u2: int) -> Dict[str, Any]:
        """
        Compute sum of two integer inputs.

        Args:
            u1: First integer value
            u2: Second integer value

        Returns:
            Dictionary with output 'y' = u1 + u2
        """
        return {'y': u1 + u2}
