# Research Findings: State Management in Ptolemy II and Modelica/CDL

This document summarizes research on how Ptolemy II and Modelica/CDL handle state management and data flow.

## Table of Contents
- [Ptolemy II Execution Model](#1-ptolemy-ii-execution-model)
- [Modelica/CDL Execution Model](#2-modelicacdl-execution-model)
- [Key Differences](#3-key-differences-ptolemy-vs-modelica)
- [What CDL Actually Uses](#4-what-cdl-actually-uses)
- [Implications for CDL Python](#5-implications-for-cdl-python-two-phase-implementation)
- [Sources](#sources)

---

## 1. Ptolemy II Execution Model

### Three-Phase Execution

Ptolemy II uses a strict three-phase actor execution model:

**Iteration Structure:**
- **One iteration** = `prefire()` → (multiple `fire()` calls) → `postfire()`
- **One execution** = `initialize()` → (multiple iterations) → `wrapup()`

### Phase Details

**`prefire()` - Readiness Check**
- Returns `true` if actor is ready to fire, `false` otherwise
- Checks preconditions (e.g., sufficient input tokens available)
- Does NOT modify state
- Called once per iteration

**`fire()` - Computation WITHOUT State Modification**
- **Critical rule:** "fire() should not change the state of the actor"
- Performs all computations based on current inputs and current state
- Produces outputs by calling `send()` on output ports (tokens deposited into receivers)
- **Can be called multiple times** in one iteration for fixed-point convergence
- Reads from persistent state but doesn't modify it

**`postfire()` - State Update**
- **This is where ALL state updates happen**
- Called exactly once per iteration, after all `fire()` calls complete
- Commits any state changes computed during `fire()`
- Returns `true` to continue execution, `false` to stop

### Data Flow Between Actors

**Token Production:**
- Tokens are sent to output ports during `fire()` via `send()` method
- `send()` deposits tokens into receiver objects immediately
- Tokens become available in receivers right away

**Token Consumption:**
- Downstream actors read tokens via `get()` on input ports during their `fire()` phase
- **Key insight:** Downstream actors can see outputs produced during upstream `fire()`, even before upstream `postfire()` executes
- The director (scheduler) controls the order of actor execution

**State Consistency:**
- Separation of computation (`fire`) from state updates (`postfire`) ensures consistency
- Multiple `fire()` calls see the same state snapshot
- All `fire()` calls complete before any `postfire()` modifies state
- This supports fixed-point iteration semantics

---

## 2. Modelica/CDL Execution Model

### Simultaneous Equation Semantics

Modelica uses a fundamentally different paradigm based on **simultaneous equations**:

**Core Principle:**
- "Modelica equations relate scalar variables by constraining the values that these variables can take **simultaneously**"
- Based on the **synchronous data flow principle** and **single assignment rule**
- Equations are declarative: "relationships are always true and order is irrelevant"

### Continuous vs. Discrete Time

**Continuous-Time Equations:**
- Entire model is a DAE (Differential Algebraic Equation) system
- DAE solver (e.g., DASSL, CVODE) solves all equations simultaneously at each time point
- Algebraic loops are solved together as a coupled system
- State derivatives `der(x)` are integrated over time

**Discrete-Time (When-Clause) Equations:**
- "when-equations are activated only at the instant when the scalar expression becomes true"
- Discrete variables are updated at **event instants** only
- Updates happen instantaneously (computation takes zero time)

### Event Handling and State Updates

**Event Iteration Process:**
1. Event triggered (e.g., `when` condition becomes true)
2. **Inner event iteration:**
   - Evaluate all when-clauses that are active
   - Update discrete state variables
   - Re-evaluate conditions
   - Repeat until discrete states stabilize
3. **Outer event step:**
   - Check if discrete variables changed from pre-values
   - If changed, update and perform another outer event step
   - If stable, resume continuous simulation

**Multiple Evaluations:**
- "Continuous-time part is typically evaluated **three times** at a sample instant"
- Once when sample instant is reached
- Once to evaluate continuous equations at the sample instant
- Once when event iteration occurs (since discrete variable changed)

### Data Flow Between Blocks

**In Continuous-Time:**
- All equations solved simultaneously by DAE solver
- Outputs computed together with all other variables
- No concept of "sequential execution" - it's a simultaneous algebraic system

**In Discrete-Time (CDL focus):**
- CDL enforces **acyclic topology** (no algebraic loops allowed)
- At each event instant:
  1. All active when-clauses evaluate
  2. All discrete states update together
  3. Event iteration continues until stable
- Values are consistent across all blocks at each instant

**Single Assignment Rule:**
- "Every input connector shall be connected to exactly one output connector"
- Each variable receives exactly one value per evaluation
- Guarantees consistency

---

## 3. Key Differences: Ptolemy vs. Modelica

| Aspect | Ptolemy II | Modelica/CDL |
|--------|-----------|--------------|
| **Execution Model** | Sequential actor firing | Simultaneous equation solving |
| **State Updates** | In `postfire()`, after all `fire()` | At event instants via event iteration |
| **Computation Phase** | `fire()` - explicit method call | Equation evaluation by DAE solver |
| **Multiple Evaluations** | Multiple `fire()` for fixed-point | Event iteration until discrete states stabilize |
| **Data Flow** | Tokens through ports/receivers | Variable connections (equations) |
| **Ordering** | Director controls firing order | Order irrelevant (simultaneous) |
| **State Visibility** | All `fire()` see same state snapshot | All equations see consistent state at event instant |

---

## 4. What CDL Actually Uses

Based on the CDL specification:

**From Modelica:**
- Synchronous data flow principle
- Single assignment rule
- Acyclic topology requirement (no algebraic loops)
- Instantaneous computation at event instants

**CDL-Specific Constraints:**
- Elementary blocks only (no arbitrary equations)
- Restricted to discrete-time control (not continuous simulation)
- Must break feedback loops with delay/integrator blocks
- "Consistent with Modelica Language Specification" semantics

**Key Quotes from CDL spec:**
> "All variables keep their actual values until these values are explicitly changed. Variable values can be accessed at any time instant."

> "Computation and communication at an event instant does not take time."

---

## 5. Implications for CDL Python Two-Phase Implementation

### What We Need to Match

**Modelica/CDL Semantics:**
- ✅ All blocks should see a **consistent state snapshot** at each time instant
- ✅ State updates happen **simultaneously** (conceptually)
- ✅ Output computations happen **before** state updates are committed
- ✅ Multiple evaluations possible until discrete states stabilize

**Ptolemy II Semantics:**
- ✅ Separate computation (`fire`) from state updates (`postfire`)
- ✅ Allow multiple `fire()` calls with same state
- ✅ All `fire()` complete before any `postfire()`
- ✅ Support for fixed-point iteration (if needed)

### Recommended Two-Phase Design

**For CDL Python, we should implement:**

```python
# Phase 1: Fire (Compute outputs without state modification)
for block in topological_order:
    block.fire(inputs)  # Computes outputs, stages state updates

# Phase 2: Postfire (Commit all state updates simultaneously)
for block in topological_order:
    block.postfire()  # Commits staged states
```

**This provides:**
1. ✅ Consistent state visibility (all `fire()` see states from time t)
2. ✅ Simultaneous state updates (all `postfire()` move to time t+1)
3. ✅ Matches Modelica's event iteration semantics
4. ✅ Matches Ptolemy's three-phase model
5. ✅ Supports fixed-point iteration if needed in future

---

## Sources

### Ptolemy II
- [Ptolemy II Actor Architecture](https://ptolemy.berkeley.edu/publications/papers/99/HMAD/html/actor.html)
- [Ptolemy II Actors](https://ptolemy.berkeley.edu/papers/98/HMAD/html/actor.html)
- [SDFDirector Documentation](http://ptolemy.berkeley.edu/ptolemyII/ptII11.0/ptII/doc/codeDoc/ptolemy/domains/sdf/kernel/SDFDirector.html)

### Modelica
- [Modelica Specification - Equations](https://specification.modelica.org/master/equations.html)
- [Modelica Specification - Synchronous Language Elements](https://specification.modelica.org/master/synchronous-language-elements.html)
- [OpenModelica DAE Solving](https://openmodelica.org/doc/OpenModelicaUsersGuide/latest/solving.html)
- [Modelica When Clause](https://mbe.modelica.university/behavior/discrete/when/)
- [Modelica Event Handling](https://doc.simulationx.com/4.2/1033/Content/Misc/Modelica/EventHandling.htm)

### CDL
- [CDL Specification](https://obc.lbl.gov/specification/cdl.html)

---

## Conclusion

**Both Modelica/CDL and Ptolemy II use a two-phase execution model** where:
1. **Computation happens first** (without modifying persistent state)
2. **State updates happen second** (all together, simultaneously)

This ensures consistent state visibility across all blocks/actors and matches the mathematical semantics of synchronous data flow systems.

**CDL Python should implement a two-phase model** to correctly match these semantics and ensure:
- Execution order independence
- Consistent state snapshots
- Correct behavior for parallel branches
- Compliance with Modelica/CDL specification
