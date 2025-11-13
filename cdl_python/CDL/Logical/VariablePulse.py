# ABOUTME: VariablePulse - Generate pulse with variable width
from typing import Any, Dict
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class VariablePulse(CDLBlock):
    """Generate boolean pulse with variable width

    Generates a pulse that starts at 'period' and has a width determined by
    the input 'u'. The pulse repeats with the specified period.

    When the pulse starts, the width is sampled from input 'u' (in seconds).
    The output stays true for that duration, then goes false until the next period.

    Used for:
    - Variable duty cycle PWM
    - Timed control signals
    - Periodic events with variable duration
    """

    def __init__(self, time_manager: TimeManager, period: float):
        """Initialize VariablePulse block

        Args:
            time_manager: Time manager for timing
            period: Time between pulse starts (must be > 0)
        """
        super().__init__(time_manager)
        if period <= 0:
            raise ValueError("period must be positive")
        self.period = period

        # State variables
        self._pulse_active = False
        self._pulse_end_time = 0.0
        self._next_pulse_time = period
        self._sampled_width = 0.0

    def compute(self, u: float) -> Dict[str, Any]:
        """Compute pulse output

        Args:
            u: Desired pulse width in seconds (sampled at pulse start)

        Returns:
            Dictionary with 'y': True during pulse, False otherwise
        """
        current_time = self.get_time()

        # Check if pulse should end
        if self._pulse_active and current_time >= self._pulse_end_time:
            self._pulse_active = False

        # Check if new pulse should start
        if current_time >= self._next_pulse_time:
            # Sample the width
            self._sampled_width = max(0.0, min(u, self.period))  # Clamp to [0, period]

            # Start pulse
            self._pulse_active = True
            self._pulse_end_time = current_time + self._sampled_width

            # Schedule next pulse
            while self._next_pulse_time <= current_time:
                self._next_pulse_time += self.period

        return {'y': self._pulse_active}
