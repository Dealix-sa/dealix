export function OfferCard({
  name,
  price,
  cycle,
  description,
}: {
  name: string;
  price: string;
  cycle: string;
  description: string;
}) {
  return (
    <div className="dlx-card" style={{ marginBottom: 0 }}>
      <h2>{name}</h2>
      <div className="dlx-metric" style={{ marginBottom: 4 }}>
        <span className="dlx-metric-value">{price}</span>
        <span className="dlx-metric-label">{cycle}</span>
      </div>
      <p style={{ margin: 0, fontSize: 13, color: "#475569" }}>{description}</p>
    </div>
  );
}
