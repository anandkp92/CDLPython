# ABOUTME: TrueDelay block - delays rising edge but not falling edge
# ABOUTME: Delays true signal by specified time, passes false immediately
from typing import Any, Dict, Optional
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class TrueDelay(CDLBlock):
    """
    True delay block

    Delays a rising edge of the input by delayTime.
    Does not delay a falling edge (outputs false immediately).

    Parameters:
        delayTime: Delay time for rising edge (seconds)
        delayOnInit: If true, delay initial true input (default: False)

    Inputs:
        u: Boolean input to be delayed

    Outputs:
        y: Delayed boolean output
    """

    def __init__(
        self,
        time_manager: Optional[TimeManager] = None,
        delayTime: float = 0.0,
        delayOnInit: bool = False
    ):
        """
        Initialize TrueDelay block.

        Args:
            time_manager: TimeManager instance
            delayTime: Delay time (seconds)
            delayOnInit: Delay initial true input
        """
        super().__init__(time_manager)
        self.delayTime = delayTime
        self.delayOnInit = delayOnInit
        self._trigger_time = None
        self._y = False
        self._prev_u = False
        self._initialized = False

    def compute(self, u: bool) -> Dict[str, Any]:
        """
        Compute delayed output.

        Args:
            u: Boolean input

        Returns:
            Dictionary with key 'y' containing delayed output
        """
        current_time = self.get_time()

        # Detect rising edge
        u_rising = u and not self._prev_u

        if not u:
            # Input is false - output immediately false
            self._y = False
            self._trigger_time = None

        elif u_rising:
            # Rising edge detected
            if self.delayTime > 0:
                # Set trigger time for delayed output
                self._trigger_time = current_time + self.delayTime
                self._y = False
            else:
                # Zero delay - output immediately
                self._y = True
                self._trigger_time = None

        elif self._trigger_time is not None:
            # Waiting for delay to expire
            if current_time >= self._trigger_time:
                self._y = True
                self._trigger_time = None

        elif u:
            # Input is still true and delay has already passed
            self._y = True

        # Update previous value
        self._prev_u = u
        self._initialized = True

        return {'y': self._y}

    def reset_state(self):
        """Reset the block state"""
        self._trigger_time = None
        self._y = False
        self._prev_u = False
        self._initialized = False
