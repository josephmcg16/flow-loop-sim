from flow_loop_sim.models import (
    Node,
    Junction,
    Reference,
    Branch,
    StaticBranch,
    Pump,
    Pipe,
    ControlValve,
)


def create_node(node_dict):
    """
    Given a dict describing a node (including node_type),
    return the appropriate Node subclass instance.
    """
    node_type = node_dict.get("node_type", "junction")

    if node_type == "reference":
        return Reference(
            name=node_dict["name"],
            reference_pressure=node_dict.get("reference_pressure", 0.0),
        )
    elif node_type == "junction":
        return Junction(name=node_dict["name"])
    else:
        # Default or fallback – or raise an error
        # e.g., if node_dict has unrecognized node_type
        return Node(name=node_dict["name"], node_type=node_type)


def create_branch(branch_dict):
    """
    Given a dict describing a branch (including branch_type),
    return the appropriate Branch subclass instance.
    """
    branch_type = branch_dict["branch_type"]

    if branch_type == "static":
        return StaticBranch(
            name=branch_dict["name"],
            from_node_name=branch_dict["from_node_name"],
            to_node_name=branch_dict["to_node_name"],
            elevation_change=branch_dict["elevation_change"],
            density=branch_dict["density"],
            gravity=branch_dict.get("gravity", 9.81),
        )
    elif branch_type == "pump":
        return Pump(
            name=branch_dict["name"],
            from_node_name=branch_dict["from_node_name"],
            to_node_name=branch_dict["to_node_name"],
            num_of_pumps=branch_dict["num_of_pumps"],
            pump_speed=branch_dict["pump_speed"],
            density=branch_dict["density"],
            gravity=branch_dict.get("gravity", 9.81),
        )
    elif branch_type == "pipe":
        return Pipe(
            name=branch_dict["name"],
            from_node_name=branch_dict["from_node_name"],
            to_node_name=branch_dict["to_node_name"],
            friction_factor=branch_dict["friction_factor"],
            length=branch_dict["length"],
            diameter=branch_dict["diameter"],
            density=branch_dict["density"],
        )
    elif branch_type == "control_valve":
        return ControlValve(
            name=branch_dict["name"],
            from_node_name=branch_dict["from_node_name"],
            to_node_name=branch_dict["to_node_name"],
            valve_travel=branch_dict["valve_travel"],
            density=branch_dict["density"],
            gravity=branch_dict.get("gravity", 9.81),
        )
    else:
        raise ValueError(f"Unknown branch_type: {branch_type}")
