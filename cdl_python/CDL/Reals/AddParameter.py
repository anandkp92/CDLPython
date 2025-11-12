# ABOUTME: AddParameter block - adds parameter to real input.
# ABOUTME: Implements y = u + p for CDL real-valued addition with parameter.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class AddParameter(CDLBlock):
    """
    Output the sum of an input plus a parameter.

    Outputs y = u + p where p is a parameter.

    Parameters:
        p: Parameter to be added to the input

    Inputs:
        u: Input to be added to the parameter

    Outputs:
        y: Sum of the parameter and the input
    """

    def __init__(self, p: float, **kwargs):
        """
        Initialize AddParameter.

        Args:
            p: Parameter value to add
            **kwargs: Additional arguments for CDLBlock
        """
        super().__init__(**kwargs)
        self.p = p

    def compute(self, u: float) -> Dict[str, Any]:
        """
        Compute sum of input and parameter.

        Args:
            u: Input value

        Returns:
            Dictionary with output 'y' = u + p
        """
        return {'y': u + self.p}
