import { NodeResult } from "../api";

export default function NodeTable({ nodes }: { nodes: NodeResult[] }) {
    return (
        <table>
            <thead>
                <tr>
                    <th>Node</th>
                    <th>Pressure (barg)</th>
                </tr>
            </thead>
            <tbody>
                {nodes.map((n) => (
                    <tr key={n.node_name}>
                        <td>{n.node_name}</td>
                        <td>{n["pressure (barg)"].toFixed(3)}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}
