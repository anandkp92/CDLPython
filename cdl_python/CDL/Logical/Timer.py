# ABOUTME: Timer block - measures elapsed time when input is true
# ABOUTME: Outputs time elapsed since input became true, with threshold comparison
from typing import Any, Dict, Optional
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class Timer(CDLBlock):
    """
    Timer block

    Measures elapsed time while input is true.
    Outputs zero when input is false.
    Sets 'passed' output to true when elapsed time exceeds threshold.

    Parameters:
        t: Threshold time for comparison (seconds, default: 0)

    Inputs:
        u: Boolean input that activates timer

    Outputs:
        y: Elapsed time (seconds)
        passed: True if elapsed time > threshold
    """

    def __init__(
        self,
        time_manager: Optional[TimeManager] = None,
        t: float = 0.0
    ):
        """
        Initialize Timer block.

        Args:
            time_manager: TimeManager instance
            t: Threshold time (seconds)
        """
        super().__init__(time_manager)
        self.t = t
        self._entry_time = None
        self._passed = (t <= 0)

    def compute(self, u: bool) -> Dict[str, Any]:
        """
        Compute timer output.

        Args:
            u: Boolean input

        Returns:
            Dictionary with keys 'y' (elapsed time) and 'passed' (threshold exceeded)
        """
        current_time = self.get_time()

        if u:
            # Timer is running
            if self._entry_time is None:
                # Just became true
                self._entry_time = current_time
                self._passed = (self.t <= 0)

            # Calculate elapsed time
            elapsed = current_time - self._entry_time
            y = elapsed

            # Check if threshold passed
            if elapsed >= self.t:
                self._passed = True

        else:
            # Timer is off
            self._entry_time = None
            self._passed = False
            y = 0.0

        return {'y': y, 'passed': self._passed}

    def reset_state(self):
        """Reset the block state"""
        self._entry_time = None
        self._passed = (self.t <= 0)
