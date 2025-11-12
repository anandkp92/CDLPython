# ABOUTME: NOR logical operator block
# ABOUTME: Outputs true if both inputs are false
from typing import Any, Dict
from cdl_python.base import CDLBlock


class Nor(CDLBlock):
    """
    Logical NOR block: y = not (u1 or u2)

    Outputs true if both inputs are false, otherwise false.

    Inputs:
        u1: First boolean input
        u2: Second boolean input

    Outputs:
        y: Result of NOT (u1 OR u2)
    """

    def compute(self, u1: bool, u2: bool) -> Dict[str, Any]:
        """
        Compute NOR of two boolean inputs.

        Args:
            u1: First boolean input
            u2: Second boolean input

        Returns:
            Dictionary with key 'y' containing the NOR result
        """
        y = not (u1 or u2)
        return {'y': y}
