# ABOUTME: Subtract block - outputs difference of two integer inputs.
# ABOUTME: Implements y = u1 - u2 for CDL integer subtraction.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class Subtract(CDLBlock):
    """
    Output the difference of two integer inputs.

    Outputs y = u1 - u2

    Inputs:
        u1: Minuend
        u2: Subtrahend

    Outputs:
        y: Difference of the inputs
    """

    def compute(self, u1: int, u2: int) -> Dict[str, Any]:
        """
        Compute difference of two integer inputs.

        Args:
            u1: Minuend value
            u2: Subtrahend value

        Returns:
            Dictionary with output 'y' = u1 - u2
        """
        return {'y': u1 - u2}
