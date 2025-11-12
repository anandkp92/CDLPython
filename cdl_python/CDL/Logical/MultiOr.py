# ABOUTME: Multi-input OR logical operator block
# ABOUTME: Outputs true if at least one input is true
from typing import Any, Dict, List
from cdl_python.base import CDLBlock


class MultiOr(CDLBlock):
    """
    Multi-input OR block: y = u[1] or u[2] or u[3] or ...

    Outputs true if at least one input element is true.
    If no inputs are provided, outputs false.

    Inputs:
        u: List of boolean inputs

    Outputs:
        y: True if at least one input is true, false otherwise
    """

    def compute(self, u: List[bool]) -> Dict[str, Any]:
        """
        Compute OR of all boolean inputs.

        Args:
            u: List of boolean inputs

        Returns:
            Dictionary with key 'y' containing the OR result
        """
        if len(u) == 0:
            return {'y': False}

        # At least one input must be true
        y = any(u)
        return {'y': y}
