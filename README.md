# Flow Loop Simulation

A Python-based simulation of a **steady-state closed-loop piping network**. This project demonstrates a lumped-parameter (nodal) approach for computing flowrates and pressures in a simple test network. It is designed to serve as an early proof-of-concept **“digital twin”** for a flow-measurement calibration lab, with possible extensions to dynamic controllers, fluid inertia/compliance, and thermal effects. The following uses open source libraries, providing a low-cost solution.

## Table of Contents

- [Flow Loop Simulation](#flow-loop-simulation)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Project Structure](#project-structure)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Configuration](#configuration)
  - [Mathematical Formulation](#mathematical-formulation)
  - [Future Plans](#future-plans)

---

## Features

- **Nodal and Branch Models**: Nodes (junctions or reference pressures) are connected by branches (pipes, pumps, valves).  
- **Configurable via JSON**: Network topology, component parameters, fluid properties, etc. can be specified in JSON.  
- **Steady-State Simulation**: Solves a system of mass balance and pressure-flow relationships using `fsolve` from `scipy.optimize`.  
- **Modular Design**: Each component type (e.g., `Pipe`, `Pump`, `ControlValve`) encapsulates its own pressure-drop (or rise) calculations.  
- **Extendable to Dynamics**: The architecture is suitable for adding time-dependent mass/inertia, fluid compressibility, and controller dynamics.

---

## Project Structure

```plain-text
flow-loop-sim
├── configs
│   └── simple_parallel_system.json
├── flow_loop_sim
│   ├── factories.py      # Factory functions for Nodes and Branches
│   ├── models.py         # Node and Branch classes (Pipe, Pump, ControlValve, etc.)
│   ├── simulation.py     # Simulation manager (steady-state solver, etc.)
│   └── utils.py          # Helper utilities for pressure drop/rise calculations
└── main.py               # Entry point script
```

- **`main.py`**: A top-level script that loads the JSON config and runs the simulation.  
- **`configs/`**: Holds JSON configuration files describing the network’s nodes and branches.  
- **`flow_loop_sim/`**: Contains the core simulation logic, classes, and utilities.

---

## Installation

1. **Clone or Download** this repository.  
2. **Install Python dependencies** (preferably in a virtual environment) using [pip](https://pypi.org/project/pip/):

   ```bash
   pip install -r requirements.txt
   ```

3. You can now run the simulation by calling `python main.py` (see [Usage](#usage)).

---

## Usage

1. **Check or modify** the `configs/simple_parallel_system.json` file to adjust:
   - Node definitions (e.g., reference nodes, or junctions).
   - Branch definitions (pipes, pumps, valves, etc.).
   - Physical parameters (densities, friction factors, pump speeds, etc.).

2. **Run**:

   ```bash
   python main.py
   ```

   This will:
   - Parse the JSON config.
   - Create Node/Branch objects using `flow_loop_sim.factories`.
   - Assemble and solve the steady-state equations via `flow_loop_sim.simulation.Simulation`.
   - Plot flowrates by branch and nodal pressures via `plotly`.

3. **Output**:
   - Bar charts in separate windows showing flowrates in branches and pressures at nodes.
   - Console logs of the solution vectors (from `fsolve`).

---

## Configuration

The JSON config defines the network. Example (`simple_parallel_system.json`):

```json
{
    "nodes": [
        {
            "name": "Top of Tank",
            "node_type": "reference",
            "reference_pressure": 0.0
        },
        {
            "name": "Bottom of Tank"
        }
        // ...
    ],
    "branches": [
        {
            "name": "Through Buffer Tank",
            "from_node_name": "Top of Tank",
            "to_node_name": "Bottom of Tank",
            "branch_type": "static",
            "elevation_change": 5.0,
            "density": 880.0
        },
        // ...
    ]
}
```

- **`nodes`**:
  - `node_type`: `"reference"` or `"junction"`.
  - `reference_pressure`: Value for reference nodes (e.g., atmospheric).
- **`branches`**:
  - `branch_type`: `"static"`, `"pipe"`, `"pump"`, or `"control_valve"`.
  - Attributes required for each type (e.g., `elevation_change`, `pump_speed`, or friction factor parameters).

---

## Mathematical Formulation

The steady-state equations are derived from:

1. **Mass (Volume) Balance (Kirchhoff’s Current Law)**:
   $$
   A \vec{q} = 0
   $$
   Where $A$ is the incidence matrix that relates the direction of branches to/ from each node, $\vec{q}\in\mathbb{R}^{N_q}$ are the branch flowrates.

   The incidence matrix is defined by:

    $$
    A_{i,j} =
    \begin{cases}
    +1 & \text{if branch }j\text{ enters node } i, \\
    -1 & \text{if branch }j\text{ leaves node } i, \\
    0  & \text{otherwise.}
    \end{cases}
    $$

2. **Pressure Relationships (Kirchoff's Voltage Law)**:
   $$
   \Delta \vec{p} = A^T \vec{p} \quad \text{and} \quad \Delta \vec{p} = f(\vec{q})
   $$
   Where $\Delta\vec{p}$ is the branch pressure drops, $\vec{p}\in\mathbb{R}^{N_p}$ are the node pressures. Each branch component has its own function $f_j(\cdot)$ relating flowrate to pressure drop (or rise for pumps).

The system is then a nonlinear system of algebraic equations of the form:

$$
\begin{bmatrix}
    A& 0 \\
    0 & A^\top
\end{bmatrix}
\begin{bmatrix}
    \vec{q} \\
    \vec{p}
\end{bmatrix}
-\begin{bmatrix}
    0 \\
    f(\vec{q})
\end{bmatrix}
= 0
$$

$$
\begin{matrix}
    F(\vec{x})=0 \ , & \vec{x}=\begin{bmatrix}
    \vec{q} \\ \vec{p}
\end{bmatrix}
\end{matrix}
$$

Where $F:\mathbb{R}^{N_q + N_p}\mapsto\mathbb{R}^{N_q + N_p}$ is a generalised nonlinear vector function which must be minimized to solve the steady-state system.

In code terms, these relationships appear as the `calculate_residuals` function, which is numerically solved by `scipy.optimize.fsolve`.

For more details, see the docstrings and the math references in `models.py` and `utils.py`.

---

## Future Plans

- **Dynamic Simulation**: Introduce fluid inertia, pipe compliance, real-time controllers, and solve a system of ODE/DAEs, i.e. systems of ODEs of the form $L\dot{\vec{q}}=A\vec{p}-f(\vec{q})$, $C\dot{\vec{p}}=A^\top\vec{p}$ where $L$ and $C$ are the equivalent lumped "inductance" and "capacitance" terms.
- **Thermal Effects**: Account for temperature-dependent properties and energy balances.
- **Advanced Controller Models**: PID loops, cascade controls, or custom logic for pumps and valves. I.e., introducing an additional state variable $\vec{u}$
which is governed by it's own dynamics, $\dot{\vec{u}}=f_u(\vec{u},t)$
- **Interface Improvements**: Provide user-friendly GUIs or config editors.
