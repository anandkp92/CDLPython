# ABOUTME: Test suite for stateful logical blocks (FallingEdge, Latch, Toggle, Pre, Change, Switch)
# ABOUTME: Tests logical blocks that maintain internal state
import pytest
from cdl_python.CDL.Logical import FallingEdge, Latch, Toggle, Pre, Change, Switch


class TestSwitch:
    """Test the Switch logical block (stateless)"""

    def test_switch_select_u1(self):
        """Test Switch selecting u1 when u2 is true"""
        switch = Switch()
        result = switch.compute(u1=True, u2=True, u3=False)
        assert result['y'] is True

    def test_switch_select_u3(self):
        """Test Switch selecting u3 when u2 is false"""
        switch = Switch()
        result = switch.compute(u1=True, u2=False, u3=False)
        assert result['y'] is False

    def test_switch_both_true(self):
        """Test Switch with both u1 and u3 true"""
        switch = Switch()
        result = switch.compute(u1=True, u2=True, u3=True)
        assert result['y'] is True

    def test_switch_both_false(self):
        """Test Switch with both u1 and u3 false"""
        switch = Switch()
        result = switch.compute(u1=False, u2=False, u3=False)
        assert result['y'] is False


class TestFallingEdge:
    """Test the FallingEdge detection block"""

    def test_falling_edge_initialization(self):
        """Test FallingEdge initializes correctly"""
        falling_edge = FallingEdge()
        result = falling_edge.compute(u=True)
        assert result['y'] is False

    def test_falling_edge_detection(self):
        """Test FallingEdge detects true to false transition"""
        falling_edge = FallingEdge()
        # Start with true
        result = falling_edge.compute(u=True)
        assert result['y'] is False
        # Transition to false should trigger
        result = falling_edge.compute(u=False)
        assert result['y'] is True
        # Staying false should not trigger
        result = falling_edge.compute(u=False)
        assert result['y'] is False

    def test_falling_edge_no_rising(self):
        """Test FallingEdge does not trigger on rising edge"""
        falling_edge = FallingEdge()
        result = falling_edge.compute(u=False)
        assert result['y'] is False
        result = falling_edge.compute(u=True)
        assert result['y'] is False

    def test_falling_edge_with_pre_u_start_true(self):
        """Test FallingEdge with pre_u_start=True"""
        falling_edge = FallingEdge(pre_u_start=True)
        # First input false should trigger (since pre_u_start was true)
        result = falling_edge.compute(u=False)
        assert result['y'] is True


class TestChange:
    """Test the Change detection block"""

    def test_change_initialization(self):
        """Test Change initializes correctly"""
        change = Change()
        result = change.compute(u=False)
        assert result['y'] is False

    def test_change_rising_edge(self):
        """Test Change detects false to true transition"""
        change = Change()
        result = change.compute(u=False)
        assert result['y'] is False
        result = change.compute(u=True)
        assert result['y'] is True
        result = change.compute(u=True)
        assert result['y'] is False

    def test_change_falling_edge(self):
        """Test Change detects true to false transition"""
        change = Change(pre_u_start=True)
        result = change.compute(u=True)
        assert result['y'] is False  # No change from True to True
        result = change.compute(u=False)
        assert result['y'] is True  # Change from True to False
        result = change.compute(u=False)
        assert result['y'] is False  # No change from False to False

    def test_change_with_pre_u_start_true(self):
        """Test Change with pre_u_start=True"""
        change = Change(pre_u_start=True)
        result = change.compute(u=False)
        assert result['y'] is True


class TestPre:
    """Test the Pre (delay) block"""

    def test_pre_initialization(self):
        """Test Pre initializes with pre_u_start"""
        pre = Pre()
        result = pre.compute(u=True)
        assert result['y'] is False  # Returns pre_u_start (default False)

    def test_pre_delays_input(self):
        """Test Pre delays input by one step"""
        pre = Pre()
        result = pre.compute(u=True)
        assert result['y'] is False
        result = pre.compute(u=False)
        assert result['y'] is True  # Returns previous value (True)
        result = pre.compute(u=True)
        assert result['y'] is False  # Returns previous value (False)

    def test_pre_with_start_true(self):
        """Test Pre with pre_u_start=True"""
        pre = Pre(pre_u_start=True)
        result = pre.compute(u=False)
        assert result['y'] is True


class TestLatch:
    """Test the Latch (SR latch) block"""

    def test_latch_initialization(self):
        """Test Latch initializes correctly"""
        latch = Latch()
        result = latch.compute(u=False, clr=False)
        assert result['y'] is False

    def test_latch_set(self):
        """Test Latch sets on rising edge of u"""
        latch = Latch()
        result = latch.compute(u=False, clr=False)
        assert result['y'] is False
        result = latch.compute(u=True, clr=False)
        assert result['y'] is True
        # Stays true even when u goes false
        result = latch.compute(u=False, clr=False)
        assert result['y'] is True

    def test_latch_clear(self):
        """Test Latch clears on rising edge of clr"""
        latch = Latch()
        # Set the latch
        result = latch.compute(u=True, clr=False)
        assert result['y'] is True
        # Clear the latch
        result = latch.compute(u=True, clr=True)
        assert result['y'] is False
        # Stays false even when clr goes false
        result = latch.compute(u=True, clr=False)
        assert result['y'] is False

    def test_latch_prevents_set_when_clr(self):
        """Test Latch does not set when clr is true"""
        latch = Latch()
        result = latch.compute(u=True, clr=True)
        assert result['y'] is False


class TestToggle:
    """Test the Toggle block"""

    def test_toggle_initialization(self):
        """Test Toggle initializes to false"""
        toggle = Toggle()
        result = toggle.compute(u=False, clr=False)
        assert result['y'] is False

    def test_toggle_first_press(self):
        """Test Toggle turns on with first rising edge"""
        toggle = Toggle()
        result = toggle.compute(u=False, clr=False)
        assert result['y'] is False
        result = toggle.compute(u=True, clr=False)
        assert result['y'] is True

    def test_toggle_second_press(self):
        """Test Toggle turns off with second rising edge"""
        toggle = Toggle()
        result = toggle.compute(u=False, clr=False)
        result = toggle.compute(u=True, clr=False)
        assert result['y'] is True
        # Release and press again
        result = toggle.compute(u=False, clr=False)
        assert result['y'] is True
        result = toggle.compute(u=True, clr=False)
        assert result['y'] is False

    def test_toggle_clear(self):
        """Test Toggle clears when clr is true"""
        toggle = Toggle()
        # Toggle on
        result = toggle.compute(u=True, clr=False)
        assert result['y'] is True
        # Clear
        result = toggle.compute(u=False, clr=True)
        assert result['y'] is False

    def test_toggle_ignores_clear_falling(self):
        """Test Toggle only responds to u rising edge"""
        toggle = Toggle()
        result = toggle.compute(u=True, clr=False)
        assert result['y'] is True
        # Falling edge of u should not toggle
        result = toggle.compute(u=False, clr=False)
        assert result['y'] is True
