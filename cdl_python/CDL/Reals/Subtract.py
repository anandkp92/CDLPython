# ABOUTME: Subtract block - outputs difference of two real inputs.
# ABOUTME: Implements y = u1 - u2 for CDL real-valued subtraction.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class Subtract(CDLBlock):
    """
    Output the difference of two inputs.

    Outputs y = u1 - u2

    Inputs:
        u1: Input with minuend
        u2: Input with subtrahend

    Outputs:
        y: Difference of the inputs
    """

    def compute(self, u1: float, u2: float) -> Dict[str, Any]:
        """
        Compute difference of two inputs.

        Args:
            u1: Minuend value
            u2: Subtrahend value

        Returns:
            Dictionary with output 'y' = u1 - u2
        """
        return {'y': u1 - u2}
