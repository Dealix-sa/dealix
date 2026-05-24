import { ConsolePage } from "../../components/brand/console-page";

export const metadata = { title: "Worker Orchestrator — Dealix" };

export default function Page() {
  return (
    <ConsolePage
      eyebrow="Runtime Operating Surface"
      title="Worker Orchestrator"
      description="Jobs, queues and schedules across distribution, finance, delivery and intelligence workers."
      status={{ tone: "ok", label: "scheduled" }}
      sections={[
        { title: "Distribution workers", bullets: ["Draft generators", "Reply router", "Follow-up planner"] },
        { title: "Intelligence workers", bullets: ["Sector ranking", "Account scoring", "Trigger event watcher"] },
        { title: "Finance workers", bullets: ["Invoice generator", "Receivables ageing", "Cash forecaster"] },
        { title: "Delivery workers", bullets: ["Sample renderer", "Proposal renderer", "QA checklist runner"] },
      ]}
      trustNote="Workers never break trust gates. A worker that needs external action enqueues an approval item; the founder decides."
      related={[
        { href: "/control-plane", label: "Control Plane" },
        { href: "/audit", label: "Audit Log" },
      ]}
    />
  );
}
