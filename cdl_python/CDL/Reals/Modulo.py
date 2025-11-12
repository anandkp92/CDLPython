# ABOUTME: Modulo block - computes remainder of division of two real inputs.
# ABOUTME: Implements y = u1 mod u2 for CDL real-valued modulo operation.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class Modulo(CDLBlock):
    """
    Output the remainder of first input divided by second input.

    Outputs y = u1 mod u2

    Inputs:
        u1: Dividend of the modulus function
        u2: Divisor of the modulus function (must not be zero)

    Outputs:
        y: Modulus u1 mod u2

    Raises:
        ZeroDivisionError: If u2 is zero
    """

    def compute(self, u1: float, u2: float) -> Dict[str, Any]:
        """
        Compute modulo operation.

        Args:
            u1: Dividend
            u2: Divisor (must not be zero)

        Returns:
            Dictionary with output 'y' = u1 mod u2

        Raises:
            ZeroDivisionError: If u2 is zero
        """
        if u2 == 0:
            raise ZeroDivisionError("Modulo divisor cannot be zero")
        return {'y': u1 % u2}
