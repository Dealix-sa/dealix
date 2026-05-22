import { RiskScoreFunnel } from "@/components/gtm/RiskScoreFunnel";

export default function RiskScorePage() {
  return (
    <div className="min-h-screen bg-background grid-pattern">
      <div className="mx-auto max-w-4xl px-6 py-16">
        <RiskScoreFunnel />
      </div>
    </div>
  );
}
