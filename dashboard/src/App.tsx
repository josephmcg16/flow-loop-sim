import { useState } from "react";
import "./index.css";
import initialConfig from "./config";
import { runSimulation, SimResult } from "./api";

import RunButton from "./components/RunButton";
import BranchTable from "./components/BranchTable";
import NodeTable from "./components/NodeTable";
import FlowChart from "./components/FlowChart";
import PressureChart from "./components/PressureChart";
import ConfigEditor from "./components/ConfigEditor";

export default function App() {
  /** editable copy of the JSON config */
  const [config, setConfig] = useState<any>(initialConfig);

  /** last simulation results */
  const [data, setData] = useState<SimResult | null>(null);

  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  const handleRun = async () => {
    setLoading(true);
    setErr(null);
    try {
      const res = await runSimulation(config);
      setData(res);
    } catch (e: any) {
      setErr(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <header>
        <h1>Flow‑Loop Dashboard</h1>
        <RunButton onClick={handleRun} disabled={loading} />
        {err && <span className="error">{err}</span>}
      </header>

      {/* NEW: parameter sliders */}
      <ConfigEditor config={config} onChange={setConfig} />

      {data && (
        <>
          <section className="charts">
            <FlowChart branches={data.branches} />
            <PressureChart nodes={data.nodes} />
          </section>

          <section className="tables">
            <BranchTable branches={data.branches} />
            <NodeTable nodes={data.nodes} />
          </section>
        </>
      )}
    </div>
  );
}
