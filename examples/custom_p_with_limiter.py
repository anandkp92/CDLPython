#!/usr/bin/env python3
"""
Custom P Controller with Limiter

Python implementation of CustomPWithLimiter.mo from:
https://github.com/lbl-srg/modelica-json/blob/master/test/FromModelica/CustomPWithLimiter.mo

This example demonstrates how to compose CDL blocks to create custom control logic.

Block Description:
    A proportional controller that outputs y = min(yMax, k*e), where:
    - e: control error (input)
    - k: constant gain (parameter)
    - yMax: maximum output value (input)
    - y: control signal (output)

CDL Blocks Used:
    - Buildings.Controls.OBC.CDL.Reals.MultiplyByParameter (gain)
    - Buildings.Controls.OBC.CDL.Reals.Min (minValue)

Original Modelica code translates to Python by instantiating CDL blocks
and connecting them through function calls.

Note: This example requires the cdl_python package to be installed.
      Install with: pip install -e .
"""

from cdl_python.CDL.Reals import MultiplyByParameter, Min


class CustomPWithLimiter:
    """
    Custom implementation of a P controller with variable output limiter.

    This is a Python translation of the CDL block CustomPWithLimiter.mo

    Parameters:
        k (float): Constant gain (default: 2.0)

    Inputs (via compute method):
        e (float): Control error
        yMax (float): Maximum value of output signal

    Outputs:
        y (float): Control signal = min(yMax, k * e)
    """

    def __init__(self, k=2.0):
        """
        Initialize the P controller with limiter.

        Args:
            k: Constant gain (default: 2.0)
        """
        self.k = k

        # Instantiate CDL blocks (matches Modelica model structure)
        self.gain = MultiplyByParameter(k=self.k)  # Multiply error by gain
        self.min_value = Min()  # Take minimum of two inputs

    def compute(self, e, yMax):
        """
        Compute the control output.

        Args:
            e: Control error
            yMax: Maximum value of output signal

        Returns:
            dict: {'y': control signal output}
        """
        # Connect blocks (matches Modelica connections)
        # e → gain.u
        gain_output = self.gain.compute(u=e)

        # yMax → minValue.u1, gain.y → minValue.u2
        min_output = self.min_value.compute(u1=yMax, u2=gain_output['y'])

        # minValue.y → y
        return {'y': min_output['y']}


def main():
    """Example usage of CustomPWithLimiter"""

    print("=" * 60)
    print("Custom P Controller with Limiter Example")
    print("=" * 60)
    print()

    # Create controller with gain k=2.0
    controller = CustomPWithLimiter(k=2.0)

    print(f"Controller parameters:")
    print(f"  Gain (k) = {controller.k}")
    print()

    # Test scenarios
    test_cases = [
        {"e": 1.0, "yMax": 5.0, "description": "Normal operation (within limit)"},
        {"e": 5.0, "yMax": 5.0, "description": "At limit (k*e = yMax)"},
        {"e": 10.0, "yMax": 5.0, "description": "Above limit (k*e > yMax)"},
        {"e": -2.0, "yMax": 5.0, "description": "Negative error"},
        {"e": 3.0, "yMax": 10.0, "description": "High limit"},
    ]

    print("Test Results:")
    print("-" * 60)
    print(f"{'Error (e)':<12} {'Max (yMax)':<12} {'Output (y)':<12} {'k*e':<12}")
    print("-" * 60)

    for test in test_cases:
        e = test["e"]
        yMax = test["yMax"]

        # Compute output
        result = controller.compute(e=e, yMax=yMax)
        y = result['y']

        # Calculate what k*e would be without limiter
        k_times_e = controller.k * e

        print(f"{e:<12.2f} {yMax:<12.2f} {y:<12.2f} {k_times_e:<12.2f} "
              f"{'← limited' if y < k_times_e else ''}")

    print("-" * 60)
    print()

    # Demonstrate time-series simulation
    print("Time-series simulation (setpoint tracking):")
    print("-" * 60)

    setpoint = 20.0  # Desired value
    yMax = 15.0      # Output limit

    print(f"Setpoint: {setpoint}")
    print(f"Output limit: {yMax}")
    print()
    print(f"{'Time':<8} {'Measured':<12} {'Error':<12} {'Output':<12}")
    print("-" * 60)

    # Simulate approaching setpoint
    measured_values = [0.0, 5.0, 10.0, 15.0, 18.0, 19.0, 19.5, 20.0]

    for t, measured in enumerate(measured_values):
        error = setpoint - measured  # Control error
        result = controller.compute(e=error, yMax=yMax)
        output = result['y']

        print(f"{t:<8} {measured:<12.1f} {error:<12.1f} {output:<12.2f}")

    print("-" * 60)
    print()
    print("✓ Example complete!")


if __name__ == "__main__":
    main()
