# ABOUTME: Hysteresis block - transforms real to boolean with hysteresis
# ABOUTME: Implements hysteresis logic to prevent rapid switching near thresholds
from typing import Any, Dict
from cdl_python.base import CDLBlock


class Hysteresis(CDLBlock):
    """
    Hysteresis block

    Transforms real input to boolean output with hysteresis.
    - When output is false and input becomes greater than uHigh, switch to true
    - When output is true and input becomes less than uLow, switch to false

    Parameters:
        uLow: Lower threshold (if y=true and u<uLow, switch to y=false)
        uHigh: Upper threshold (if y=false and u>uHigh, switch to y=true)
        pre_y_start: Initial value of output (default: False)

    Inputs:
        u: Real input to compare against thresholds

    Outputs:
        y: Boolean output with hysteresis
    """

    def __init__(self, uLow: float, uHigh: float, pre_y_start: bool = False, **kwargs):
        """
        Initialize Hysteresis block.

        Args:
            uLow: Lower threshold
            uHigh: Upper threshold
            pre_y_start: Initial output value
        """
        super().__init__(**kwargs)
        if uHigh <= uLow:
            raise ValueError("uHigh must be larger than uLow")

        self.uLow = uLow
        self.uHigh = uHigh
        self._y = pre_y_start

    def compute(self, u: float) -> Dict[str, Any]:
        """
        Compute hysteresis output.

        Args:
            u: Real input

        Returns:
            Dictionary with key 'y' containing boolean output
        """
        # Hysteresis logic:
        # y = (not pre(y) and u > uHigh) or (pre(y) and u >= uLow)
        self._y = (not self._y and u > self.uHigh) or (self._y and u >= self.uLow)
        return {'y': self._y}

    def reset_state(self, pre_y_start: bool = False):
        """Reset the block state"""
        self._y = pre_y_start
