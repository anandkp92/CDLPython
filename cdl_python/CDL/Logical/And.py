# ABOUTME: And block - logical AND of two boolean inputs.
# ABOUTME: Implements y = u1 and u2 for CDL boolean AND operation.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class And(CDLBlock):
    """
    Logical 'and': y = u1 and u2

    Outputs true if both inputs are true.

    Inputs:
        u1: First boolean input for logical 'and'
        u2: Second boolean input for logical 'and'

    Outputs:
        y: True if u1 and u2 are both true
    """

    def compute(self, u1: bool, u2: bool) -> Dict[str, Any]:
        """
        Compute logical AND of two inputs.

        Args:
            u1: First boolean value
            u2: Second boolean value

        Returns:
            Dictionary with output 'y' = u1 and u2
        """
        return {'y': u1 and u2}
