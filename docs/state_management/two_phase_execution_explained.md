# Event Iteration Model Explained (Modelica/CDL Semantics)

This document explains how CDL Python implements event iteration to match Modelica/CDL semantics, ensuring that all blocks see consistent state snapshots.

## Table of Contents
- [The Problem with Immediate Updates](#the-problem-with-immediate-updates-current-cdl-python)
- [Event Iteration - How It Works](#event-iteration---how-it-actually-works)
- [Why Does This Matter?](#why-does-this-matter-a-real-example)
- [Understanding "Simultaneous"](#simultaneous-doesnt-mean-parallel-execution)
- [Data Flow Timeline](#data-flow-when-do-outputs-become-visible)
- [Simple Analogy](#simple-analogy)
- [Implementation Changes](#what-this-means-for-implementation)

---

## The Problem with Immediate Updates (Current CDL Python)

Let's say you have this simple control system:

```
Temperature Sensor (22°C)
         ↓
    [Integrator A] → state = 10.0
         ↓
    [Gain × 2]
         ↓
    [Integrator B] → state = 5.0
         ↓
    Output
```

### What Happens NOW (Immediate Update) - Step by Step

At event instant t=1.0, with dt=0.1:

**Step 1:** Integrator A evaluates
- Reads input: 22°C
- Computes: state = 10.0 + (22 × 0.1) = 12.2
- **IMMEDIATELY updates its state to 12.2**
- Returns output: 12.2

**Step 2:** Gain evaluates
- Reads input: 12.2 (the NEW value from Integrator A)
- Computes: 12.2 × 2 = 24.4
- Returns output: 24.4

**Step 3:** Integrator B evaluates
- Reads input: 24.4
- Computes: state = 5.0 + (24.4 × 0.1) = 7.44
- **IMMEDIATELY updates its state to 7.44**
- Returns output: 7.44

**Problem:** Integrator B sees the UPDATED state from Integrator A (12.2), not the value from the previous event instant (10.0).

**This violates Modelica semantics** where all equations should see consistent values at an event instant.

---

## Event Iteration - How It Actually Works

In Modelica, discrete variables are updated through **event iteration**:

1. All blocks evaluate using values from **previous event instant** (accessed via `pre()`)
2. New values are computed
3. If any discrete variable changed (`pre(v) ≠ v`), trigger another iteration
4. Repeat until all discrete variables stabilize (`pre(v) = v` for all v)

### Our Implementation: Equation Evaluation + State Update

We split this into two phases at each event instant:

### PHASE 1: Equation Evaluation - Compute All Outputs

All blocks evaluate **at the same event instant** using **pre-values** (states from previous instant):

**Integrator A evaluates:**
- Current state (pre-value): 10.0
- Reads input: 22°C
- Computes NEW output: 12.2
- **Stores this in temporary output**
- **Does NOT change state yet!** (state still = pre(state) = 10.0)

**Gain evaluates:**
- Reads input from Integrator A's **temporary output**: 12.2
- Computes: 12.2 × 2 = 24.4
- **Stores in temporary output**

**Integrator B evaluates:**
- Current state (pre-value): 5.0
- Reads input from Gain's **temporary output**: 24.4
- Computes NEW output: 7.44
- **Stores in temporary output**
- **Does NOT change state yet!** (state still = pre(state) = 5.0)

**After Phase 1:**
- Integrator A: pre(state) = 10.0, computed output = 12.2
- Integrator B: pre(state) = 5.0, computed output = 7.44

### PHASE 2: State Update - Commit All Discrete Variables

Now ALL blocks update their discrete states together (the event iteration completes):

**Integrator A updates:**
- State: 10.0 → 12.2

**Integrator B updates:**
- State: 5.0 → 7.44

**After Phase 2:**
- Integrator A: state = 12.2 (now this becomes pre(state) for next event)
- Integrator B: state = 7.44 (now this becomes pre(state) for next event)
- Ready for next event instant!

**Check:** Did any variable change? Yes, so event iteration would check conditions again. If no more changes, we're done with this event instant.

---

## Why Does This Matter? A Real Example

Consider parallel branches (common in control systems):

```
          ┌──→ [Integrator A] →
Input ────┤                     [Add] → Output
          └──→ [Integrator B] →
```

At event instant t=1.0, both integrators have pre(state)=0, input=10, dt=0.1:

### Immediate Update (WRONG - violates Modelica semantics):
1. Integrator A evaluates first: state = 0 + 10×0.1 = 1.0, **updates immediately**
2. Integrator B evaluates: state = 0 + 10×0.1 = 1.0, **updates immediately**
3. Add evaluates: 1.0 + 1.0 = 2.0 ✓ (happens to work)

But what if execution order changes? What if Integrator A evaluates, then Add evaluates **before** Integrator B?

1. Integrator A: output = 1.0, state updates to 1.0
2. Add evaluates: 1.0 + 0.0 = 1.0 ❌ (WRONG! Integrator B hasn't evaluated yet!)
3. Integrator B: output = 1.0 (too late)

**Result depends on execution order!** This violates Modelica's principle that "order is irrelevant."

### Event Iteration (CORRECT - matches Modelica):
**Phase 1 (Equation Evaluation):**
- Integrator A: output = 1.0, pre(state) still 0
- Integrator B: output = 1.0, pre(state) still 0
- Add: reads both outputs → 1.0 + 1.0 = 2.0

**Phase 2 (State Update):**
- Both integrators update state to 1.0 simultaneously

**Result is always correct, regardless of evaluation order!**

---

## "Simultaneous" Doesn't Mean Parallel Execution

**Question:** "Does it all happen simultaneously?"

**Answer:** Conceptually yes (at the same event instant), implementation-wise no.

### What "Simultaneous" Really Means (in Modelica):

All blocks evaluate at the same **event instant** and see a **consistent snapshot** of discrete variables (via `pre()` values).

```python
# Implementation (runs sequentially)
# But BEHAVES as if all at same event instant

# === PHASE 1: Equation Evaluation ===
# These run one-by-one, but all use pre-values from previous event
result_A = blockA.evaluate(inputs)  # uses pre(state) from t_prev
result_B = blockB.evaluate(result_A['y'])  # uses pre(state) from t_prev
result_C = blockC.evaluate(result_B['y'])  # uses pre(state) from t_prev

# === PHASE 2: State Update ===
# All discrete variables advance to current event instant together
blockA.update_state()  # pre(state) becomes current state
blockB.update_state()  # pre(state) becomes current state
blockC.update_state()  # pre(state) becomes current state
```

**The key:** When Block C evaluates, it sees Block A and Block B's `pre(state)` from the **previous event instant**, even though their outputs for the **current event instant** have already been computed.

---

## Data Flow: When Do Outputs Become Visible?

Here's the timeline at an event instant:

```
Event instant t=1.0, all blocks have pre-values from t=0.9
    ↓
BlockA.evaluate()
    → computes new output based on pre(state)
    → stores in output variable
    → output is IMMEDIATELY available to downstream blocks
    → state NOT updated yet (still = pre(state))
    ↓
BlockB.evaluate()
    → reads BlockA's output (the new value!)
    → computes using its own pre(state)
    → stores in output variable
    → state NOT updated yet (still = pre(state))
    ↓
BlockC.evaluate()
    → reads BlockB's output
    → computes using its own pre(state)
    → stores output
    → state NOT updated yet (still = pre(state))
    ↓
=== All equations evaluated ===
    ↓
BlockA.update_state()
    → commits state change (pre → current)
    ↓
BlockB.update_state()
    → commits state change (pre → current)
    ↓
BlockC.update_state()
    → commits state change (pre → current)
    ↓
Check: Did any discrete variable change from pre-value?
    → If yes: trigger another event iteration
    → If no: event instant complete, ready for next event
```

### Key Points:

1. **Outputs** are computed during equation evaluation and immediately available
2. **Discrete states** (accessed via `pre()`) remain unchanged during all evaluations
3. **Discrete states** update only after all equations evaluated
4. Downstream blocks see:
   - Upstream **outputs** (newly computed for current event)
   - Upstream **states** (pre-values from previous event)

---

## Simple Analogy

Think of it like a classroom where everyone is filling out a form:

### Immediate Update (Current):
- Student A fills out their form, **hands it to teacher immediately**
- Student B looks at A's submitted form, fills theirs out, **hands it in**
- Student C looks at B's submitted form, fills theirs out, hands it in
- **Problem:** Later students see earlier students' NEW answers

### Event Iteration (Correct):
- **Phase 1 (Equation Evaluation):** Everyone fills out their form, but keeps it on their desk
  - Student A writes answers based on yesterday's data
  - Student B writes answers (can peek at A's form on their desk, but uses yesterday's data for their own calculations)
  - Student C writes answers (can see A and B's forms on desks, but uses yesterday's data for their own calculations)
- **Phase 2 (State Update):** Teacher says "Everyone update your records at the same time!"
  - All students update their record books simultaneously
  - **Now everyone's record books have today's values for tomorrow's calculations**

In Modelica terms:
- "Yesterday's data" = `pre(state)` (values from previous event instant)
- "Forms on desks" = computed outputs (available to downstream blocks)
- "Record books" = discrete state variables
- "Update records simultaneously" = event iteration completes

---

## What This Means for Implementation

You'll change from this:

```python
# Current - immediate update
def compute(self, inputs):
    # Block1 evaluates and updates state
    r1 = self.block1.compute(u=inputs)

    # Block2 sees block1's UPDATED state
    r2 = self.block2.compute(u=r1['y'])

    return r2
```

To this:

```python
# Event iteration model
def compute(self, inputs):
    # Phase 1: All blocks evaluate using pre-values
    r1 = self.block1.evaluate(u=inputs)      # uses pre(state), doesn't update
    r2 = self.block2.evaluate(u=r1['y'])     # uses pre(state), doesn't update

    # Phase 2: All blocks update discrete states together
    self.block1.update_state()  # NOW state updates (pre → current)
    self.block2.update_state()  # NOW state updates (pre → current)

    return r2
```

**The difference:** In phase 1, `block2.evaluate()` uses its own `pre(state)` from previous event instant, even though it uses `block1`'s newly computed output from the current event instant.

---

## Modelica Concepts Used

### `pre()` Operator
In Modelica, `pre(v)` returns the value of discrete variable `v` from the **left limit** at an event instant - i.e., the value before the current event's updates are committed.

**From Modelica spec:**
> "At an event instant, y(t_pre) is the value of y after the last event iteration at the previous time instant."

### Event Iteration
> "A new event is triggered if at least for one variable v 'pre(v) ≠ v' after the active model equations are evaluated at an event instant."

> "Event iteration is performed until the values are equal."

### Equation Sections
> "In contrast to an algorithm section, there is no order between the equations in an equation section and they can be solved separately."

### When Clauses
> "The equations within a when-equation are activated only at the instant when the scalar expression becomes true."

---

## Summary

The key insight is:
- **Outputs** flow immediately during equation evaluation
- **Discrete states** (via `pre()`) don't update until all equations evaluated
- This ensures **consistent state snapshot** at each event instant

This ensures:
1. ✅ Consistent state visibility across the entire system
2. ✅ Execution order doesn't affect results
3. ✅ Matches Modelica's "simultaneous" semantics
4. ✅ Matches CDL specification requirements
5. ✅ Correct behavior for parallel branches and complex topologies

---

## Sources

- [Modelica `pre()` Operator](https://build.openmodelica.org/Documentation/ModelicaReference.Operators.'pre()'.html)
- [Modelica Equations Specification](https://specification.modelica.org/master/equations.html)
- [Modelica Event Handling](http://doc.simulationx.com/4.0/1033/Content/10_Modelica/Event%20Handling.htm)
- [Modelica When Clause](https://build.openmodelica.org/Documentation/ModelicaReference.'when'.html)
- [CDL Specification](https://obc.lbl.gov/specification/cdl.html)
