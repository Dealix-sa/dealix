"use client";

export default function ProofPanel({ items }: { items: { label: string; value: string }[] }) {
  return (
    <div className="card" style={{ marginTop: "var(--sp-6)" }}>
      <p className="eyebrow">إثبات القيمة</p>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: "var(--sp-4)" }}>
        {items.map((item) => (
          <div key={item.label} style={{ textAlign: "center" }}>
            <div className="stat-value" style={{ fontSize: "1.8rem" }}>{item.value}</div>
            <p className="stat-label">{item.label}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
