import Plot from "react-plotly.js";
import { BranchResult } from "../api";

export default function FlowChart({ branches }: { branches: BranchResult[] }) {
    return (
        <Plot
            data={[
                {
                    type: "bar",
                    x: branches.map((b) => b.branch_name),
                    y: branches.map((b) => b["flowrate (l/s)"]),
                },
            ]}
            layout={{ title: "Branch flow‑rates (l/s)", margin: { t: 40 } }}
            style={{ width: "100%", height: 300 }}
        />
    );
}
