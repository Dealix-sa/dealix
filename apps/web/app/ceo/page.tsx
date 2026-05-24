import { FounderShell } from "../../components/founder-console/founder-shell";
import { getLayer } from "../../lib/dealix-runtime";

export default async function CEOPage() {
  const layer = await getLayer("ceo_os");
  return (
    <FounderShell
      title="CEO"
      subtitle="Daily brief + weekly review status."
      source={layer.source === "live" || layer.source === "files" ? layer.source : "fallback"}
    >
      <ul>
        <li>Daily brief generator: <code>make ceo-daily-brief</code></li>
        <li>Weekly review generator: <code>make ceo-weekly-review</code></li>
        <li>Doc present: {String(layer.present)}</li>
        <li>Source-of-truth: <code>{layer.doc_rel || "docs/company/DEALIX_CEO_OS.md"}</code></li>
      </ul>
    </FounderShell>
  );
}
