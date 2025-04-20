# Flow Loop Simulation & Dashboard

A Python simulation of a **steady‑state closed‑loop piping network** paired with a lightweight React dashboard. The back end calculates flow‑rates and node pressures via a lumped‑parameter (nodal) model; the front end lets users adjust pump speeds and valve positions in real time and view the results in the browser.

---

## Table of Contents

- [Flow Loop Simulation \& Dashboard](#flowloopsimulationdashboard)
  - [Table of Contents](#tableofcontents)
  - [Features](#features)
    - [Simulation engine](#simulation-engine)
    - [Web dashboard](#web-dashboard)
  - [Project Structure](#projectstructure)
  - [Installation](#installation)
    - [Python back end](#python-back-end)
    - [Node front end](#node-front-end)
  - [Usage](#usage)
    - [Start the API](#start-the-api)
    - [Start the dashboard](#start-the-dashboard)
  - [Configuration](#configuration)
  - [Mathematical Formulation](#mathematicalformulation)
  - [Future Plans](#futureplans)

---

## Features

### Simulation engine

- **Nodal & Branch models** – pipes, pumps, control valves, static elevation changes.  

- **JSON‑configurable** – network topology and parameters in plain JSON.  

- **Steady‑state solver** – non‑linear system solved with `scipy.optimize.fsolve`.

### Web dashboard

- **Run button** – posts the current configuration to the API.  
- **Interactive sliders** – adjust `pump_speed` and `valve_travel` (0 – 1) before each run.  
- **Plotly charts** – bar charts for branch flow‑rates and node pressures.  
- **Tables** – numeric view of all branch and node results.

---

## Project Structure

```plain-text
flow-loop-sim/
│
├─ api.py                    # FastAPI wrapper exposing /simulate
├─ main.py                   # CLI entry point
│
├─ flow_loop_sim/            # core solver
│   ├─ factories.py
│   ├─ models.py
│   ├─ simulation.py
│   └─ utils.py
│
├─ configs/
│   └─ simple_parallel_system.json
│
└─ dashboard/                # React + TypeScript front‑end
    ├─ package.json
    ├─ vite.config.ts
    └─ src/
        ├─ App.tsx
        ├─ api.ts
        ├─ config.ts
        ├─ components/
        │   ├─ ConfigEditor.tsx
        │   ├─ FlowChart.tsx
        │   ├─ PressureChart.tsx
        │   ├─ BranchTable.tsx
        │   └─ NodeTable.tsx
        └─ …
```

---

## Installation

### Python back end

```bash
python -m venv .venv
source .venv\Scripts\activate
pip install -r requirements.txt
```

### Node front end

```bash
cd dashboard
npm install
```

---

## Usage

### Start the API

```bash
uvicorn api:app --reload --port 8000
```

### Start the dashboard

```bash
cd dashboard
npm run dev                           # opens http://localhost:5173
```

Open the browser, adjust pump speeds or valve positions with the sliders, and click **Run simulation** to see updated charts and tables.

The command‑line script is still available:

```bash
python main.py configs/simple_parallel_system.json
```

---

## Configuration

The network is defined in `configs/simple_parallel_system.json`. Key fields:

| Section    | Field                    | Description                                                               |
| ---------- | ------------------------ | ------------------------------------------------------------------------- |
| `nodes`    | `node_type`              | `"reference"` or `"junction"`                                             |
|            | `reference_pressure`     | Pressure for reference nodes (Pa)                                         |
| `branches` | `branch_type`            | `"static"`, `"pipe"`, `"pump"`, `"control_valve"`                         |
|            | Type‑specific parameters | `elevation_change`, `pump_speed`, `valve_travel`, `friction_factor`, etc. |

Pump speeds and valve travels are exposed as sliders in the dashboard (`0.0 – 1.0`). All other parameters can be edited directly in the JSON file.

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

## Future Plans

- Dynamic simulation (fluid inertia, compliance, controller dynamics)  
- Result history and comparison views  
- SVG schematic with drag‑and‑drop layout and colour‑by‑pressure  
- Single‑container deployment serving both API and static dashboard
