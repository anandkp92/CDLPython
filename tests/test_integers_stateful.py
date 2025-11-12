# ABOUTME: Test suite for stateful integer blocks (Change, OnCounter, Stage)
# ABOUTME: Tests integer blocks that maintain internal state
import pytest
from cdl_python.time_manager import TimeManager
from cdl_python.CDL.Integers import Change, OnCounter, Stage


class TestChange:
    """Test the Change detection block for integers"""

    def test_change_initialization(self):
        """Test Change initializes correctly"""
        change = Change(pre_u_start=5)
        result = change.compute(u=5)
        assert result['y'] is False
        assert result['up'] is False
        assert result['down'] is False

    def test_change_increase(self):
        """Test Change detects increase"""
        change = Change(pre_u_start=5)
        result = change.compute(u=10)
        assert result['y'] is True
        assert result['up'] is True
        assert result['down'] is False

    def test_change_decrease(self):
        """Test Change detects decrease"""
        change = Change(pre_u_start=10)
        result = change.compute(u=5)
        assert result['y'] is True
        assert result['up'] is False
        assert result['down'] is True

    def test_change_no_change(self):
        """Test Change when value stays same"""
        change = Change(pre_u_start=5)
        result = change.compute(u=5)
        assert result['y'] is False
        assert result['up'] is False
        assert result['down'] is False


class TestOnCounter:
    """Test the OnCounter block"""

    def test_oncounter_initialization(self):
        """Test OnCounter initializes to y_start"""
        counter = OnCounter(y_start=0)
        result = counter.compute(trigger=False, reset=False)
        assert result['y'] == 0

    def test_oncounter_trigger(self):
        """Test OnCounter increments on trigger"""
        counter = OnCounter(y_start=0)
        result = counter.compute(trigger=False, reset=False)
        assert result['y'] == 0
        result = counter.compute(trigger=True, reset=False)
        assert result['y'] == 1
        result = counter.compute(trigger=False, reset=False)
        assert result['y'] == 1
        result = counter.compute(trigger=True, reset=False)
        assert result['y'] == 2

    def test_oncounter_reset(self):
        """Test OnCounter resets to y_start"""
        counter = OnCounter(y_start=5)
        result = counter.compute(trigger=True, reset=False)
        assert result['y'] == 6
        result = counter.compute(trigger=False, reset=False)  # Release trigger
        assert result['y'] == 6
        result = counter.compute(trigger=True, reset=False)  # Trigger again
        assert result['y'] == 7
        result = counter.compute(trigger=False, reset=True)
        assert result['y'] == 5

    def test_oncounter_reset_priority(self):
        """Test reset has priority over trigger"""
        counter = OnCounter(y_start=0)
        result = counter.compute(trigger=True, reset=False)
        assert result['y'] == 1
        result = counter.compute(trigger=True, reset=True)
        assert result['y'] == 0  # Reset takes priority


class TestStage:
    """Test the Stage block"""

    def test_stage_initialization(self):
        """Test Stage initializes correctly"""
        tm = TimeManager(mode='simulation', time_step=0.1)
        stage = Stage(time_manager=tm, n=3, holdDuration=0.0)
        result = stage.compute(u=0.0)
        assert result['y'] == 0

    def test_stage_single_stage(self):
        """Test Stage with single input level"""
        tm = TimeManager(mode='simulation', time_step=0.1)
        stage = Stage(time_manager=tm, n=3, holdDuration=0.0)
        # Input 0.4 should select stage 1 (threshold 0.333)
        result = stage.compute(u=0.4)
        tm.advance(dt=0.1)
        result = stage.compute(u=0.4)
        assert result['y'] == 1

    def test_stage_max_stage(self):
        """Test Stage at maximum"""
        tm = TimeManager(mode='simulation', time_step=0.1)
        stage = Stage(time_manager=tm, n=3, holdDuration=0.0)
        result = stage.compute(u=1.0)
        tm.advance(dt=0.1)
        result = stage.compute(u=1.0)
        assert result['y'] == 3
