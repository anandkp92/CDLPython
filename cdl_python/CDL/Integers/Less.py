# ABOUTME: Less block - compares two integer inputs.
# ABOUTME: Implements y = (u1 < u2) for CDL integer comparison.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class Less(CDLBlock):
    """
    Output true if first integer input is less than second.

    Outputs y = (u1 < u2)

    Inputs:
        u1: First integer input
        u2: Second integer input

    Outputs:
        y: True if u1 < u2
    """

    def compute(self, u1: int, u2: int) -> Dict[str, Any]:
        """
        Compare two integers.

        Args:
            u1: First integer value
            u2: Second integer value

        Returns:
            Dictionary with output 'y' = (u1 < u2)
        """
        return {'y': u1 < u2}
