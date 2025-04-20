import Plot from "react-plotly.js";
import { NodeResult } from "../api";

export default function PressureChart({ nodes }: { nodes: NodeResult[] }) {
    return (
        <Plot
            data={[
                {
                    type: "bar",
                    x: nodes.map((n) => n.node_name),
                    y: nodes.map((n) => n["pressure (barg)"]),
                },
            ]}
            layout={{ title: "Node pressures (barg)", margin: { t: 40 } }}
            style={{ width: "100%", height: 300 }}
        />
    );
}
