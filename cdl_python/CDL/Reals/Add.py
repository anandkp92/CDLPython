# ABOUTME: Add block - outputs sum of two real inputs.
# ABOUTME: Implements y = u1 + u2 for CDL real-valued addition.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class Add(CDLBlock):
    """
    Output the sum of two inputs.

    Outputs y = u1 + u2

    Inputs:
        u1: First input to be added
        u2: Second input to be added

    Outputs:
        y: Sum of the inputs
    """

    def compute(self, u1: float, u2: float) -> Dict[str, Any]:
        """
        Compute sum of two inputs.

        Args:
            u1: First input value
            u2: Second input value

        Returns:
            Dictionary with output 'y' = u1 + u2
        """
        return {'y': u1 + u2}
