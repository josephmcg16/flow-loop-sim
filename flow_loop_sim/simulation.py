import pandas as pd
import numpy as np
from scipy.optimize import fsolve
from flow_loop_sim.factories import create_node, create_branch


class Simulation:
    def __init__(self, config: dict):
        self.calculate_residuals = self._build_model(config)

    def _build_model(self, config: dict):
        self.nodes = [create_node(node_config) for node_config in config["nodes"]]
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

        def calculate_residuals(x: np.ndarray, allow_reverse_flow) -> np.ndarray:
            flowrates = x[: len(self.branches)]
            flowrates = np.maximum(flowrates, 0.0) if not allow_reverse_flow else flowrates
            pressures = x[len(self.branches) :]
            for i, node in enumerate(self.nodes):
                if node.node_type == "reference":
                    pressures[i] = node.reference_pressure
            dp = np.array(
                [self.calculate_dp[j](flowrate) for j, flowrate in enumerate(flowrates)]
            )
            return np.hstack(
                [
                    self.incidence_matrix @ flowrates,
                    (self.incidence_matrix.T @ pressures - dp),
                ]
            )

        return calculate_residuals

    def solve_steady_state(
        self, flowrates_limits=(0, 10), pressures_limits=(0, 1e6), maxiter=500, allow_reverse_flow=False
    ) -> np.ndarray:
        # random doe for fsolve initial guess
        flowrates0 = np.random.uniform(*flowrates_limits, len(self.branches))
        pressures0 = np.random.uniform(*pressures_limits, len(self.nodes))

        for j, branch in enumerate(self.branches):
            if branch.branch_type == "control_valve":
                if branch.valve_travel < 1e-3:
                    flowrates0[j] = 0.0
            if branch.branch_type == "pump":
                if branch.pump_speed < 1e-3:
                    flowrates0[j] = 1e-6

        x0 = np.hstack([flowrates0, pressures0])
        sol = fsolve(
            self.calculate_residuals,
            x0,
            full_output=True,
            xtol=1e-8,
            maxfev=int(2e9),
            args=allow_reverse_flow,
        )

        iter = 0
        while sol[2] != 1:
            sol, _, _ = self.solve_steady_state(flowrates_limits, pressures_limits)
            iter += 1
            if iter >= maxiter:
                raise RuntimeError(sol[3])
        self.flowrates = sol[0][: len(self.branches)]
        self.pressures = sol[0][len(self.branches) :]
        return sol, self.flowrates, self.pressures
