Quick Start Guide
=================

This guide will help you get started with CDL Python quickly.

Basic Concepts
--------------

CDL Python implements the Control Description Language (CDL) in Python, providing:

1. **Time Management**: Simulation and real-time execution modes
2. **Elementary Blocks**: Pre-built control blocks (math, logic, sources, etc.)
3. **Type Safety**: Separate packages for Real, Integer, and Logical signals
4. **CXF Translation**: Convert CXF files to executable Python code

Your First CDL Block
--------------------

Here's a simple example using a constant source:

.. code-block:: python

    from cdl_python.CDL.Reals.Sources import Constant

    # Create a constant block
    const = Constant(k=5.0)

    # Compute output
    result = const.compute()
    print(result['y'])  # Output: 5.0

Using Time-Dependent Blocks
----------------------------

Many blocks depend on simulation time:

.. code-block:: python

    from cdl_python.time_manager import TimeManager, ExecutionMode
    from cdl_python.CDL.Reals.Sources import Sin
    import math

    # Create time manager in simulation mode
    tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)

    # Create a sine wave source
    sin_block = Sin(
        time_manager=tm,
        amplitude=1.0,
        freqHz=1.0,
        phase=0.0,
        offset=0.0
    )

    # Compute at different times
    for i in range(10):
        result = sin_block.compute()
        print(f"t={tm.get_time():.1f}, y={result['y']:.3f}")
        tm.advance(0.25)

Building a Simple Controller
-----------------------------

Combine multiple blocks to create a proportional controller:

.. code-block:: python

    from cdl_python.time_manager import TimeManager, ExecutionMode
    from cdl_python.CDL.Reals.Math import Add, Gain
    from cdl_python.CDL.Reals.Sources import Constant

    # Create time manager
    tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)

    # Setpoint
    setpoint = Constant(k=20.0)

    # Sensor reading (simulated)
    sensor = Constant(k=18.0)

    # Calculate error (setpoint - sensor)
    # Note: Subtract is implemented as Add with negative value
    error = Add()

    # Proportional gain
    controller = Gain(k=2.0)

    # Compute control signal
    sp_value = setpoint.compute()
    sens_value = sensor.compute()

    # Calculate error
    error_result = error.compute(
        u1=sp_value['y'],
        u2=-sens_value['y']  # Negative for subtraction
    )

    # Apply gain
    output = controller.compute(u=error_result['y'])

    print(f"Setpoint: {sp_value['y']}")
    print(f"Sensor: {sens_value['y']}")
    print(f"Error: {error_result['y']}")
    print(f"Control output: {output['y']}")

Using Pulse Generators
-----------------------

Generate periodic pulse signals:

.. code-block:: python

    from cdl_python.time_manager import TimeManager, ExecutionMode
    from cdl_python.CDL.Logical.Sources import Pulse

    tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)

    # Create pulse with 50% duty cycle, 1 second period
    pulse = Pulse(
        time_manager=tm,
        width=0.5,
        period=1.0,
        shift=0.0
    )

    # Sample over 2 periods
    for i in range(20):
        result = pulse.compute()
        print(f"t={tm.get_time():.1f}s: {result['y']}")
        tm.advance(0.1)

Using Time Tables
-----------------

Time tables provide scheduled value changes:

.. code-block:: python

    from cdl_python.time_manager import TimeManager, ExecutionMode
    from cdl_python.CDL.Reals.Sources import TimeTable, Smoothness, Extrapolation

    tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.5)

    # Define schedule: [time, value]
    schedule = [
        [0.0, 15.0],   # 15°C at midnight
        [6.0, 18.0],   # 18°C at 6am
        [18.0, 22.0],  # 22°C at 6pm
        [22.0, 18.0],  # 18°C at 10pm
        [24.0, 15.0],  # Back to 15°C
    ]

    # Create time table with linear interpolation
    schedule_block = TimeTable(
        time_manager=tm,
        table=schedule,
        smoothness=Smoothness.LINEAR_SEGMENTS,
        extrapolation=Extrapolation.PERIODIC
    )

    # Sample throughout the day
    for hour in range(0, 25):
        result = schedule_block.compute()
        print(f"Hour {hour}: {result['y']:.1f}°C")
        tm.advance(3600)  # Advance 1 hour

Translating CXF to Python
--------------------------

Convert CXF (CDL Exchange Format) files to Python code:

.. code-block:: python

    from cdl_translator.parser import CXFParser
    from cdl_translator.translator import PythonTranslator

    # Parse CXF file
    parser = CXFParser()
    model = parser.parse_file('examples/controller.json')

    print(f"Model: {model.model_name}")
    print(f"Blocks: {len(model.instances)}")
    print(f"Connections: {len(model.connections)}")

    # Translate to Python
    translator = PythonTranslator()
    python_code = translator.translate(model)

    # Save generated code
    with open('generated_controller.py', 'w') as f:
        f.write(python_code)

Or use the command-line tool:

.. code-block:: bash

    python -m cdl_translator.cli controller.json -o controller.py

Next Steps
----------

* Explore the :doc:`api/index` for detailed API documentation
* Check out :doc:`examples/index` for more complex examples
* Read about individual block types in the API reference
