import { ConsolePage } from "../../components/brand/console-page";

export const metadata = { title: "Security — Dealix" };

export default function Page() {
  return (
    <ConsolePage
      eyebrow="Security Operating Surface"
      title="Security"
      description="Policies, scans, incidents and access. Every external interaction passes through trust + security gates."
      status={{ tone: "ok", label: "monitored" }}
      sections={[
        { title: "Access", bullets: ["Founder, operator, customer roles", "Least privilege by default", "Per-action audit"] },
        { title: "Scanning", bullets: ["Secrets (gitleaks, detect-secrets)", "Static analysis (bandit, ruff)", "SBOM and dependency scans"] },
        { title: "Incidents", bullets: ["Runbook: docs/SECURITY_RUNBOOK.md", "On-call: docs/ON_CALL.md", "Post-mortem template enforced"] },
        { title: "AI-specific", description: "OWASP LLM Top 10 mapped controls.", bullets: ["Prompt-injection drills", "Excessive-agency limits", "Output validation"] },
      ]}
      trustNote="Security events are first-class trust events: every block, every drill, every incident lives in the audit log."
      related={[
        { href: "/trust", label: "Trust Center" },
        { href: "/audit", label: "Audit Log" },
        { href: "/sovereign", label: "Sovereign" },
      ]}
    />
  );
}
