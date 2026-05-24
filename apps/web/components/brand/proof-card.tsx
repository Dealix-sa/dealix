export function ProofCard({
  customer,
  result,
  evidence,
  approved,
}: {
  customer: string;
  result: string;
  evidence: string;
  approved: boolean;
}) {
  return (
    <div className="dlx-card" style={{ marginBottom: 0 }}>
      <h2>{customer}</h2>
      <p style={{ margin: "4px 0", fontSize: 14 }}>{result}</p>
      <div className="dlx-source">evidence: {evidence}</div>
      <div style={{ marginTop: 8 }}>
        <span className={`dlx-badge ${approved ? "ok" : "warn"}`}>
          {approved ? "approved for external use" : "internal only"}
        </span>
      </div>
    </div>
  );
}
