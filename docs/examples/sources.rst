Source Block Examples
=====================

This page demonstrates the use of various source blocks in CDL Python.

Real-Valued Sources
-------------------

Constant Source
~~~~~~~~~~~~~~~

.. code-block:: python

    from cdl_python.CDL.Reals.Sources import Constant

    # Simple constant
    const = Constant(k=42.5)
    result = const.compute()
    print(result['y'])  # 42.5

Sine Wave Generator
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from cdl_python.time_manager import TimeManager, ExecutionMode
    from cdl_python.CDL.Reals.Sources import Sin
    import math

    tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.01)

    # 1 Hz sine wave with amplitude 2.0
    sine = Sin(
        time_manager=tm,
        amplitude=2.0,
        freqHz=1.0,
        phase=0.0,
        offset=0.0
    )

    # Sample one complete cycle
    for _ in range(100):
        result = sine.compute()
        print(f"{tm.get_time():.2f}, {result['y']:.3f}")
        tm.advance(0.01)

Pulse Generator
~~~~~~~~~~~~~~~

.. code-block:: python

    from cdl_python.time_manager import TimeManager, ExecutionMode
    from cdl_python.CDL.Reals.Sources import Pulse

    tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)

    # Square wave: 0-10V, 2 second period, 25% duty cycle
    pulse = Pulse(
        time_manager=tm,
        amplitude=10.0,
        width=0.25,
        period=2.0,
        shift=0.0,
        offset=0.0
    )

    for _ in range(40):
        result = pulse.compute()
        print(f"t={tm.get_time():.1f}s: {result['y']}V")
        tm.advance(0.1)

Ramp Generator
~~~~~~~~~~~~~~

.. code-block:: python

    from cdl_python.time_manager import TimeManager, ExecutionMode
    from cdl_python.CDL.Reals.Sources import Ramp

    tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)

    # Ramp from 0 to 100 over 10 seconds, starting at t=5s
    ramp = Ramp(
        time_manager=tm,
        height=100.0,
        duration=10.0,
        offset=0.0,
        startTime=5.0
    )

    # Before ramp (t < 5s): output = 0
    result = ramp.compute()
    print(f"t=0: {result['y']}")  # 0.0

    # During ramp (5s <= t < 15s): linear interpolation
    for _ in range(100):
        tm.advance(0.1)
        result = ramp.compute()
        if 4.9 <= tm.get_time() <= 15.1:
            print(f"t={tm.get_time():.1f}: {result['y']:.1f}")

Integer Sources
---------------

Integer Constant
~~~~~~~~~~~~~~~~

.. code-block:: python

    from cdl_python.CDL.Integers.Sources import Constant

    const = Constant(k=42)
    result = const.compute()
    print(result['y'])  # 42

Integer Pulse
~~~~~~~~~~~~~

.. code-block:: python

    from cdl_python.time_manager import TimeManager, ExecutionMode
    from cdl_python.CDL.Integers.Sources import Pulse

    tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)

    # Pulse between 0 and 5
    pulse = Pulse(
        time_manager=tm,
        amplitude=5,
        width=0.5,
        period=1.0,
        shift=0.0,
        offset=0
    )

    for _ in range(20):
        result = pulse.compute()
        print(f"t={tm.get_time():.1f}: {result['y']}")
        tm.advance(0.1)

Boolean Sources
---------------

Boolean Constant
~~~~~~~~~~~~~~~~

.. code-block:: python

    from cdl_python.CDL.Logical.Sources import Constant

    true_const = Constant(k=True)
    false_const = Constant(k=False)

    print(true_const.compute()['y'])   # True
    print(false_const.compute()['y'])  # False

Boolean Pulse
~~~~~~~~~~~~~

.. code-block:: python

    from cdl_python.time_manager import TimeManager, ExecutionMode
    from cdl_python.CDL.Logical.Sources import Pulse

    tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)

    # 1 Hz pulse, 30% duty cycle
    pulse = Pulse(
        time_manager=tm,
        width=0.3,
        period=1.0,
        shift=0.0
    )

    for _ in range(20):
        result = pulse.compute()
        state = "HIGH" if result['y'] else "LOW"
        print(f"t={tm.get_time():.1f}s: {state}")
        tm.advance(0.1)

Sample Trigger
~~~~~~~~~~~~~~

.. code-block:: python

    from cdl_python.time_manager import TimeManager, ExecutionMode
    from cdl_python.CDL.Logical.Sources import SampleTrigger

    tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.05)

    # Trigger every 1 second
    trigger = SampleTrigger(
        time_manager=tm,
        period=1.0,
        shift=0.0
    )

    # Edge-triggered: fires only once at sample time
    for _ in range(50):
        result = trigger.compute()
        if result['y']:
            print(f"TRIGGER at t={tm.get_time():.2f}s")
        tm.advance(0.05)

Calendar Time
-------------

.. code-block:: python

    from cdl_python.time_manager import TimeManager, ExecutionMode
    from cdl_python.CDL.Reals.Sources import CalendarTime, ZeroTime

    tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=3600)

    # Start at January 1, 2020
    calendar = CalendarTime(
        time_manager=tm,
        zerTim=ZeroTime.NY2020,
        offset=0.0
    )

    # Simulate first week
    for day in range(7):
        result = calendar.compute()
        print(f"Day {day+1}: {result['year']}/{result['month']}/{result['day']}, "
              f"Weekday: {result['weekDay']}")
        # Advance 24 hours
        for _ in range(24):
            tm.advance(3600)
