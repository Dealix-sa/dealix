import { ConsolePage } from "../../components/brand/console-page";

export const metadata = { title: "Audit Log — Dealix" };

export default function Page() {
  return (
    <ConsolePage
      eyebrow="Governance Operating Surface"
      title="Audit Log"
      description="Every event, every actor, every decision. Append-only, searchable, exportable."
      status={{ tone: "ok", label: "append-only" }}
      sections={[
        { title: "Event taxonomy", bullets: ["Brand events (logo / token changes)", "Distribution events (draft / queue / approve)", "Finance events (invoice / payment / refund)", "Trust events (gate hit / violation)"] },
        { title: "Retention", bullets: ["Indefinite append", "Periodic cold-storage roll", "Sovereign storage where required"] },
      ]}
      trustNote="The audit log is the legal record of what Dealix did. Tampering is impossible by design."
      related={[
        { href: "/trust", label: "Trust Center" },
        { href: "/security", label: "Security" },
      ]}
    />
  );
}
