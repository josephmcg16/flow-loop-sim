from flow_loop_sim.utils import (
    pump_pressure_rise,
    darcy_weisbach_pressure_drop,
    valve_pressure_drop,
)  # placeholders for library of pressure change functions


NODE_TYPES = ["junction", "reference"]
BRANCH_TYPES = ["static", "pipe", "pump", "control_valve"]


class Node:
    def __init__(self, name: str, node_type: str = "junction"):
        self.name = name
        if node_type not in NODE_TYPES:
            raise ValueError(
                f"Invalid node type: {node_type}. Must be one of {NODE_TYPES}."
            )
        self.node_type = node_type


class Branch:
    def __init__(
        self,
        name: str,
        from_node_name: str,
        to_node_name: str,
        branch_type: str = "static",
    ):
        self.name = name
        self.from_node = from_node_name
        self.to_node = to_node_name
        if branch_type not in BRANCH_TYPES:
            raise ValueError(
                f"Invalid branch type: {branch_type}. Must be one of {BRANCH_TYPES}."
            )
        self.branch_type = branch_type

    def calculate_dp(self, flow_rate: float) -> float:
        raise NotImplementedError("This method should be implemented in subclasses.")


class Junction(Node):
    def __init__(
        self,
        name: str,
    ):
        super().__init__(name, node_type="junction")


class Reference(Node):
    def __init__(self, name: str, reference_pressure: float):
        super().__init__(name, node_type="reference")
        self.reference_pressure = reference_pressure


class StaticBranch(Branch):
    def __init__(
        self,
        name: str,
        from_node_name: str,
        to_node_name: str,
        elevation_change: float,
        density: float,
        gravity: float = 9.81,
    ):
        super().__init__(name, from_node_name, to_node_name, branch_type="static")
        self.density = density
        self.elevation_change = elevation_change
        self.gravity = gravity
        self.static_pressure_change = density * gravity * elevation_change

    def calculate_dp(self, flow_rate: float) -> float:
        return self.static_pressure_change


class Pump(Branch):
    def __init__(
        self,
        name: str,
        from_node_name: str,
        to_node_name: str,
        num_of_pumps: int,
        pump_speed: float,
        density: float,
        gravity: float = 9.81,
    ):
        super().__init__(name, from_node_name, to_node_name, branch_type="pump")
        self.num_of_pumps = num_of_pumps
        self.pump_speed = pump_speed
        self.density = density
        self.gravity = gravity

    def calculate_dp(self, flow_rate: float) -> float:
        return pump_pressure_rise(
            flow_rate / self.num_of_pumps,
            self.pump_speed,
            self.density,
            self.gravity,
        )


class Pipe(Branch):
    def __init__(
        self,
        name: str,
        from_node_name: str,
        to_node_name: str,
        friction_factor: float,
        length: float,
        diameter: float,
        density: float,
    ):
        super().__init__(name, from_node_name, to_node_name, branch_type="pipe")
        self.friction_factor = friction_factor
        self.length = length
        self.diameter = diameter
        self.density = density

    def calculate_dp(self, flow_rate: float) -> float:
        return -1 * darcy_weisbach_pressure_drop(
            flow_rate,
            self.friction_factor,
            self.length,
            self.diameter,
            self.density,
        )


class ControlValve(Branch):
    def __init__(
        self,
        name: str,
        from_node_name: str,
        to_node_name: str,
        valve_travel: float,
        density: float,
        gravity: float = 9.81,
    ):
        super().__init__(
            name, from_node_name, to_node_name, branch_type="control_valve"
        )
        self.valve_travel = valve_travel
        self.density = density
        self.gravity = gravity

    def calculate_dp(self, flow_rate: float) -> float:
        return -1 * valve_pressure_drop(
            flow_rate,
            self.valve_travel,
            self.density,
            self.gravity,
        )
