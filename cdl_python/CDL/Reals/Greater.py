# ABOUTME: Greater block - compares two real inputs with optional hysteresis.
# ABOUTME: Implements y = u1 > u2 with optional hysteresis for CDL real comparison.

from typing import Dict, Any, Optional
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class Greater(CDLBlock):
    """
    Output y is true if input u1 is greater than input u2 with hysteresis.

    For h = 0: y = u1 > u2
    For h > 0: output switches to true if u1 > u2, and switches to false if u1 <= u2 - h

    Parameters:
        h: Hysteresis (default: 0, must be >= 0)
        pre_y_start: Initial value of output (default: False)

    Inputs:
        u1: First input
        u2: Second input

    Outputs:
        y: True if u1 is greater than u2 with hysteresis

    State:
        For h > 0, maintains previous output to implement hysteresis
    """

    def __init__(
        self,
        h: float = 0.0,
        pre_y_start: bool = False,
        time_manager: Optional[TimeManager] = None
    ):
        """
        Initialize Greater.

        Args:
            h: Hysteresis parameter (must be >= 0)
            pre_y_start: Initial value of output
            time_manager: TimeManager instance (optional)

        Raises:
            ValueError: If h < 0
        """
        super().__init__(time_manager)
        if h < 0:
            raise ValueError(f"Hysteresis h must be >= 0, got {h}")
        self.h = h
        self.pre_y_start = pre_y_start

        # Initialize state for hysteresis
        self._state = {
            'y': pre_y_start
        }

    def compute(self, u1: float, u2: float) -> Dict[str, Any]:
        """
        Compute comparison with hysteresis.

        Args:
            u1: First input value
            u2: Second input value

        Returns:
            Dictionary with output 'y' (boolean)
        """
        if self.h < 1e-10:
            # No hysteresis
            y = u1 > u2
        else:
            # With hysteresis
            prev_y = self._state['y']
            if not prev_y and u1 > u2:
                y = True
            elif prev_y and u1 > u2 - self.h:
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
