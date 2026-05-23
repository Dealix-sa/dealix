import type { FunnelStage } from "../../lib/types";

export function SalesFunnel({ stages }: { stages: FunnelStage[] }) {
  const max = Math.max(1, ...stages.map((s) => s.count));
  return (
    <div className="card">
      <h2>Sales Funnel</h2>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th align="left">Stage</th>
            <th align="left">Count</th>
            <th align="left">Bar</th>
          </tr>
        </thead>
        <tbody>
          {stages.map((s) => (
            <tr key={s.stage}>
              <td>{s.stage}</td>
              <td>{s.count}</td>
              <td>
                <div
                  style={{
                    height: 8,
                    width: `${(s.count / max) * 100}%`,
                    minWidth: 2,
                    background: "#0f172a",
                    borderRadius: 4,
                  }}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
