# ABOUTME: Boolean switch block for selecting between two boolean signals
# ABOUTME: Outputs u1 if u2 is true, otherwise outputs u3
from typing import Any, Dict
from cdl_python.base import CDLBlock


class Switch(CDLBlock):
    """
    Boolean switch block: y = u1 if u2 else u3

    Selects between two boolean inputs based on a control signal.

    Inputs:
        u1: First boolean input
        u2: Control signal (if true, output u1; if false, output u3)
        u3: Second boolean input

    Outputs:
        y: u1 if u2 is true, otherwise u3
    """

    def compute(self, u1: bool, u2: bool, u3: bool) -> Dict[str, Any]:
        """
        Switch between two boolean inputs based on control signal.

        Args:
            u1: First boolean input
            u2: Control signal
            u3: Second boolean input

        Returns:
            Dictionary with key 'y' containing the selected input
        """
        y = u1 if u2 else u3
        return {'y': y}
