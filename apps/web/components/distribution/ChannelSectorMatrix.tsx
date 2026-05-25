import type { ChannelSectorCell } from "../../lib/types";

function pillFor(status: ChannelSectorCell["status"]): string {
  if (status === "double_down") return "pill pill-ok";
  if (status === "fix") return "pill pill-warn";
  if (status === "kill") return "pill pill-danger";
  return "pill";
}

export function ChannelSectorMatrix({ cells }: { cells: ChannelSectorCell[] }) {
  return (
    <div className="card">
      <h2>Channels × Sectors</h2>
      {cells.length === 0 ? (
        <p style={{ margin: 0, opacity: 0.7 }}>لم تُسجّل تجارب توزيع بعد.</p>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th align="left">Channel</th>
              <th align="left">Sector</th>
              <th align="left">Replies</th>
              <th align="left">Positive</th>
              <th align="left">Verdict</th>
            </tr>
          </thead>
          <tbody>
            {cells.map((cell) => (
              <tr key={`${cell.channel}:${cell.sector}`}>
                <td>{cell.channel}</td>
                <td>{cell.sector}</td>
                <td>{cell.replies}</td>
                <td>{cell.positive}</td>
                <td>
                  <span className={pillFor(cell.status)}>{cell.status.replace("_", " ")}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
