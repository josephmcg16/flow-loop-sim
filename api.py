from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import pandas as pd
from flow_loop_sim.simulation import Simulation

app = FastAPI(title="Flow‑Loop Simulation API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev port
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/simulate")
async def simulate(config: dict):
    """
    Accepts a full JSON network config and returns
    { "branches": [...], "nodes": [...] }
    identical to the structure your React code expects.
    """
    try:
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
        results = {
            "branches": df_branches.to_dict(orient="records"),
            "nodes": df_nodes.to_dict(orient="records"),
        }
        return JSONResponse(content=jsonable_encoder(results))

    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
