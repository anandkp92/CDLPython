# ABOUTME: Constant - Output constant signal
# ABOUTME: Simple source block that outputs a constant value
from typing import Any, Dict, Optional
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class Constant(CDLBlock):
    """
    Output constant signal of type Real

    Parameters:
        k: Constant output value

    Outputs:
        y: Constant output signal (always equals k)
    """

    def __init__(self, time_manager: Optional[TimeManager] = None, k: float = 0.0):
        """
        Initialize Constant source.

        Args:
            time_manager: TimeManager instance (optional for constant blocks)
            k: Constant output value
        """
        super().__init__(time_manager)
        self.k = k

    def compute(self) -> Dict[str, Any]:
        """
        Compute constant output.

        Returns:
            Dictionary with 'y' containing the constant value k
        """
        return {'y': self.k}
