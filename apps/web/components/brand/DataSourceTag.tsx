export type DataSource = "api" | "fallback";

export function DataSourceTag({ source }: { source: DataSource }) {
  const label = source === "api" ? "LIVE DATA" : "FALLBACK DATA";
  const className =
    source === "api" ? "dx-source dx-source--api" : "dx-source dx-source--fallback";
  return <span className={className}>{label}</span>;
}
