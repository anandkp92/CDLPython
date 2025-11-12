# ABOUTME: Not block - logical NOT of boolean input.
# ABOUTME: Implements y = not u for CDL boolean NOT operation.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class Not(CDLBlock):
    """
    Logical not

    Outputs true if input is false, and false if input is true.

    Inputs:
        u: Input to be negated

    Outputs:
        y: Negated input
    """

    def compute(self, u: bool) -> Dict[str, Any]:
        """
        Compute logical NOT of input.

        Args:
            u: Boolean value

        Returns:
            Dictionary with output 'y' = not u
        """
        return {'y': not u}
