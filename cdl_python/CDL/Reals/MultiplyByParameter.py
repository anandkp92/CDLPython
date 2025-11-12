# ABOUTME: MultiplyByParameter block - multiplies real input by parameter (gain).
# ABOUTME: Implements y = k * u for CDL real-valued multiplication with parameter.

from typing import Dict, Any
from cdl_python.base import CDLBlock


class MultiplyByParameter(CDLBlock):
    """
    Output the product of a gain value with the input signal.

    Outputs y = k * u where k is a parameter.

    Parameters:
        k: Factor to be multiplied with input signal

    Inputs:
        u: Input to be multiplied with gain

    Outputs:
        y: Product of the parameter times the input
    """

    def __init__(self, k: float, **kwargs):
        """
        Initialize MultiplyByParameter.

        Args:
            k: Gain parameter
            **kwargs: Additional arguments for CDLBlock
        """
        super().__init__(**kwargs)
        self.k = k

    def compute(self, u: float) -> Dict[str, Any]:
        """
        Compute product of input and gain parameter.

        Args:
            u: Input value

        Returns:
            Dictionary with output 'y' = k * u
        """
        return {'y': self.k * u}
