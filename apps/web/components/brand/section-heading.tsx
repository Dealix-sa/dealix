interface SectionHeadingProps {
  eyebrow?: string;
  title: string;
  description?: string;
}

export function SectionHeading({ eyebrow, title, description }: SectionHeadingProps) {
  return (
    <header style={{ marginBottom: 20 }}>
      {eyebrow ? (
        <div
          style={{
            color: "var(--dx-accent)",
            fontSize: "0.75rem",
            fontWeight: 700,
            letterSpacing: "0.2em",
            textTransform: "uppercase",
            marginBottom: 8,
          }}
        >
          {eyebrow}
        </div>
      ) : null}
      <h1
        className="dx-heading"
        style={{ fontSize: "1.75rem", margin: 0, letterSpacing: "-0.01em" }}
      >
        {title}
      </h1>
      {description ? (
        <p className="dx-muted" style={{ margin: "8px 0 0 0", maxWidth: 720 }}>
          {description}
        </p>
      ) : null}
    </header>
  );
}

export default SectionHeading;
