import { ConsolePage } from "../../components/brand/console-page";

export const metadata = { title: "Sovereign — Dealix" };

export default function Page() {
  return (
    <ConsolePage
      eyebrow="Sovereignty Operating Surface"
      title="Sovereign"
      description="Saudi data residency, sovereign deployment posture, and customer-controlled key options for enterprise customers."
      status={{ tone: "ok", label: "KSA-ready" }}
      sections={[
        { title: "Residency", bullets: ["KSA-region storage option", "Cross-border replication off by default", "Documented for enterprise procurement"] },
        { title: "Keys", bullets: ["Per-tenant encryption keys", "Customer-managed keys (CMK) option"] },
        { title: "Audit", bullets: ["Sovereign audit log mirror", "Export on customer request"] },
      ]}
      trustNote="Sovereignty is a contract; it is enforced in code, not in marketing copy."
      related={[
        { href: "/security", label: "Security" },
        { href: "/trust", label: "Trust Center" },
      ]}
    />
  );
}
