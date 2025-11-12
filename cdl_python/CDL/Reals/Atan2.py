# ABOUTME: Atan2 block - outputs four-quadrant arctangent of two inputs.
# ABOUTME: Implements y = atan2(u1, u2) for CDL real-valued two-argument arctangent.

import math
from typing import Dict, Any
from cdl_python.base import CDLBlock


class Atan2(CDLBlock):
    """
    Output atan(u1/u2) in the correct quadrant.

    Outputs y = atan2(u1, u2) where result is in radians.

    Inputs:
        u1: First input (y-coordinate)
        u2: Second input (x-coordinate)

    Outputs:
        y: Four-quadrant arctangent in radians
    """

    def compute(self, u1: float, u2: float) -> Dict[str, Any]:
        """
        Compute two-argument arctangent.

        Args:
            u1: y-coordinate
            u2: x-coordinate

        Returns:
            Dictionary with output 'y' = atan2(u1, u2) in radians
        """
        return {'y': math.atan2(u1, u2)}
