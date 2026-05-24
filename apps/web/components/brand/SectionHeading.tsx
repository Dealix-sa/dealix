export function SectionHeading({
  title,
  meta,
}: {
  title: string;
  meta?: string;
}) {
  return (
    <div className="dx-section-heading">
      <h2 className="dx-section-heading__title">{title}</h2>
      {meta ? <span className="dx-section-heading__meta">{meta}</span> : null}
    </div>
  );
}
