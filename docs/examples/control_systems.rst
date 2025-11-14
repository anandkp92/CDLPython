Control System Examples
=======================

This page demonstrates building complete control systems using CDL Python.

Proportional Controller
-----------------------

.. code-block:: python

    from cdl_python.time_manager import TimeManager, ExecutionMode
    from cdl_python.CDL.Reals.Math import Add, Gain, MultiplyByParameter
    from cdl_python.CDL.Reals.Sources import Constant

    # Create time manager
    tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)

    # Components
    setpoint = Constant(k=22.0)  # 22°C setpoint
    sensor = Constant(k=20.0)    # Current temperature

    # Calculate error
    error_calc = Add()

    # P controller with gain = 5.0
    controller = Gain(k=5.0)

    # Compute
    sp = setpoint.compute()
    temp = sensor.compute()

    # Error = setpoint - measurement
    error = error_calc.compute(u1=sp['y'], u2=-temp['y'])

    # Control output
    output = controller.compute(u=error['y'])

    print(f"Setpoint: {sp['y']}°C")
    print(f"Temperature: {temp['y']}°C")
    print(f"Error: {error['y']}°C")
    print(f"Control output: {output['y']}")

PID Controller Example
-----------------------

.. code-block:: python

    from cdl_python.time_manager import TimeManager, ExecutionMode
    from cdl_python.CDL.Reals.PIDController import PID

    tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)

    # PID controller
    pid = PID(
        time_manager=tm,
        k=2.0,      # Proportional gain
        Ti=10.0,    # Integral time
        Td=1.0,     # Derivative time
        yMax=100.0, # Max output
        yMin=0.0    # Min output
    )

    setpoint = 22.0
    measured = 18.0

    # Simulate control loop
    for i in range(100):
        # Compute control output
        result = pid.compute(
            u_s=setpoint,
            u_m=measured
        )

        print(f"t={tm.get_time():.1f}s: output={result['y']:.2f}")

        # Simulate process (simplified)
        measured += (result['y'] - measured) * 0.01

        tm.advance(0.1)

On/Off Controller with Hysteresis
----------------------------------

.. code-block:: python

    from cdl_python.CDL.Logical import OnOffController

    # Hysteresis controller
    controller = OnOffController(
        bandwidth=2.0  # ±1°C around setpoint
    )

    setpoint = 20.0
    temps = [18.0, 19.5, 20.5, 21.5, 20.5, 19.0, 18.5]

    for temp in temps:
        result = controller.compute(
            reference=setpoint,
            u=temp
        )
        state = "ON" if result['y'] else "OFF"
        print(f"Temp: {temp}°C, Heater: {state}")

Limiter with Proportional Controller
-------------------------------------

.. code-block:: python

    from cdl_python.CDL.Reals.Math import Gain
    from cdl_python.CDL.Reals.Limiter import Limit

    # Proportional controller
    gain = Gain(k=10.0)

    # Output limiter (0-100%)
    limiter = Limit(uMin=0.0, uMax=100.0)

    # Large error
    error = 15.0

    # Calculate control signal
    control = gain.compute(u=error)
    print(f"Unlimited output: {control['y']}")  # 150.0

    # Apply limits
    limited = limiter.compute(u=control['y'])
    print(f"Limited output: {limited['y']}")    # 100.0
