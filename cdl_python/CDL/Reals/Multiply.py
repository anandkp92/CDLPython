# ABOUTME: Multiply block - outputs product of two real inputs.
# ABOUTME: Implements y = u1 * u2 for CDL real-valued multiplication.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class Multiply(CDLBlock):
    """
    Output product of two inputs.

    Outputs y = u1 * u2

    Inputs:
        u1: First input to be multiplied
        u2: Second input to be multiplied

    Outputs:
        y: Product of the inputs
    """

    def compute(self, u1: float, u2: float) -> Dict[str, Any]:
        """
        Compute product of two inputs.

        Args:
            u1: First input value
            u2: Second input value

        Returns:
            Dictionary with output 'y' = u1 * u2
        """
        return {'y': u1 * u2}
