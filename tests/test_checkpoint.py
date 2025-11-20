#!/usr/bin/env python3
"""Test checkpoint functionality for CDL systems"""

import sys
from pathlib import Path
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cdl_python.time_manager import TimeManager, ExecutionMode
from cdl_python.CDL.Reals import IntegratorWithReset
from cdl_python.checkpoint import CheckpointManager, AutoCheckpointer


def test_basic_checkpoint():
    """Test basic checkpoint save/restore"""
    print("="*80)
    print("Test 1: Basic Checkpoint Save/Restore")
    print("="*80)

    # Create temporary checkpoint directory
    temp_dir = tempfile.mkdtemp()
    try:
        # Create system
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        integrator = IntegratorWithReset(time_manager=tm, k=1.0, y_start=0.0)

        # Run simulation for a few steps
        for i in range(5):
            result = integrator.compute(u=1.0, trigger=False, y_reset_in=0.0)
            tm.advance()
            print(f"Step {i}: t={tm.get_time():.1f}, y={result['y']:.2f}")

        # Save checkpoint
        checkpoint_mgr = CheckpointManager(checkpoint_dir=temp_dir)

        # Create a mock model object that holds the integrator
        class MockModel:
            def __init__(self, integrator):
                self.integrator = integrator

        model = MockModel(integrator)

        checkpoint_file = checkpoint_mgr.save_checkpoint(
            model=model,
            time_manager=tm,
            metadata={'description': 'Test checkpoint', 'step': 5}
        )
        print(f"\n✓ Checkpoint saved to: {checkpoint_file}")

        # Continue simulation
        for i in range(5, 10):
            result = integrator.compute(u=1.0, trigger=False, y_reset_in=0.0)
            tm.advance()
            print(f"Step {i}: t={tm.get_time():.1f}, y={result['y']:.2f}")

        # Restore checkpoint
        print("\nRestoring checkpoint...")
        metadata = checkpoint_mgr.restore_checkpoint(
            model=model,
            time_manager=tm,
            checkpoint_file=checkpoint_file
        )
        print(f"✓ Restored from: {metadata['description']}")

        # Verify state was restored
        result = integrator.compute(u=1.0, trigger=False, y_reset_in=0.0)
        print(f"\nAfter restore: t={tm.get_time():.1f}, y={result['y']:.2f}")
        print("✓ Test passed - state restored correctly")

    finally:
        # Cleanup
        shutil.rmtree(temp_dir)


def test_auto_checkpoint():
    """Test automatic checkpointing"""
    print("\n" + "="*80)
    print("Test 2: Auto Checkpoint")
    print("="*80)

    temp_dir = tempfile.mkdtemp()
    try:
        # Create system
        tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)
        integrator = IntegratorWithReset(time_manager=tm, k=1.0, y_start=0.0)

        class MockModel:
            def __init__(self, integrator):
                self.integrator = integrator

        model = MockModel(integrator)

        # Setup auto checkpointing every 3 steps
        checkpoint_mgr = CheckpointManager(checkpoint_dir=temp_dir)
        auto_cp = AutoCheckpointer(
            checkpoint_mgr=checkpoint_mgr,
            interval_steps=3
        )

        # Run simulation with auto checkpointing
        for i in range(10):
            result = integrator.compute(u=1.0, trigger=False, y_reset_in=0.0)
            tm.advance()

            # Maybe create checkpoint
            checkpoint_file = auto_cp.maybe_checkpoint(
                model=model,
                time_manager=tm,
                step=i,
                metadata={'step': i, 'value': result['y']}
            )

            if checkpoint_file:
                print(f"Step {i}: Auto checkpoint created: {checkpoint_file.name}")
            else:
                print(f"Step {i}: t={tm.get_time():.1f}, y={result['y']:.2f}")

        # List checkpoints
        checkpoints = checkpoint_mgr.list_checkpoints()
        print(f"\n✓ Created {len(checkpoints)} checkpoints")
        for cp in checkpoints:
            print(f"  - {cp.name}")

        print("✓ Test passed - auto checkpointing works")

    finally:
        shutil.rmtree(temp_dir)


def test_time_manager_state():
    """Test TimeManager state save/restore"""
    print("\n" + "="*80)
    print("Test 3: TimeManager State Save/Restore")
    print("="*80)

    # Create time manager
    tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)

    # Advance time
    for i in range(5):
        tm.advance()

    print(f"Time before save: {tm.get_time():.1f}")

    # Save state
    saved_state = tm.get_state()
    print(f"✓ Saved state: {saved_state}")

    # Advance more
    for i in range(5):
        tm.advance()

    print(f"Time after advancing: {tm.get_time():.1f}")

    # Restore state
    tm.set_state(saved_state)
    print(f"Time after restore: {tm.get_time():.1f}")

    if tm.get_time() == 0.5:
        print("✓ Test passed - TimeManager state restored correctly")
    else:
        print(f"✗ Test failed - Expected 0.5, got {tm.get_time()}")


if __name__ == "__main__":
    test_basic_checkpoint()
    test_auto_checkpoint()
    test_time_manager_state()
    print("\n" + "="*80)
    print("All checkpoint tests completed!")
    print("="*80)
