# ABOUTME: Exp block - outputs exponential of real input.
# ABOUTME: Implements y = exp(u) for CDL real-valued exponential function.

import math
from typing import Dict, Any
from cdl_python.base import CDLBlock


class Exp(CDLBlock):
    """
    Output the exponential (base e) of the input.

    Outputs y = exp(u) = e^u

    Inputs:
        u: Input for the exponential function

    Outputs:
        y: Exponential of input
    """

    def compute(self, u: float) -> Dict[str, Any]:
        """
        Compute exponential of input.

        Args:
            u: Input value

        Returns:
            Dictionary with output 'y' = exp(u)
        """
        return {'y': math.exp(u)}
