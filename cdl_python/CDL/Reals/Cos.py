# ABOUTME: Cos block - outputs cosine of real input in radians.
# ABOUTME: Implements y = cos(u) for CDL real-valued cosine function.

import math
from typing import Dict, Any
from cdl_python.base import CDLBlock


class Cos(CDLBlock):
    """
    Output the cosine of the input.

    Outputs y = cos(u) where u is in radians.

    Inputs:
        u: Input for the cosine function (in radians)

    Outputs:
        y: Cosine of input
    """

    def compute(self, u: float) -> Dict[str, Any]:
        """
        Compute cosine of input.

        Args:
            u: Input value in radians

        Returns:
            Dictionary with output 'y' = cos(u)
        """
        return {'y': math.cos(u)}
