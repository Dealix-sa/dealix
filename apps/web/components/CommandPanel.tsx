"use client";

export default function CommandPanel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="card" style={{ marginTop: "var(--sp-6)" }}>
      <h3 style={{ marginBottom: "var(--sp-4)" }}>{title}</h3>
      {children}
    </section>
  );
}
