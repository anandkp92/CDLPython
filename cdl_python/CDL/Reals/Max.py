# ABOUTME: Max block - outputs maximum of two real inputs.
# ABOUTME: Implements y = max(u1, u2) for CDL real-valued maximum.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class Max(CDLBlock):
    """
    Pass through the largest signal.

    Outputs y = max(u1, u2)

    Inputs:
        u1: First input to the max function
        u2: Second input to the max function

    Outputs:
        y: Maximum of the inputs
    """

    def compute(self, u1: float, u2: float) -> Dict[str, Any]:
        """
        Compute maximum of two inputs.

        Args:
            u1: First input value
            u2: Second input value

        Returns:
            Dictionary with output 'y' = max(u1, u2)
        """
        return {'y': max(u1, u2)}
