# ABOUTME: Multi-input AND logical operator block
# ABOUTME: Outputs true if all inputs are true
from typing import Any, Dict, List
from cdl_python.base import CDLBlock


class MultiAnd(CDLBlock):
    """
    Multi-input AND block: y = u[1] and u[2] and u[3] and ...

    Outputs true if all input elements are true.
    If no inputs are provided, outputs false.

    Inputs:
        u: List of boolean inputs

    Outputs:
        y: True if all inputs are true, false otherwise
    """

    def compute(self, u: List[bool]) -> Dict[str, Any]:
        """
        Compute AND of all boolean inputs.

        Args:
            u: List of boolean inputs

        Returns:
            Dictionary with key 'y' containing the AND result
        """
        if len(u) == 0:
            return {'y': False}

        # All inputs must be true
        y = all(u)
        return {'y': y}
