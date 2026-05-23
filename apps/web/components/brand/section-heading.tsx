export function SectionHeading({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <header style={{ marginBottom: 16 }}>
      <h1 className="dealix-section-heading" style={{ fontSize: 22 }}>
        {title}
      </h1>
      {subtitle && <p className="dealix-section-sub">{subtitle}</p>}
    </header>
  );
}
