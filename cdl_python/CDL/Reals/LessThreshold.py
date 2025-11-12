# ABOUTME: LessThreshold block - compares real input against threshold with optional hysteresis.
# ABOUTME: Implements y = u < threshold with optional hysteresis for CDL threshold comparison.

from typing import Dict, Any, Optional
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class LessThreshold(CDLBlock):
    """
    Output y is true if input u is less than threshold with hysteresis.

    For h = 0: y = u < threshold
    For h > 0: output switches to true if u < threshold, and switches to false if u >= threshold + h

    Parameters:
        threshold: Threshold value for comparison
        h: Hysteresis (default: 0, must be >= 0)
        pre_y_start: Initial value of output (default: False)

    Inputs:
        u: Input signal

    Outputs:
        y: True if u is less than threshold with hysteresis

    State:
        For h > 0, maintains previous output to implement hysteresis
    """

    def __init__(
        self,
        threshold: float,
        h: float = 0.0,
        pre_y_start: bool = False,
        time_manager: Optional[TimeManager] = None
    ):
        """
        Initialize LessThreshold.

        Args:
            threshold: Threshold value
            h: Hysteresis parameter (must be >= 0)
            pre_y_start: Initial value of output
            time_manager: TimeManager instance (optional)

        Raises:
            ValueError: If h < 0
        """
        super().__init__(time_manager)
        if h < 0:
            raise ValueError(f"Hysteresis h must be >= 0, got {h}")
        self.threshold = threshold
        self.h = h
        self.pre_y_start = pre_y_start

        # Initialize state for hysteresis
        self._state = {
            'y': pre_y_start
        }

    def compute(self, u: float) -> Dict[str, Any]:
        """
        Compute threshold comparison with hysteresis.

        Args:
            u: Input value

        Returns:
            Dictionary with output 'y' (boolean)
        """
        if self.h < 1e-10:
            # No hysteresis
            y = u < self.threshold
        else:
            # With hysteresis
            prev_y = self._state['y']
            if not prev_y and u < self.threshold:
                y = True
            elif prev_y and u < self.threshold + self.h:
                y = True
            else:
                y = False

            self._state['y'] = y

        return {'y': y}

    def reset_state(self):
        """Reset state to initial conditions"""
        self._state = {
            'y': self.pre_y_start
        }
