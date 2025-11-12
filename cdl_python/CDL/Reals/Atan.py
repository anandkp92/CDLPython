# ABOUTME: Atan block - outputs arctangent of real input.
# ABOUTME: Implements y = atan(u) for CDL real-valued arctangent function.

import math
from typing import Dict, Any
from cdl_python.base import CDLBlock


class Atan(CDLBlock):
    """
    Output the arctangent of the input.

    Outputs y = atan(u) where result is in radians.

    Inputs:
        u: Input for the arctangent function

    Outputs:
        y: Arctangent of input in radians
    """

    def compute(self, u: float) -> Dict[str, Any]:
        """
        Compute arctangent of input.

        Args:
            u: Input value

        Returns:
            Dictionary with output 'y' = atan(u) in radians
        """
        return {'y': math.atan(u)}
