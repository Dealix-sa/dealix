import { FounderShell } from "../components/founder/founder-shell";

export default function HomePage() {
  return (
    <FounderShell
      title="Dealix Founder Console"
      subtitle="AI prepares. Humans approve. One internal cockpit for the whole company."
    >
      <div className="card">
        <p>
          Open <a href="/ceo">/ceo</a> for the daily briefing. Use the nav above
          for the rest of the operating layer.
        </p>
      </div>
    </FounderShell>
  );
}
