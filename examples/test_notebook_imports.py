#!/usr/bin/env python3
"""
Quick test to verify all notebook imports work
"""
import sys
print("Testing notebook imports...")

# Test CDL imports
try:
    from cdl_python.time_manager import TimeManager, ExecutionMode
    from cdl_python.CDL.Reals.Sources import Constant, Sin
    print("✓ CDL imports successful")
except ImportError as e:
    print(f"✗ CDL import failed: {e}")
    sys.exit(1)

# Test CustomPWithLimiter import
try:
    sys.path.append('.')
    from custom_p_with_limiter import CustomPWithLimiter
    print("✓ CustomPWithLimiter import successful")
except ImportError as e:
    print(f"✗ CustomPWithLimiter import failed: {e}")
    sys.exit(1)

# Test other libraries
try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    print("✓ Pandas, NumPy, Matplotlib imports successful")
except ImportError as e:
    print(f"✗ Library import failed: {e}")
    print("Install with: pip install pandas numpy matplotlib")
    sys.exit(1)

# Quick functional test
print("\nRunning quick functional test...")
tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
const = Constant(time_manager=tm, k=5.0)
sin = Sin(time_manager=tm, amplitude=1.0, freqHz=1.0)
controller = CustomPWithLimiter(k=2.0)

ymax = const.compute()['y']
e = sin.compute()['y']
result = controller.compute(e=e, yMax=ymax)

print(f"  yMax = {ymax}")
print(f"  e = {e:.3f}")
print(f"  y = {result['y']:.3f}")
print("✓ Functional test passed")

print("\n" + "="*60)
print("All tests passed! The notebook should work now.")
print("="*60)
print("\nTo run the notebook:")
print("  jupyter notebook examples/task1_custom_p_with_limiter_demo.ipynb")
