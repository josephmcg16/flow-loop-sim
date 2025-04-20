import { BranchResult } from "../api";

export default function BranchTable({ branches }: { branches: BranchResult[] }) {
    return (
        <table>
            <thead>
                <tr>
                    <th>Branch</th>
                    <th>Flowrate (l/s)</th>
                </tr>
            </thead>
            <tbody>
                {branches.map((b) => (
                    <tr key={b.branch_name}>
                        <td>{b.branch_name}</td>
                        <td>{b["flowrate (l/s)"].toFixed(2)}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}
