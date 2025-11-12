# ABOUTME: Round block - rounds real input to specified number of digits.
# ABOUTME: Implements rounding to n digits for CDL real-valued rounding.

import math
from typing import Dict, Any
from cdl_python.base import CDLBlock


class Round(CDLBlock):
    """
    Round real number to given digits.

    For n = 0: rounds to nearest integer
    For n = 1: rounds to next decimal point
    For n = -1: rounds to next multiple of ten

    Outputs:
        y = floor(u * 10^n + 0.5) / 10^n  for u > 0
        y = ceil(u * 10^n - 0.5) / 10^n   for u < 0

    Parameters:
        n: Number of digits to round to

    Inputs:
        u: Input to be rounded

    Outputs:
        y: Rounded value of input
    """

    def __init__(self, n: int, **kwargs):
        """
        Initialize Round.

        Args:
            n: Number of digits to round to
            **kwargs: Additional arguments for CDLBlock
        """
        super().__init__(**kwargs)
        self.n = n
        self.fac = 10 ** n

    def compute(self, u: float) -> Dict[str, Any]:
        """
        Compute rounded value.

        Args:
            u: Input value

        Returns:
            Dictionary with output 'y' = rounded value
        """
        if u > 0:
            y = math.floor(u * self.fac + 0.5) / self.fac
        else:
            y = math.ceil(u * self.fac - 0.5) / self.fac
        return {'y': y}
