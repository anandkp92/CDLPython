# ABOUTME: Min block - outputs minimum of two real inputs.
# ABOUTME: Implements y = min(u1, u2) for CDL real-valued minimum.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class Min(CDLBlock):
    """
    Pass through the smallest signal.

    Outputs y = min(u1, u2)

    Inputs:
        u1: First input to the min function
        u2: Second input to the min function

    Outputs:
        y: Minimum of the inputs
    """

    def compute(self, u1: float, u2: float) -> Dict[str, Any]:
        """
        Compute minimum of two inputs.

        Args:
            u1: First input value
            u2: Second input value

        Returns:
            Dictionary with output 'y' = min(u1, u2)
        """
        return {'y': min(u1, u2)}
