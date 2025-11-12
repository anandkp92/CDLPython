# ABOUTME: Divide block - outputs quotient of two real inputs.
# ABOUTME: Implements y = u1 / u2 for CDL real-valued division.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class Divide(CDLBlock):
    """
    Output first input divided by second input.

    Outputs y = u1 / u2

    Inputs:
        u1: Input for dividend
        u2: Input for divisor

    Outputs:
        y: Quotient of the inputs

    Raises:
        ZeroDivisionError: If u2 is zero
    """

    def compute(self, u1: float, u2: float) -> Dict[str, Any]:
        """
        Compute quotient of two inputs.

        Args:
            u1: Dividend value
            u2: Divisor value

        Returns:
            Dictionary with output 'y' = u1 / u2

        Raises:
            ZeroDivisionError: If u2 is zero
        """
        if u2 == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return {'y': u1 / u2}
