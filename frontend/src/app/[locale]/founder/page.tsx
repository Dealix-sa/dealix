import { PublicShell } from "@/components/layout/PublicShell";
import { FounderLaunchBoard } from "@/components/founder/FounderLaunchBoard";

export default function FounderPage() {
  return (
    <PublicShell>
      <div className="page-container page-content max-w-5xl mx-auto">
        <FounderLaunchBoard />
      </div>
    </PublicShell>
  );
}
