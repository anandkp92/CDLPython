# ABOUTME: PID block - PID controller with anti-windup compensation.
# ABOUTME: Implements standard PID control y = P + I + D with configurable controller type and limits.

from typing import Dict, Any, Optional
from enum import Enum
from cdl_python.base import CDLBlock
from cdl_python.time_manager import TimeManager


class SimpleController(Enum):
    """Controller type enumeration"""
    P = "P"
    PI = "PI"
    PD = "PD"
    PID = "PID"


class PID(CDLBlock):
    """
    P, PI, PD, and PID controller.

    Implements standard form:
        y_u = k/r * (e(t) + 1/Ti * integral(e(t)) + Td * de/dt)

    where e(t) = u_s(t) - u_m(t) is control error.

    Parameters:
        controllerType: Type of controller (P, PI, PD, or PID) (default: PI)
        k: Gain of controller (default: 1.0)
        Ti: Time constant of integrator block in seconds (default: 0.5)
        Td: Time constant of derivative block in seconds (default: 0.1)
        r: Typical range of control error for scaling (default: 1.0)
        yMax: Upper limit of output (default: 1.0)
        yMin: Lower limit of output (default: 0.0)
        Ni: Ni*Ti is time constant of anti-windup (default: 0.9)
        Nd: The higher Nd, the more ideal the derivative block (default: 10.0)
        xi_start: Initial value of integrator state (default: 0.0)
        yd_start: Initial value of derivative output (default: 0.0)
        reverseActing: True for reverse acting, False for direct acting (default: True)

    Inputs:
        u_s: Setpoint input signal
        u_m: Measurement input signal

    Outputs:
        y: Actuator output signal

    State:
        Maintains integrator state, derivative state, and last computation time
    """

    def __init__(
        self,
        time_manager: Optional[TimeManager] = None,
        controllerType: SimpleController = SimpleController.PI,
        k: float = 1.0,
        Ti: float = 0.5,
        Td: float = 0.1,
        r: float = 1.0,
        yMax: float = 1.0,
        yMin: float = 0.0,
        Ni: float = 0.9,
        Nd: float = 10.0,
        xi_start: float = 0.0,
        yd_start: float = 0.0,
        reverseActing: bool = True
    ):
        """
        Initialize PID controller.

        Args:
            time_manager: TimeManager instance (required)
            controllerType: Type of controller
            k: Controller gain
            Ti: Integral time constant
            Td: Derivative time constant
            r: Typical range of control error
            yMax: Upper output limit
            yMin: Lower output limit
            Ni: Anti-windup time constant factor
            Nd: Derivative filter factor
            xi_start: Initial integrator value
            yd_start: Initial derivative output
            reverseActing: Reverse or direct acting

        Raises:
            ValueError: If yMin >= yMax
        """
        super().__init__(time_manager)
        if yMin >= yMax:
            raise ValueError(f"yMin ({yMin}) must be less than yMax ({yMax})")

        self.controllerType = controllerType
        self.k = k
        self.Ti = Ti
        self.Td = Td
        self.r = r
        self.yMax = yMax
        self.yMin = yMin
        self.Ni = Ni
        self.Nd = Nd
        self.xi_start = xi_start
        self.yd_start = yd_start
        self.reverseActing = reverseActing

        # Determine which terms to use
        self.with_I = controllerType in [SimpleController.PI, SimpleController.PID]
        self.with_D = controllerType in [SimpleController.PD, SimpleController.PID]

        # Initialize state
        self._state = {
            'integral': xi_start,
            'last_error': 0.0,
            'derivative_filtered': yd_start,
            'last_time': None
        }

    def compute(self, u_s: float, u_m: float) -> Dict[str, Any]:
        """
        Compute PID controller output.

        Args:
            u_s: Setpoint
            u_m: Measurement

        Returns:
            Dictionary with output 'y' (controller output)
        """
        current_time = self.get_time()

        # Compute error with reverse/direct acting
        sign = 1.0 if self.reverseActing else -1.0
        error = sign * (u_s - u_m) / self.r

        # First call - initialize
        if self._state['last_time'] is None:
            self._state['last_time'] = current_time
            self._state['last_error'] = error
            # P term only on first call
            P = self.k * error
            y = max(self.yMin, min(self.yMax, P))
            return {'y': y}

        # Compute time step
        dt = current_time - self._state['last_time']

        # P term
        P = self.k * error

        # I term
        I = 0.0
        if self.with_I and dt > 0:
            self._state['integral'] += error * dt
            I = self.k / self.Ti * self._state['integral']

        # D term (simplified first-order filter)
        D = 0.0
        if self.with_D and dt > 0:
            # Simplified derivative with filter
            derivative = (error - self._state['last_error']) / dt
            # First-order filter: dy/dt = (derivative - y_filtered) * Nd / Td
            alpha = dt * self.Nd / self.Td
            self._state['derivative_filtered'] += alpha * (derivative - self._state['derivative_filtered'])
            D = self.k * self.Td * self._state['derivative_filtered']

        # Compute unlimited output
        y_unlim = P + I + D

        # Apply limits
        y = max(self.yMin, min(self.yMax, y_unlim))

        # Anti-windup: back-calculate integral if saturated
        if self.with_I and y != y_unlim and dt > 0:
            # Back-calculate integral
            delta_y = y_unlim - y
            self._state['integral'] -= delta_y / (self.k * self.Ni) * dt

        # Update state
        self._state['last_error'] = error
        self._state['last_time'] = current_time

        return {'y': y}

    def reset_state(self):
        """Reset controller to initial conditions"""
        self._state = {
            'integral': self.xi_start,
            'last_error': 0.0,
            'derivative_filtered': self.yd_start,
            'last_time': None
        }
