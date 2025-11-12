# ABOUTME: Add parameter block for integers
# ABOUTME: Outputs sum of input and a constant parameter
from typing import Any, Dict
from cdl_python.base import CDLBlock


class AddParameter(CDLBlock):
    """
    Add parameter block: y = u + p

    Adds a constant parameter to the input.

    Parameters:
        p: Parameter to be added to the input

    Inputs:
        u: Integer input

    Outputs:
        y: Sum of u and p
    """

    def __init__(self, p: int = 0, **kwargs):
        """
        Initialize AddParameter block.

        Args:
            p: Parameter to add to input
        """
        super().__init__(**kwargs)
        self.p = p

    def compute(self, u: int) -> Dict[str, Any]:
        """
        Add parameter to input.

        Args:
            u: Integer input

        Returns:
            Dictionary with key 'y' containing u + p
        """
        return {'y': u + self.p}
