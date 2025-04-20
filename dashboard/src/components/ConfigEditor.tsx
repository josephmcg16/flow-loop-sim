interface Props {
    /** full network config object */
    config: any;
    /** callback with *new* config whenever a slider moves */
    onChange: (cfg: any) => void;
}

/**
 * Lists every pump and control‑valve branch
 *   – pumps expose a `pump_speed` slider
 *   – control valves expose a `valve_travel` slider
 */
export default function ConfigEditor({ config, onChange }: Props) {
    const handleSlider = (
        branchIdx: number,
        key: "pump_speed" | "valve_travel",
        value: number
    ) => {
        // shallow‑clone config → update just one branch
        const newBranches = config.branches.map((b: any, i: number) =>
            i === branchIdx ? { ...b, [key]: value } : b
        );
        onChange({ ...config, branches: newBranches });
    };

    return (
        <section className="config-editor">
            <h2>Adjust parameters</h2>

            {config.branches.map((b: any, idx: number) => {
                if (b.branch_type === "pump" || b.branch_type === "control_valve") {
                    const key = b.branch_type === "pump" ? "pump_speed" : "valve_travel";
                    const label =
                        b.branch_type === "pump" ? "Pump speed" : "Valve position";
                    const value = b[key] ?? 0;

                    return (
                        <div key={b.name} className="param-row">
                            <label htmlFor={`${b.name}-${key}`}>
                                {b.name} — {label}: <strong>{value.toFixed(2)}</strong>
                            </label>

                            <input
                                id={`${b.name}-${key}`}
                                type="range"
                                min={0}
                                max={1}
                                step={0.01}
                                value={value}
                                onChange={(e) =>
                                    handleSlider(idx, key as any, parseFloat(e.target.value))
                                }
                            />
                        </div>
                    );
                }
                return null;
            })}
        </section>
    );
}
