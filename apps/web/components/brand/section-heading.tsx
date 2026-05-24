export function SectionHeading({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <header className="dlx-page-header">
      <h1>{title}</h1>
      {subtitle ? <span className="dlx-subtitle">{subtitle}</span> : null}
    </header>
  );
}
