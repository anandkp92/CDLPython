# Debug test to understand timer behavior
from cdl_python.time_manager import TimeManager
from cdl_python.CDL.Logical import Timer

def test_timer_debug():
    """Debug timer to see what's happening"""
    tm = TimeManager(mode='simulation', time_step=0.1)
    timer = Timer(time_manager=tm, t=2.0)

    print(f"\nInitial time: {tm.get_time()}")
    result = timer.compute(u=True)
    print(f"After first compute: time={tm.get_time()}, y={result['y']}, entry_time={timer._entry_time}")

    tm.advance(dt=0.1)
    print(f"After advance: time={tm.get_time()}")
    result = timer.compute(u=True)
    print(f"After second compute: time={tm.get_time()}, y={result['y']}, entry_time={timer._entry_time}")

    assert result['y'] > 0, f"Expected positive elapsed time, got {result['y']}"
