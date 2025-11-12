# ABOUTME: NAND logical operator block
# ABOUTME: Outputs true if at least one input is false
from typing import Any, Dict
from cdl_python.base import CDLBlock


class Nand(CDLBlock):
    """
    Logical NAND block: y = not (u1 and u2)

    Outputs true if at least one input is false, otherwise false.

    Inputs:
        u1: First boolean input
        u2: Second boolean input

    Outputs:
        y: Result of NOT (u1 AND u2)
    """

    def compute(self, u1: bool, u2: bool) -> Dict[str, Any]:
        """
        Compute NAND of two boolean inputs.

        Args:
            u1: First boolean input
            u2: Second boolean input

        Returns:
            Dictionary with key 'y' containing the NAND result
        """
        y = not (u1 and u2)
        return {'y': y}
