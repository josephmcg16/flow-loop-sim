import json
import pandas as pd
import plotly.express as px
from flow_loop_sim.simulation import Simulation


with open("configs\\simple_parallel_system.json") as file:
    config = json.load(file)

sim = Simulation(config)
sol, flowrates, pressures = sim.solve_steady_state()

df_branches = pd.DataFrame(
    {
        "flowrate (l/s)": flowrates * 1000,
        "branch_name": [branch.name for branch in sim.branches],
    }
)

df_nodes = pd.DataFrame(
    {
        "pressure (barg)": pressures / 1e5,
        "node_name": [node.name for node in sim.nodes],
    }
)

fig_q = px.bar(
    df_branches,
    x="branch_name",
    y="flowrate (l/s)",
    title="Flowrates in branches",
)

fig_p = px.bar(
    df_nodes,
    x="node_name",
    y="pressure (barg)",
    title="Pressure at nodes",
)

fig_q.show()
fig_p.show()
