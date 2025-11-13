"""
Integer constant source block.

Outputs a constant integer signal.
"""

from typing import Dict, Any


class Constant:
    """Output constant signal of type Integer

    Block that outputs a constant signal y = k, where k is an Integer-valued parameter.

    Parameters:
        k: Constant output value (Integer)

    Outputs:
        y: Output with constant value
    """

    def __init__(self, k: int = 0):
        """Initialize Constant block

        Args:
            k: Constant output value
        """
        self.k = k

    def compute(self) -> Dict[str, Any]:
        """Compute output

        Returns:
            Dictionary with output 'y' = k
        """
        return {'y': self.k}
