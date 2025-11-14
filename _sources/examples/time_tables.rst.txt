Time Table Examples
===================

Time tables provide scheduled value changes based on simulation time.

Daily Temperature Schedule
--------------------------

.. code-block:: python

    from cdl_python.time_manager import TimeManager, ExecutionMode
    from cdl_python.CDL.Reals.Sources import TimeTable, Smoothness, Extrapolation

    tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=600)  # 10 min steps

    # Daily schedule (time in hours, temperature in °C)
    schedule = [
        [0.0, 16.0],   # Midnight: 16°C
        [6.0, 18.0],   # 6 AM: start warming
        [8.0, 21.0],   # 8 AM: occupied temperature
        [17.0, 21.0],  # 5 PM: maintain
        [19.0, 19.0],  # 7 PM: start cooling
        [22.0, 16.0],  # 10 PM: night setback
        [24.0, 16.0],  # End of day
    ]

    # Create time table with linear interpolation
    temp_schedule = TimeTable(
        time_manager=tm,
        table=schedule,
        timeScale=3600.0,  # Convert hours to seconds
        smoothness=Smoothness.LINEAR_SEGMENTS,
        extrapolation=Extrapolation.PERIODIC
    )

    # Simulate 48 hours
    for _ in range(288):  # 48 hours * 6 (10-min intervals per hour)
        result = temp_schedule.compute()
        hour = (tm.get_time() / 3600.0) % 24
        print(f"Hour {hour:5.1f}: {result['y']:.1f}°C")
        tm.advance(600)

Weekly Occupancy Schedule
--------------------------

.. code-block:: python

    from cdl_python.time_manager import TimeManager, ExecutionMode
    from cdl_python.CDL.Logical.Sources import TimeTable

    tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=3600)  # 1 hour steps

    # Weekly schedule (time in days, 1=occupied, 0=unoccupied)
    weekly_schedule = [
        [0.0, 0],    # Sunday midnight: unoccupied
        [1.0, 0],    # Monday midnight: still unoccupied
        [1.33, 1],   # Monday 8 AM: occupied
        [1.71, 0],   # Monday 5 PM: unoccupied
        [2.33, 1],   # Tuesday 8 AM: occupied
        [2.71, 0],   # Tuesday 5 PM: unoccupied
        [3.33, 1],   # Wednesday 8 AM: occupied
        [3.71, 0],   # Wednesday 5 PM: unoccupied
        [4.33, 1],   # Thursday 8 AM: occupied
        [4.71, 0],   # Thursday 5 PM: unoccupied
        [5.33, 1],   # Friday 8 AM: occupied
        [5.71, 0],   # Friday 5 PM: unoccupied
        [7.0, 0],    # Sunday midnight: end
    ]

    occupancy = TimeTable(
        time_manager=tm,
        table=weekly_schedule,
        timeScale=86400.0,  # Convert days to seconds
        period=604800.0      # 1 week in seconds
    )

    # Simulate one week
    for hour in range(168):  # 7 days * 24 hours
        result = occupancy.compute()
        day = hour // 24
        hour_of_day = hour % 24
        status = "OCCUPIED" if result['y'] else "VACANT"
        print(f"Day {day}, Hour {hour_of_day:02d}: {status}")
        tm.advance(3600)

Multi-Column Time Table
------------------------

.. code-block:: python

    from cdl_python.time_manager import TimeManager, ExecutionMode
    from cdl_python.CDL.Reals.Sources import TimeTable, Smoothness, Extrapolation

    tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=1.0)

    # Time table with multiple outputs
    # Column 1: Temperature, Column 2: Humidity
    schedule = [
        [0.0, 20.0, 50.0],
        [3600.0, 22.0, 55.0],
        [7200.0, 21.0, 52.0],
        [10800.0, 20.0, 50.0],
    ]

    multi_schedule = TimeTable(
        time_manager=tm,
        table=schedule,
        smoothness=Smoothness.LINEAR_SEGMENTS,
        extrapolation=Extrapolation.PERIODIC
    )

    # Sample every 15 minutes
    for _ in range(24):
        result = multi_schedule.compute()
        # For multi-column tables, y is a list
        temp = result['y'][0] if isinstance(result['y'], list) else result['y']
        humidity = result['y'][1] if isinstance(result['y'], list) and len(result['y']) > 1 else None

        time_min = tm.get_time() / 60.0
        print(f"t={time_min:5.0f} min: Temp={temp:.1f}°C, RH={humidity:.1f}%")
        tm.advance(900)  # 15 minutes

Constant Segments (Step Changes)
---------------------------------

.. code-block:: python

    from cdl_python.time_manager import TimeManager, ExecutionMode
    from cdl_python.CDL.Reals.Sources import TimeTable, Smoothness, Extrapolation

    tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.5)

    # Step changes in valve position
    valve_schedule = [
        [0.0, 0.0],    # Closed
        [5.0, 50.0],   # Half open
        [10.0, 100.0], # Full open
        [15.0, 0.0],   # Closed
    ]

    valve_position = TimeTable(
        time_manager=tm,
        table=valve_schedule,
        smoothness=Smoothness.CONSTANT_SEGMENTS,  # Step changes
        extrapolation=Extrapolation.HOLD_LAST_POINT
    )

    # Simulate 20 seconds
    for _ in range(40):
        result = valve_position.compute()
        print(f"t={tm.get_time():4.1f}s: Valve={result['y']:5.1f}%")
        tm.advance(0.5)
