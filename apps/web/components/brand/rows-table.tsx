import type { JSX } from "react";

interface RowsTableProps {
  rows: Array<Record<string, unknown>>;
  emptyMessage?: string;
  maxColumns?: number;
}

export function RowsTable({
  rows,
  emptyMessage = "No rows yet.",
  maxColumns = 8,
}: RowsTableProps): JSX.Element {
  if (!rows || rows.length === 0) {
    return <div className="dealix-empty">{emptyMessage}</div>;
  }
  const allKeys = Array.from(
    rows.reduce<Set<string>>((acc, r) => {
      Object.keys(r).forEach((k) => acc.add(k));
      return acc;
    }, new Set<string>()),
  ).slice(0, maxColumns);

  return (
    <table className="dealix-table">
      <thead>
        <tr>
          {allKeys.map((k) => (
            <th key={k}>{k}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((row, i) => (
          <tr key={i}>
            {allKeys.map((k) => (
              <td key={k}>{String((row as Record<string, unknown>)[k] ?? "—")}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
