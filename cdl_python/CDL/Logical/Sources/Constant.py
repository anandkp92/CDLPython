"""
Boolean constant source block.

Outputs a constant boolean signal.
"""

from typing import Dict, Any


class Constant:
    """Output constant signal of type Boolean

    Block that outputs a constant signal y = k, where k is a Boolean-valued parameter.

    Parameters:
        k: Constant output value (Boolean)

    Outputs:
        y: Output with constant value
    """

    def __init__(self, k: bool = False):
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
