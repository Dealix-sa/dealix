import { ConsolePage } from "../../components/brand/console-page";

export const metadata = { title: "Trust Center — Dealix" };

export default function Page() {
  return (
    <ConsolePage
      eyebrow="Governance Operating Surface"
      title="Trust Center"
      description="Audit log, suppression lists, eval gates and the policy-as-code that keeps Dealix trust-gated by default."
      status={{ tone: "ok", label: "enforced" }}
      sections={[
        { title: "Audit log", description: "Every internal and external action recorded with actor, target and decision.", bullets: ["Append-only", "Searchable by entity and time", "Exportable for audits"] },
        { title: "Suppression list", description: "Accounts, addresses and identifiers that must never receive outreach.", bullets: ["Honoured by every distribution machine", "Updated on request and on unsubscribe"] },
        { title: "Eval gates", description: "Quality and safety evals run before any agent output reaches production.", bullets: ["Eval Guardian agent", "Failing evals block release"] },
        { title: "Policy-as-code", description: "Allowed and forbidden actions defined in code, not in prose.", bullets: ["External send forbidden by default", "Pricing changes require founder approval", "Bulk export forbidden without ticket"] },
      ]}
      trustNote="The Trust Center is the canonical place to investigate any action Dealix has taken. If something is not here, it did not happen."
      related={[
        { href: "/evals", label: "Evals" },
        { href: "/audit", label: "Audit Log" },
        { href: "/security", label: "Security" },
      ]}
    />
  );
}
