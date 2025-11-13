# ABOUTME: LimitSlewRate - Limit rate of change of signal
from typing import Any, Dict
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class LimitSlewRate(CDLBlock):
    """Limit the rate of change of a signal

    Constrains how fast the output can change by limiting dy/dt.
    Output follows input but with rate limited by raisingSlewRate and
    fallingSlewRate parameters.

    This is useful for:
    - Ramping setpoints gradually
    - Preventing sudden changes
    - Protecting equipment from fast transients
    - Smooth transitions

    Implementation uses Euler integration:
    y(t+dt) = y(t) + rate_limited_derivative * dt
    """

    def __init__(
        self,
        time_manager: TimeManager,
        raisingSlewRate: float = float('inf'),
        fallingSlewRate: float = float('inf'),
        y_start: float = 0.0
    ):
        """Initialize LimitSlewRate block

        Args:
            time_manager: Time manager for timestep
            raisingSlewRate: Maximum rate of increase (units/second)
            fallingSlewRate: Maximum rate of decrease (units/second, positive value)
            y_start: Initial output value
        """
        super().__init__(time_manager)
        self.raisingSlewRate = raisingSlewRate
        self.fallingSlewRate = fallingSlewRate

        # State
        self._y = y_start
        self._previous_time = None

    def compute(self, u: float) -> Dict[str, Any]:
        """Compute rate-limited output

        Args:
            u: Input signal

        Returns:
            Dictionary with 'y': rate-limited output
        """
        current_time = self.get_time()

        # Always apply rate limiting (even on first call)
        if self._previous_time is not None:
            dt = current_time - self._previous_time
        else:
            # First call: assume some small timestep to start limiting
            dt = 0.001 if current_time == 0 else current_time

        if dt > 0:
            # Desired change
            delta = u - self._y

            # Limit the rate of change
            if delta > 0:
                # Rising: limit by raisingSlewRate
                max_delta = self.raisingSlewRate * dt
                delta = min(delta, max_delta)
            else:
                # Falling: limit by fallingSlewRate
                max_delta = -self.fallingSlewRate * dt
                delta = max(delta, max_delta)

            # Update output
            self._y += delta

        self._previous_time = current_time

        return {'y': self._y}
