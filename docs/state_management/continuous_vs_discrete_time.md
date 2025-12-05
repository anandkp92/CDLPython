# Continuous vs. Discrete Time: Modelica/CDL and CDL Python

This document explains the fundamental difference between how Modelica handles continuous-time simulation and how CDL Python uses discrete-time execution.

## Table of Contents
- [Executive Summary](#executive-summary)
- [Modelica: Continuous-Time Simulation](#modelica-continuous-time-simulation)
- [CDL Python: Discrete-Time Execution](#cdl-python-discrete-time-execution)
- [Why CDL Python Uses Discrete Time](#why-cdl-python-uses-discrete-time)
- [Implications for Event Iteration](#implications-for-event-iteration)
- [Euler Discretization in CDL Python](#euler-discretization-in-cdl-python)

---

## Executive Summary

**You are correct!** CDL Python uses **discrete-time** execution, which is fundamentally different from Modelica's **continuous-time** simulation approach.

| Aspect | Modelica | CDL Python |
|--------|----------|------------|
| **Time Model** | Continuous (mathematical) | Discrete (sampled) |
| **Solver** | DAE solver (DASSL, CVODE, etc.) | Euler discretization |
| **Integration** | Variable timestep, adaptive | Fixed timestep (user-specified) |
| **State Updates** | Continuous derivatives `der(x)` | Discrete differences `Δx/Δt` |
| **Time Advance** | Solver determines dt | User/system determines dt |
| **Accuracy** | High (adaptive methods) | Depends on timestep size |
| **Purpose** | Physical simulation | Real-time control execution |

---

## Modelica: Continuous-Time Simulation

### Mathematical Model

In Modelica, time is **continuous**, and the system is described by **Differential Algebraic Equations (DAEs)**:

```modelica
// Continuous-time integrator in Modelica
model Integrator
  input Real u;
  output Real y;
  parameter Real k = 1.0;
  parameter Real y_start = 0.0;
initial equation
  y = y_start;
equation
  der(y) = k * u;  // Continuous derivative
end Integrator;
```

**Key points:**
- `der(y)` represents the **continuous derivative** dy/dt
- The equation `der(y) = k * u` is a **mathematical relationship**, not a computation
- It's always true at every infinitesimal instant in continuous time

### DAE Solver

Modelica tools (OpenModelica, Dymola, etc.) use sophisticated numerical solvers:

**Process:**
1. **Compile-time:** Convert Modelica model to system of DAEs
2. **Runtime:** DAE solver (e.g., DASSL) solves equations
3. **Variable timestep:** Solver automatically adjusts dt based on:
   - Local error estimates
   - Stiffness of equations
   - Event detection
4. **High accuracy:** Adaptive methods provide numerical accuracy guarantees

**From OpenModelica documentation:**
> "By default OpenModelica transforms a Modelica model into an ODE representation to perform a simulation by using numerical integration methods. DASSL is the default solver because it is an implicit, higher order, multi-step solver with step-size control."

### Event Handling

Even though time is continuous, **discrete events** can occur:

```modelica
when sample(0, 0.1) then
  // Execute every 0.1 seconds
  discrete_var := continuous_expr;
end when;
```

At event instants:
- DAE solver **stops** integration
- **Event iteration** occurs (what we're implementing!)
- Discrete variables updated
- Integration **resumes** with new initial conditions

---

## CDL Python: Discrete-Time Execution

### Sampled-Data Model

CDL Python operates in **discrete time** with fixed sampling intervals:

```python
# Discrete-time integrator in CDL Python
class IntegratorWithReset(CDLBlock):
    def compute(self, u, trigger, y_reset_in):
        current_time = self.get_time()
        dt = current_time - self._state['last_time']

        # Euler discretization: y[n+1] = y[n] + k * u * dt
        if dt > 0:
            self._state['y'] += self.k * u * dt

        self._state['last_time'] = current_time
        return {'y': self._state['y']}
```

**Key points:**
- Time advances in **discrete steps**: t₀, t₁, t₂, ...
- Each call to `compute()` is a **sample instant**
- Integration uses **Euler method**: `y[n+1] = y[n] + k * u[n] * dt`
- `dt` is the **sampling interval** (not infinitesimal)

### TimeManager: Two Modes

From `cdl_python/time_manager.py`:

```python
class ExecutionMode(Enum):
    SIMULATION = "simulation"  # Fixed timestep, manual advance
    REALTIME = "realtime"      # Wall-clock time
```

**SIMULATION mode:**
- Manual time advancement: `tm.advance(dt=0.1)`
- Fixed timestep (or user-specified per step)
- Time is `t[n] = t[0] + n * dt`

**REALTIME mode:**
- Wall-clock time from OS
- Samples occur at actual clock intervals
- For real building control systems

### No DAE Solver

CDL Python **does not solve DAEs**. Instead:

1. **Topological sorting** determines execution order (acyclic graph)
2. **Sequential evaluation** of blocks in that order
3. **Euler discretization** for continuous-time blocks (integrators, derivatives)
4. **Explicit computation** - no implicit equation solving

---

## Why CDL Python Uses Discrete Time

### 1. **Target Application: Real-Time Building Control**

CDL is designed for **building automation systems**, not simulation:

- Controllers run on embedded systems (Raspberry Pi, PLCs)
- BACnet communication has inherent sampling delays
- Sensors are read at discrete intervals (e.g., every 1 second)
- Actuator commands sent at discrete intervals

**Real-world building control IS discrete-time by nature!**

### 2. **Computational Efficiency**

Discrete-time execution is much faster:
- No DAE solver overhead
- No adaptive timestep calculations
- Simple forward Euler integration
- Predictable computation time per step

**Critical for real-time systems** where code must complete within sampling interval.

### 3. **Determinism and Predictability**

Fixed timesteps provide:
- Deterministic behavior (same inputs → same outputs)
- Known execution time bounds
- Easy to reason about timing
- Testable and verifiable

### 4. **CDL's Acyclic Requirement**

**From CDL specification:**
> "Connections that form an algebraic loop are not allowed."

This means:
- No need for implicit equation solving
- Simple topological execution works
- No need for DAE solver

### 5. **Simplicity**

Discrete-time is simpler to:
- Implement in Python
- Debug and test
- Explain to control engineers
- Deploy on embedded systems

---

## Implications for Event Iteration

### Modelica's Event Iteration

In Modelica continuous-time simulation:

```
Continuous integration at t ∈ [0, 10]
    ↓
Event detected at t = 5.247
    → Stop DAE solver
    → Event iteration (discrete variables update)
    → Resume integration from t = 5.247 with new conditions
```

Events are **embedded in continuous time** - the solver stops and resumes.

### CDL Python's Event Iteration

In CDL Python discrete-time execution:

```
Sample at t = 0.0
    → Evaluate all blocks
    → Update states
Sample at t = 0.1
    → Evaluate all blocks
    → Update states
Sample at t = 0.2
    → Evaluate all blocks
    → Update states
...
```

**Every sample instant IS an event instant!**

There's no "continuous integration" between samples. Time only exists at discrete points:
- t ∈ {0.0, 0.1, 0.2, 0.3, ...} in SIMULATION mode
- t ∈ {wall clock samples} in REALTIME mode

**Event iteration** in CDL Python means:
- At each sample instant
- Evaluate all blocks using pre-values from previous sample
- Update all states simultaneously
- Move to next sample instant

This is different from Modelica's "stop the DAE solver and iterate" - we have no DAE solver to stop!

---

## Euler Discretization in CDL Python

### How Continuous-Time Blocks Become Discrete

Consider a continuous-time integrator:

**Continuous (Modelica):**
```
dy/dt = k * u(t)
y(t) = y₀ + ∫₀ᵗ k * u(τ) dτ
```

**Discrete (CDL Python):**
```
y[n+1] = y[n] + k * u[n] * Δt
```

Where:
- `y[n]` = state at sample n
- `u[n]` = input at sample n
- `Δt` = sampling interval

### Example: Integrator

**Continuous integration (exact):**
```
t ∈ [0, 1], u(t) = 2.0, k = 1.0, y₀ = 0
y(t) = ∫₀ᵗ 2.0 dt = 2.0t
y(1.0) = 2.0  ← Exact
```

**Euler discretization (Δt = 0.1):**
```
y[0] = 0
y[1] = y[0] + 1.0 * 2.0 * 0.1 = 0.2
y[2] = y[1] + 1.0 * 2.0 * 0.1 = 0.4
...
y[10] = 2.0  ← Matches exact solution!
```

**With larger Δt = 0.5:**
```
y[0] = 0
y[1] = 0 + 1.0 * 2.0 * 0.5 = 1.0
y[2] = 1.0 + 1.0 * 2.0 * 0.5 = 2.0
← Still matches (for this linear case)
```

### Accuracy Considerations

**Euler method accuracy:**
- **Linear systems:** Often exact or very close
- **Nonlinear systems:** Error accumulates
- **Smaller Δt:** Better accuracy, more computation
- **Larger Δt:** Faster, less accurate, may be unstable

**Rule of thumb:** Choose Δt based on:
- Fastest dynamics in your system
- Required accuracy
- Real-time constraints
- Nyquist sampling theorem (Δt < 1/(2*f_max))

For building control: Δt = 0.1 to 1.0 seconds is typical.

---

## Comparison: Integrator Example

### Modelica Continuous-Time

```modelica
model Controller
  Reals.IntegratorWithReset integrator(k=1.0, y_start=0.0);

equation
  integrator.u = input_signal;
  integrator.trigger = reset_signal;
  output_signal = integrator.y;

end Controller;
```

**Simulation:**
- DAE solver chooses timesteps automatically
- Might use dt = 0.001, 0.01, 0.1 (varies)
- High accuracy integration
- Solves `der(y) = k * u` continuously

### CDL Python Discrete-Time

```python
from cdl_python.CDL.Reals import IntegratorWithReset
from cdl_python.time_manager import TimeManager, ExecutionMode

# Create time manager with fixed timestep
tm = TimeManager(mode=ExecutionMode.SIMULATION, time_step=0.1)

# Create integrator
integrator = IntegratorWithReset(time_manager=tm, k=1.0, y_start=0.0)

# Simulation loop (discrete time)
for i in range(100):
    output = integrator.compute(
        u=input_signal,
        trigger=reset_signal,
        y_reset_in=0.0
    )

    print(f"t={tm.get_time():.1f}, y={output['y']:.3f}")

    tm.advance()  # Advance by 0.1 seconds
```

**Execution:**
- Fixed timestep: dt = 0.1 always
- Euler discretization
- Samples at t = {0.0, 0.1, 0.2, ..., 9.9}
- Explicit computation (no solver)

---

## Summary

### Modelica/CDL (Continuous-Time Simulation)
- ✅ Mathematical continuous time
- ✅ DAE solver with adaptive timesteps
- ✅ High numerical accuracy
- ✅ Good for physical simulation
- ❌ Computationally expensive
- ❌ Not deterministic (solver-dependent)
- ❌ Overkill for real-time control

### CDL Python (Discrete-Time Execution)
- ✅ Discrete sampled time
- ✅ Fixed timesteps (user-specified)
- ✅ Fast and predictable
- ✅ Perfect for real-time control
- ✅ Matches real building automation systems
- ❌ Lower accuracy than adaptive methods
- ❌ Requires appropriate timestep choice
- ✅ But: Accuracy is sufficient for building control!

### Event Iteration in Both

Despite the time model difference, **both need event iteration semantics**:

**Why?** To ensure all blocks see **consistent state snapshot** at each:
- Event instant (Modelica continuous-time)
- Sample instant (CDL Python discrete-time)

This is what our two-phase execution model implements!

---

## Sources

- [OpenModelica Solving](https://openmodelica.org/doc/OpenModelicaUsersGuide/latest/solving.html)
- [Modelica Synchronous Elements](https://specification.modelica.org/v3.4/Ch16.html)
- [CDL Discrete Blocks](https://simulationresearch.lbl.gov/modelica/releases/v5.0.0/help/Buildings_Controls_OBC_CDL_Discrete.html)
- [Discrete-Event Simulation of Continuous Systems](https://journals.sagepub.com/doi/10.1177/00375497241230985)
- [CDL Specification](https://obc.lbl.gov/specification/cdl.html)
