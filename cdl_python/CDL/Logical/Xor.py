# ABOUTME: XOR logical operator block
# ABOUTME: Outputs true if exactly one input is true
from typing import Any, Dict
from cdl_python.base import CDLBlock


class Xor(CDLBlock):
    """
    Logical XOR block: y = u1 xor u2

    Outputs true if exactly one input is true, otherwise false.

    Inputs:
        u1: First boolean input
        u2: Second boolean input

    Outputs:
        y: Result of u1 XOR u2
    """

    def compute(self, u1: bool, u2: bool) -> Dict[str, Any]:
        """
        Compute XOR of two boolean inputs.

        Args:
            u1: First boolean input
            u2: Second boolean input

        Returns:
            Dictionary with key 'y' containing the XOR result
        """
        # XOR is true if exactly one input is true
        # Equivalent to: not ((u1 and u2) or (not u1 and not u2))
        y = (u1 and not u2) or (not u1 and u2)
        return {'y': y}
