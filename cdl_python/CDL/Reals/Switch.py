# ABOUTME: Switch block - selects between two real signals based on boolean condition.
# ABOUTME: Implements y = u1 if u2 else u3 for CDL real-valued conditional switching.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class Switch(CDLBlock):
    """
    Switch between two Real signals.

    If the input signal u2 is True, the block outputs y = u1.
    Otherwise, it outputs y = u3.

    Inputs:
        u1: First real input
        u2: Boolean switch input (if true, y=u1, else y=u3)
        u3: Second real input

    Outputs:
        y: Output with u1 if u2 is true, else u3
    """

    def compute(self, u1: float, u2: bool, u3: float) -> Dict[str, Any]:
        """
        Compute switch output based on boolean condition.

        Args:
            u1: First input value
            u2: Boolean selector
            u3: Second input value

        Returns:
            Dictionary with output 'y' = u1 if u2 else u3
        """
        return {'y': u1 if u2 else u3}
