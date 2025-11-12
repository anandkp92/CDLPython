# ABOUTME: Stage sequencer block
# ABOUTME: Outputs number of stages to enable based on input signal with hysteresis
from typing import Any, Dict, Optional
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class Stage(CDLBlock):
    """
    Stage sequencer block

    Outputs the number of stages to enable based on input signal.
    Uses hysteresis and hold time to prevent rapid switching.

    Parameters:
        n: Number of stages (minimum: 1)
        holdDuration: Minimum time output must be held constant (seconds)
        h: Hysteresis for threshold comparison (default: 0.02/n)
        pre_y_start: Initial value of output (default: 0)

    Inputs:
        u: Real input between 0 and 1

    Outputs:
        y: Number of stages to enable (1 to n)
    """

    def __init__(
        self,
        time_manager: Optional[TimeManager] = None,
        n: int = 1,
        holdDuration: float = 0.0,
        h: float = None,
        pre_y_start: int = 0
    ):
        """
        Initialize Stage block.

        Args:
            time_manager: TimeManager instance
            n: Number of stages
            holdDuration: Hold duration in seconds
            h: Hysteresis value (default: 0.02/n)
            pre_y_start: Initial output value
        """
        super().__init__(time_manager)
        self.n = n
        self.holdDuration = holdDuration
        self.h = h if h is not None else 0.02 / n
        self.pre_y_start = pre_y_start

        # Calculate stage thresholds
        self.staThr = [(i - 1) / n for i in range(1, n + 1)]

        # Initialize state
        self._y = pre_y_start
        self._t_next = self.get_time() + holdDuration
        self._upper_threshold = 0.0
        self._lower_threshold = 0.0
        self._prev_check_upper = False
        self._prev_check_lower = True

    def compute(self, u: float) -> Dict[str, Any]:
        """
        Compute stage output based on input signal.

        Args:
            u: Input signal (0 to 1)

        Returns:
            Dictionary with key 'y' containing stage number
        """
        current_time = self.get_time()

        # Calculate check conditions with hysteresis
        check_upper = (
            (not self._prev_check_upper and u > (self._upper_threshold + self.h)) or
            (self._prev_check_upper and u >= (self._upper_threshold - self.h))
        )
        check_lower = (
            (not self._prev_check_lower and u > (self._lower_threshold + self.h)) or
            (self._prev_check_lower and u >= (self._lower_threshold - self.h))
        )

        # Update output if hold time has passed and conditions met
        if current_time >= self._t_next and (check_upper or not check_lower):
            self._t_next = current_time + self.holdDuration

            # Determine stage based on input
            if u >= self.staThr[self.n - 1]:
                self._y = self.n
            else:
                # Find which stage threshold the input falls into
                self._y = 0
                for i in range(1, self.n):
                    if u >= self.staThr[i - 1] and u < self.staThr[i]:
                        self._y = i - 1
                        break

            # Update thresholds
            if self._y == self.n:
                self._upper_threshold = self.staThr[self.n - 1]
            else:
                self._upper_threshold = self.staThr[self._y + 1] if self._y < self.n - 1 else self.staThr[self.n - 1]

            if self._y > 0:
                self._lower_threshold = self.staThr[min(self._y, self.n - 1)]

        # Update state
        self._prev_check_upper = check_upper
        self._prev_check_lower = check_lower

        return {'y': self._y}

    def reset_state(self):
        """Reset the block state"""
        self._y = self.pre_y_start
        self._t_next = self.get_time() + self.holdDuration
        self._upper_threshold = 0.0
        self._lower_threshold = 0.0
        self._prev_check_upper = False
        self._prev_check_lower = True
