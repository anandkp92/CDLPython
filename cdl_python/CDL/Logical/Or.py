# ABOUTME: Or block - logical OR of two boolean inputs.
# ABOUTME: Implements y = u1 or u2 for CDL boolean OR operation.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class Or(CDLBlock):
    """
    Logical 'or': y = u1 or u2

    Outputs true if at least one input is true.

    Inputs:
        u1: First input for logical 'or'
        u2: Second input for logical 'or'

    Outputs:
        y: True if at least one of the inputs is true
    """

    def compute(self, u1: bool, u2: bool) -> Dict[str, Any]:
        """
        Compute logical OR of two inputs.

        Args:
            u1: First boolean value
            u2: Second boolean value

        Returns:
            Dictionary with output 'y' = u1 or u2
        """
        return {'y': u1 or u2}
