# ABOUTME: Greater than or equal comparison for integers
# ABOUTME: Outputs true if u1 >= u2
from typing import Any, Dict
from cdl_python.base import CDLBlock


class GreaterEqual(CDLBlock):
    """
    Greater than or equal comparison: y = (u1 >= u2)

    Compares two integer inputs.

    Inputs:
        u1: First integer input
        u2: Second integer input

    Outputs:
        y: True if u1 >= u2, false otherwise
    """

    def compute(self, u1: int, u2: int) -> Dict[str, Any]:
        """
        Compare two integers for greater than or equal.

        Args:
            u1: First integer input
            u2: Second integer input

        Returns:
            Dictionary with key 'y' containing comparison result
        """
        return {'y': u1 >= u2}
