"use client";

export default function SectionHeader({ eyebrow, title, description }: { eyebrow?: string; title: string; description?: string }) {
  return (
    <div style={{ marginBottom: "var(--sp-6)" }}>
      {eyebrow && <p className="eyebrow">{eyebrow}</p>}
      <h2>{title}</h2>
      {description && <p style={{ maxWidth: 680 }}>{description}</p>}
    </div>
  );
}
