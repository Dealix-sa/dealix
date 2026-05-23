import type { TopAction } from "../../lib/types";

export function CEOTopAction({ action }: { action: TopAction }) {
  return (
    <div className="card" style={{ borderColor: "#0f172a" }}>
      <p style={{ margin: 0, fontSize: 12, textTransform: "uppercase", letterSpacing: "0.06em", opacity: 0.7 }}>
        Top CEO Action
      </p>
      <h2 style={{ marginTop: 6, marginBottom: 6 }}>{action.title}</h2>
      <p style={{ margin: 0 }}>{action.detail}</p>
      <a
        href={action.href}
        style={{
          display: "inline-block",
          marginTop: 12,
          padding: "6px 14px",
          background: "#0f172a",
          color: "#fff",
          borderRadius: 8,
          textDecoration: "none",
        }}
      >
        {action.cta}
      </a>
    </div>
  );
}
