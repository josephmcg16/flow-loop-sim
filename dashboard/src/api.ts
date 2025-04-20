export interface BranchResult {
    branch_name: string;
    "flowrate (l/s)": number;
}

export interface NodeResult {
    node_name: string;
    "pressure (barg)": number;
}

export interface SimResult {
    branches: BranchResult[];
    nodes: NodeResult[];
}

export async function runSimulation(config: unknown): Promise<SimResult> {
    const res = await fetch("http://localhost:8000/simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(config),
    });
    if (!res.ok) {
        throw new Error(`Backend error ${res.status}`);
    }
    return res.json();
}
