# State Management Documentation

This directory contains documentation about state management and execution models in CDL Python using Modelica/CDL terminology.

## Documents

### 1. [Event Iteration Model Explained](two_phase_execution_explained.md)
A beginner-friendly explanation of how event iteration works in Modelica/CDL, with concrete examples and analogies.

**Read this first if you want to understand:**
- What's wrong with immediate state updates
- How event iteration actually works
- Why it matters for correctness
- When outputs flow vs when states update
- The role of `pre()` operator in Modelica

### 2. [Continuous vs. Discrete Time](continuous_vs_discrete_time.md)
**IMPORTANT:** Explains the fundamental difference between Modelica's continuous-time simulation and CDL Python's discrete-time execution.

**Read this to understand:**
- Why CDL Python uses discrete time (you're right!)
- How Modelica DAE solvers work vs our Euler discretization
- What "event iteration" means in discrete vs continuous time
- Accuracy and performance tradeoffs
- Why discrete time is perfect for real-time building control

### 3. [Research Findings](research_findings.md)
Detailed research on how Ptolemy II and Modelica/CDL handle state management and data flow.

**Read this for:**
- Technical details on execution models
- Modelica's simultaneous equation semantics
- Event iteration and discrete state updates
- Comparison between different systems
- References to official documentation

## Quick Summary

### Current Implementation (Immediate Update)
```python
def compute(self, inputs):
    r1 = self.block1.compute(u=inputs)  # computes AND updates state
    r2 = self.block2.compute(u=r1['y']) # sees block1's NEW state
    return r2
```

**Problem:** Later blocks see updated states from earlier blocks, violating Modelica's simultaneous semantics where all equations should see consistent `pre()` values at an event instant.

### Planned Implementation (Event Iteration)
```python
def compute(self, inputs):
    # Phase 1: All evaluate() use pre-values from previous event
    r1 = self.block1.evaluate(u=inputs)      # uses pre(state), doesn't update
    r2 = self.block2.evaluate(u=r1['y'])     # uses pre(state), doesn't update

    # Phase 2: All update_state() commit changes together
    self.block1.update_state()  # NOW state updates (pre → current)
    self.block2.update_state()  # NOW state updates (pre → current)

    return r2
```

**Benefit:** All blocks see consistent `pre(state)` snapshot at each event instant, matching Modelica/CDL semantics.

## Key Modelica/CDL Concepts

### Event Instant
A discrete point in time where:
- Discrete variables may change value
- When-clauses activate
- All equations evaluate using consistent `pre()` values
- Computation takes zero time

### `pre()` Operator
Returns the value of a discrete variable from the **previous event instant** (left limit).

**From Modelica spec:**
> "At an event instant, y(t_pre) is the value of y after the last event iteration at the previous time instant."

### Event Iteration
The process of repeatedly evaluating equations until all discrete variables stabilize:

1. Evaluate all active equations using `pre()` values
2. Compute new values for discrete variables
3. Check if any changed: `pre(v) ≠ v`
4. If yes, iterate again
5. If no, event instant complete

**From Modelica spec:**
> "A new event is triggered if at least for one variable v 'pre(v) ≠ v' after the active model equations are evaluated at an event instant."

### Equation Evaluation Phase
- All equations evaluate using `pre()` values
- Outputs computed and available to downstream blocks
- States NOT updated yet
- Order of evaluation doesn't matter (simultaneous semantics)

### State Update Phase
- All discrete variables update: `pre(v)` becomes current `v`
- All updates happen "simultaneously"
- After this, new values become `pre()` values for next event

### Synchronous Data Flow Principle
**From CDL spec:**
> "All variables keep their actual values until these values are explicitly changed. Variable values can be accessed at any time instant."

> "Computation and communication at an event instant does not take time."

## Why This Matters

1. **Correctness:** Matches Modelica/CDL specification semantics
2. **Order Independence:** Results don't depend on block evaluation order
3. **Parallel Branches:** Correct behavior when signals split and merge
4. **Compliance:** Follows synchronous data flow principle
5. **Predictability:** Consistent behavior across different implementations

## Implementation Phases

Our implementation uses two phases per event instant:

### Phase 1: Equation Evaluation
- Computes outputs based on current inputs and `pre(state)` values
- Stores outputs in variables (immediately available)
- Does NOT modify discrete state variables
- Equivalent to evaluating all equations at the event instant

### Phase 2: State Update
- Commits staged state updates
- All states update "simultaneously"
- After this phase, event iteration check occurs
- New states become `pre()` values for next event

### Terminology Mapping

| Modelica/CDL Term | Our Implementation | Purpose |
|-------------------|-------------------|---------|
| Event instant | Time point where compute() is called | Discrete time step |
| `pre(state)` | Previous state value | State from previous event |
| Equation evaluation | `evaluate()` method | Compute outputs without state change |
| State update | `update_state()` method | Commit discrete variable changes |
| Event iteration | Check if states changed | Detect need for re-evaluation |

## Related Files

- `docs/two_phase_execution_model.md` - Original analysis (Ptolemy terminology)
- `docs/modelica_semantics_and_cdl_python.md` - Semantic mismatch analysis
- `cdl_python/base.py` - Base class to be updated
- `cdl_python/checkpoint.py` - Checkpoint system for state persistence

## Sources

- [Modelica Equations Specification](https://specification.modelica.org/master/equations.html)
- [Modelica `pre()` Operator](https://build.openmodelica.org/Documentation/ModelicaReference.Operators.'pre()'.html)
- [Modelica When Clause](https://build.openmodelica.org/Documentation/ModelicaReference.'when'.html)
- [CDL Specification](https://obc.lbl.gov/specification/cdl.html)
