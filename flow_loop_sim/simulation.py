import pandas as pd
import numpy as np
from scipy.optimize import fsolve
from flow_loop_sim.factories import create_node, create_branch


class Simulation:
    def __init__(self, config: dict):
        self.calculate_residuals = self._build_model(config)

    def _build_model(self, config: dict):
        self.nodes = [
            create_node(node_config) for node_config in config["nodes"]
        ]
        self.branches = [
            create_branch(branch_config) for branch_config in config["branches"]
        ]

        node_names_vec = pd.DataFrame(config["nodes"])["name"].to_numpy()[:, None]
        branch_from_vec, branch_to_vec = (
            pd.DataFrame(config["branches"])[["from_node_name", "to_node_name"]]
            .to_numpy()
            .T
        )
        self.incidence_matrix = (node_names_vec == branch_to_vec).astype(int) - (
            node_names_vec == branch_from_vec
        )
        self.calculate_dp = [branch.calculate_dp for branch in self.branches]

        def calculate_residuals(x: np.ndarray) -> np.ndarray:
            flowrates = x[: len(self.branches)]
            flowrates = np.maximum(flowrates, 0.0)  # Ensure non-negative flowrates
            pressures = x[len(self.branches) :]
            for i, node in enumerate(self.nodes):
                if node.node_type == "reference":
                    pressures[i] = node.reference_pressure
            dp = np.array([self.calculate_dp[j](flowrate) for j, flowrate in enumerate(flowrates)])
            return np.hstack(
                [
                    self.incidence_matrix @ flowrates,
                    self.incidence_matrix.T @ pressures - dp,
                ]
            )

        return calculate_residuals


    def solve_steady_state(self) -> np.ndarray:
        flowrates0 = [0.1] * len(self.branches)
        pressures0 = [1e5] * len(self.nodes)
        x0 = np.concatenate([flowrates0, pressures0])
        sol = fsolve(self.calculate_residuals, x0, full_output=True, xtol=1e-6, maxfev=int(1e9))
        if sol[2] != 1:
            raise RuntimeError(sol[3])
        self.flowrates = sol[0][: len(self.branches)]
        self.pressures = sol[0][len(self.branches) :]
        return sol, self.flowrates, self.pressures
