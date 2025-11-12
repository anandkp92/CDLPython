# ABOUTME: Multiply block - outputs product of two integer inputs.
# ABOUTME: Implements y = u1 * u2 for CDL integer multiplication.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class Multiply(CDLBlock):
    """
    Output the product of two integer inputs.

    Outputs y = u1 * u2

    Inputs:
        u1: First integer input
        u2: Second integer input

    Outputs:
        y: Product of the inputs
    """

    def compute(self, u1: int, u2: int) -> Dict[str, Any]:
        """
        Compute product of two integer inputs.

        Args:
            u1: First integer value
            u2: Second integer value

        Returns:
            Dictionary with output 'y' = u1 * u2
        """
        return {'y': u1 * u2}
